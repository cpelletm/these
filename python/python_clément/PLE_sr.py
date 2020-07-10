import sys
import time
import random
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system

import numpy as np

from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


#This is a photon counter for the NI 6341 card when the TTL signal is plugged into ctr0/source which is on pin PFI8/P2.0/81
#Physical channels used : ctr0 for APD, ctr1 for sample clock

class Photon_Counter(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Timing Parameter ##
        #The program aquires the total number of photons at a rate defined by real_sampling_rate, but will only display an average of it every dt

        self.unit=1e-4 #unit of time in s
        self.tscan=500 # in unit of time
        self.ampscan=1 # in V
        self.offset=0 # in V
        self.navg=1

        


     
        

        self.is_calibrate=False
        self.PLvert=0.
        

        ##Creation of the graphical interface##

        self.setWindowTitle("PLE")

        self.main = QWidget()
        self.setCentralWidget(self.main)

        layout= QHBoxLayout()
        Vbox_gauche=QVBoxLayout()
        Vbox = QVBoxLayout()
        Vbox_droite=QVBoxLayout()


        layout.addLayout(Vbox_gauche)
        layout.addLayout(Vbox)
        layout.addLayout(Vbox_droite)
        self.main.setLayout(layout)

        #Buttons on the right
        self.stop=QPushButton('Stop')
        self.start=QPushButton('Start')
        self.calibrate=QPushButton('Calibrate')
        self.stop_calibrate=QPushButton('Stop Calibrate')
        self.reset_calibrate=QPushButton('Reset Calibration')
        self.labeliter=QLabel("iter #")
        self.labelplvert=QLabel("PL vert :")
        self.lectPLvert=QLineEdit(str(self.PLvert))

        Vbox_droite.addWidget(self.calibrate)   
        Vbox_droite.addWidget(self.stop_calibrate)
        Vbox_droite.addWidget(self.reset_calibrate)
        Vbox_droite.addWidget(self.labelplvert)
        Vbox_droite.addWidget(self.lectPLvert)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.start)
        Vbox_droite.addWidget(self.stop)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.labeliter)    
        #Labels on the left
        gras=QFont( "Consolas", 40, QFont.Bold)

        self.labelunit=QLabel("unité de temps (s)")
        self.labeltscan=QLabel("Temps de scan (UT) ")
        self.labelampscan=QLabel("Amplitude scan (V) ")   
        self.labeloffset=QLabel("Offset (V) ") 

        self.lectunit=QLineEdit(str(self.unit))
        self.lecttscan=QLineEdit(str(self.tscan))
        self.lectampscan=QLineEdit(str(self.ampscan))
        self.lectoffset=QLineEdit(str(self.offset))
        

        Vbox_gauche.addWidget(self.labelunit)
        Vbox_gauche.addWidget(self.lectunit)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labeltscan)
        Vbox_gauche.addWidget(self.lecttscan)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labelampscan)
        Vbox_gauche.addWidget(self.lectampscan)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labeloffset)
        Vbox_gauche.addWidget(self.lectoffset)

        
        #Plot in the middle + toolbar

        dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
        Vbox.addStretch(1)
        Vbox.addWidget(dynamic_canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))


        ## Matplotlib Setup ##

        self.dynamic_ax = dynamic_canvas.figure.subplots()
        self.t=np.zeros(100)
        self.y=np.zeros(100)
        
        self.dynamic_line,=self.dynamic_ax.plot(self.t, self.y)
        
              
        #Define the buttons' action 
        
        self.start.clicked.connect(self.start_measure)
        self.stop.clicked.connect(self.stop_measure)
        self.calibrate.clicked.connect(self.calibration)
        self.stop_calibrate.clicked.connect(self.stop_calibration)
        self.reset_calibrate.clicked.connect(self.reset_calibration)

        ## Timer Setup ##

        self.timer = QTimer(self,interval=0) #ms
        self.timer.timeout.connect(self.update_canvas)

        self.timer_calib=QTimer(self,interval=0)
        self.timer_calib.timeout.connect(self.update_calib)

    def update_canvas(self):       
        ##Update the plot by averaging##

        self.n_iter+=1
        self.labeliter.setText("iter # %d" % self.n_iter)


        self.sr.read_many_sample_double(self.data,number_of_samples_per_channel=len(self.data))
        
        
        self.y=np.zeros(self.N)

        for i in range (self.N) : #look for the values at the beginning and the end of the readout
            self.y[i]=(self.data[i+1]-self.data[i])/self.unit

        if self.is_calibrate :
            self.y=self.PLvert*np.ones(self.N)+(self.y-self.PLvert)/self.calib[0:self.N]

        self.y_avg=self.y_avg*((self.n_iter-1)/self.n_iter)+self.y*1/self.n_iter
        
   
        self.dynamic_line.set_ydata(self.y_avg)
        ymax=max(self.y_avg)
        ymin=min(self.y_avg)
        self.dynamic_ax.set_ylim([ymin,ymax])  
        self.dynamic_ax.figure.canvas.draw()

    def update_calib(self):
        ##Update the calibration average##

        self.n_iter+=1
        self.labeliter.setText("iter # %d" % self.n_iter)
        single=np.array(self.pd.read(self.N+1))
        self.calib_avg=self.calib_avg*((self.n_iter-1)/self.n_iter)+single*1/self.n_iter

        self.dynamic_line.set_ydata(self.calib_avg[0:self.N]) #Last point is not plotted to match the PL plot
        ymax=max(self.calib_avg)
        self.dynamic_ax.set_ylim([0,ymax])
        self.dynamic_ax.figure.canvas.draw()




    def start_measure(self):
        ## What happens when you click "start" ##

        #Read parameters
        self.tscan=np.int(self.lecttscan.text())
        self.ampscan=np.float(self.lectampscan.text())
        self.offset=np.float(self.lectoffset.text())
        self.unit=np.float(self.lectunit.text())
        self.PLvert=np.float(self.lectPLvert.text())

        self.sampling_rate=1/self.unit

        self.N=self.tscan

        self.n_iter=0
        #Sample Clock creation (On counter1)

        self.sample_clock=nidaqmx.Task()
        self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.sampling_rate)
        self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse
        self.sample_clock.start()

        



        #Counter creation
        self.counter=nidaqmx.Task()
        self.counter.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.counter.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N+1)
        self.sr=nidaqmx.stream_readers.CounterReader(self.counter.in_stream)

        self.counter.triggers.arm_start_trigger.dig_edge_src='/Dev1/100kHzTimebase'
        self.counter.triggers.arm_start_trigger.trig_type=nidaqmx.constants.TriggerType.DIGITAL_EDGE


        
        
        #Ramp creation
        self.ramp=nidaqmx.Task()
        self.ramp.ao_channels.add_ao_voltage_chan('Dev1/ao0')
        self.ramp.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N+1)

        self.ramp.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/Ctr0ArmStartTrigger') 


        vmin=self.offset-self.ampscan/2
        vmax=self.offset+self.ampscan/2
        self.signal=np.linspace(vmin,vmax,self.N+1)
        self.signal=list(self.signal)


        self.ramp.write(self.signal)
        self.ramp.start()

               
        #PL buffer creation
        self.data=np.zeros(self.N+1)
        
        #Adjust time axis
        self.t=np.arange(0,self.tscan*self.unit,self.unit)
        self.dynamic_line.set_xdata(self.t)
        xmax=max(self.t)
        self.dynamic_ax.set_xlim([0,xmax])

        #Create y-axis
        self.y_avg=np.zeros(self.N)

        #Start the timer 
        self.timer.start() 

              

    def stop_measure(self):
        #Stop the measuring, clear the tasks on both counters
        self.timer.stop()
        self.sample_clock.close()
        self.counter.close()
        self.ramp.close()
        with nidaqmx.Task() as reset :
            reset.ao_channels.add_ao_voltage_chan('Dev1/ao0')
            reset.write(self.offset)


    def calibration(self):
        #Read parameters
        self.tscan=np.int(self.lecttscan.text())
        self.ampscan=np.float(self.lectampscan.text())
        self.offset=np.float(self.lectoffset.text())
        self.unit=np.float(self.lectunit.text())

        self.sampling_rate=1/self.unit

        self.N=self.tscan

        self.n_iter=0
        #Sample Clock creation (On counter1)

        self.sample_clock=nidaqmx.Task()
        self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.sampling_rate)
        self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse
        self.sample_clock.start()
        
        #Ramp creation
        self.ramp=nidaqmx.Task()
        self.ramp.ao_channels.add_ao_voltage_chan('Dev1/ao0')
        self.ramp.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N+1)

        self.ramp.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/ai/StartTrigger') 


        vmin=self.offset-self.ampscan/2
        vmax=self.offset+self.ampscan/2
        self.signal=np.linspace(vmin,vmax,self.N+1)
        self.signal=list(self.signal)


        self.ramp.write(self.signal)
        self.ramp.start()

        #Photodiode reading
        self.pd=nidaqmx.Task()
        self.pd.ai_channels.add_ai_voltage_chan('Dev1/ai0')
        self.pd.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N+1)

        #Adjust time axis
        self.t=np.arange(0,self.tscan*self.unit,self.unit)
        self.dynamic_line.set_xdata(self.t)
        xmax=max(self.t)
        self.dynamic_ax.set_xlim([0,xmax])

        self.calib_avg=np.zeros(self.N+1)

        self.timer_calib.start()

    def stop_calibration(self) :
        self.timer_calib.stop()
        self.sample_clock.close()
        self.pd.close()
        self.ramp.close()
        with nidaqmx.Task() as reset :
            reset.ao_channels.add_ao_voltage_chan('Dev1/ao0')
            reset.write(self.offset)
        if self.calib_avg[0] != 0 :
            self.calib=self.calib_avg/max(self.calib_avg)
            #,self.is_calibrate=True

    def reset_calibration(self) :
        self.is_calibrate=False


        







qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()

app.sample_clock.close()#just in case
app.ramp.close()
app.counter.close() 
app.pd.close()