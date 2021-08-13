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
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


#This is a Hole-burning program designed for SiV nano-pyramids with permanent hole-burning possibilities with a resonant laser.
#The sequence reads as follow : First we close the shutter of the green laser and start burning with the red laser (time : tburn)
#Then the red laser is scanned in a range difined by ampscan and offset (time: tscan)
#Then we reopen the shutter and repopulate the bright state with the green laser (time : tgreen)

class Photon_Counter(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Timing Parameter ##
        #The program aquires the total number of photons at a rate defined by real_sampling_rate, but will only display an average of it every dt

        self.unit=1e-4 #unit of time in s
        self.tscan=500 # in unit of time
        self.tburn=1000 # Include the time to close the sutter (~80 ms) + the burning time
        self.tgreen=3000 # Include the time to open the shutter (~200 ms)+ the time with the green laser on
        self.ampscan=1 # in V
        self.offset=0 # in V
        self.freq_range=20 #GHz


        self.average_trace=True #Average the trace


     
        

        self.is_calibrate=False
        self.all_sequence=False

        

        ##Creation of the graphical interface##

        self.setWindowTitle("Hole Burning")

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
        self.use_calibrate=QCheckBox('Use calibration', self)
        self.use_calibrate.setEnabled(False)
        self.show_all_sequence=QCheckBox('Show all sequence', self)
        self.shutter_open=QPushButton('Open Shutter')
        self.shutter_close=QPushButton('Close Shutter')
        self.labeliter=QLabel("iter #")
        self.savebutton=QPushButton('Sava data')
        self.trace_button=QPushButton('Keep Trace')


        Vbox_droite.addWidget(self.calibrate)   
        Vbox_droite.addWidget(self.stop_calibrate)
        Vbox_droite.addWidget(self.use_calibrate)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.show_all_sequence)
        Vbox_droite.addWidget(self.start)
        Vbox_droite.addWidget(self.stop)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.trace_button)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.shutter_open)
        Vbox_droite.addWidget(self.shutter_close)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.savebutton)
        Vbox_droite.addWidget(self.labeliter)   


        #Labels on the left
        gras=QFont( "Consolas", 40, QFont.Bold)

        self.labelunit=QLabel("unité de temps (s)")
        self.labeltscan=QLabel("Temps de scan (UT) ")
        self.labeltburn=QLabel("Temps de burning (UT)")
        self.labeltgreen=QLabel("Temps d'éclairage vert (UT)")
        self.labelampscan=QLabel("Amplitude scan (V) ")   
        self.labeloffset=QLabel("Offset (V) ") 
        self.labelfreq_range=QLabel("Plage de fréquence (GHz)")

        self.lectunit=QLineEdit(str(self.unit))
        self.lecttscan=QLineEdit(str(self.tscan))
        self.lecttburn=QLineEdit(str(self.tburn))
        self.lecttgreen=QLineEdit(str(self.tgreen))
        self.lectampscan=QLineEdit(str(self.ampscan))
        self.lectoffset=QLineEdit(str(self.offset))
        self.lectfreq_range=QLineEdit(str(self.freq_range))
        

        Vbox_gauche.addWidget(self.labelunit)
        Vbox_gauche.addWidget(self.lectunit)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labeltscan)
        Vbox_gauche.addWidget(self.lecttscan)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labeltburn)
        Vbox_gauche.addWidget(self.lecttburn)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labeltgreen)
        Vbox_gauche.addWidget(self.lecttgreen)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labelampscan)
        Vbox_gauche.addWidget(self.lectampscan)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labeloffset)
        Vbox_gauche.addWidget(self.lectoffset)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labelfreq_range)
        Vbox_gauche.addWidget(self.lectfreq_range)

        
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
        self.shutter_open.clicked.connect(self.open_shutter)
        self.shutter_close.clicked.connect(self.close_shutter)
        self.savebutton.clicked.connect(self.save_data)
        self.trace_button.clicked.connect(self.add_trace)

        self.use_calibrate.stateChanged.connect(self.use_calibration)
        self.show_all_sequence.stateChanged.connect(self.showing_all_sequence)

        ## Timer Setup ##

        self.timer = QTimer(self,interval=0) #ms
        self.timer.timeout.connect(self.update_canvas)

        self.timer_calib=QTimer(self,interval=0)
        self.timer_calib.timeout.connect(self.update_calib)

    def update_canvas(self):       
        ##Update the plot by averaging##
        #data contains the integrated (counter) PL of all the sequence
        #y is differentiate of data, either on all the sequence or just the scan
        #y_avg is the average of y over all tries

        self.n_iter+=1
        self.labeliter.setText("iter # %d" % self.n_iter)


        self.sr.read_many_sample_double(self.data,number_of_samples_per_channel=len(self.data))
        
        if self.all_sequence :
            self.y=np.zeros(self.N)
            for i in range (len(self.y)) : 
                self.y[i]=(self.data[i+1]-self.data[i])/self.unit
        else :
            self.y=np.zeros(self.tscan)
            for i in range (len(self.y)) : 
                self.y[i]=(self.data[i+1+self.tburn]-self.data[i+self.tburn])/self.unit

        

        if self.is_calibrate and len(self.calib)==len(self.y_avg):
            self.y=self.y/self.calib

        self.y_avg=self.y_avg*((self.n_iter-1)/self.n_iter)+self.y*1/self.n_iter


        
        
        
        ymax=max(self.y_avg)
        ymin=min(self.y_avg)
        self.dynamic_line.set_ydata(self.y_avg)
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
        self.tburn=np.int(self.lecttburn.text())
        self.tgreen=np.int(self.lecttgreen.text())
        self.ampscan=np.float(self.lectampscan.text())
        self.offset=np.float(self.lectoffset.text())
        self.unit=np.float(self.lectunit.text())
        self.freq_range=np.float(self.lectfreq_range.text())



        self.sampling_rate=1/self.unit

        self.N=self.tscan+self.tburn+self.tgreen

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
        rampe=np.linspace(vmin,vmax,self.tscan+1)
        self.signal=[self.offset]*self.tburn+list(rampe)+[self.offset]*self.tgreen


        self.ramp.write(self.signal)
        self.ramp.start()

        #Shutter control
        self.shutter=nidaqmx.Task()
        self.shutter.do_channels.add_do_chan('Dev1/port0/line0')
        self.shutter.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N+1)

        self.shutter.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/Ctr0ArmStartTrigger') 

        self.cmd_shutter=[False]*(self.tburn+self.tscan+1)+[True]*self.tgreen

        self.shutter.write(self.cmd_shutter)
        self.shutter.start()

               
        #PL buffer creation
        self.data=np.zeros(self.N+1)
        
        #Adjust time axis
        if self.all_sequence :
            self.t=np.arange(0,self.N*self.unit,self.unit)
            self.dynamic_ax.set_xlabel("Temps (s)")
        else : 
            self.t=np.linspace(0,self.freq_range,self.tscan)
            self.dynamic_ax.set_xlabel("Freq (GHz)")
        self.dynamic_line.set_xdata(self.t)
        xmax=max(self.t)
        self.dynamic_ax.set_xlim([0,xmax])

        #Create y-axis
        if self.all_sequence :
            self.y_avg=np.zeros(self.N)
        else : 
            self.y_avg=np.zeros(self.tscan)
        self.dynamic_ax.set_ylabel("PLE (counts/s)")

        #Start the timer 
        self.timer.start() 

              

    def stop_measure(self):
        #Stop the measuring, clear the tasks on both counters
        try :
            self.timer.stop()
        except :
            pass
        try :
            self.sample_clock.close()
        except :
            pass
        try :
            self.counter.close()
        except :
            pass
        try :
            self.ramp.close()
        except :
            pass
        try :
            self.shutter.close()
        except :
            pass
        with nidaqmx.Task() as reset :
            reset.ao_channels.add_ao_voltage_chan('Dev1/ao0')
            reset.write(self.offset)
        self.open_shutter()


    def calibration(self):
        #Read parameters
        self.tscan=np.int(self.lecttscan.text())
        self.ampscan=np.float(self.lectampscan.text())
        self.offset=np.float(self.lectoffset.text())
        self.unit=np.float(self.lectunit.text())

        self.sampling_rate=1/self.unit
        if self.all_sequence :
            self.N=self.tscan+self.tburn+self.tgreen
        else :
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
        rampe=np.linspace(vmin,vmax,self.tscan+1)
        if self.all_sequence :
            self.signal=[self.offset]*self.tburn+list(rampe)+[self.offset]*self.tgreen
        else :            
            self.signal=list(rampe)


        self.ramp.write(self.signal)
        self.ramp.start()

        #Photodiode reading
        self.pd=nidaqmx.Task()
        self.pd.ai_channels.add_ai_voltage_chan('Dev1/ai0')
        self.pd.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N+1)

        #Adjust time axis
        self.t=np.arange(0,self.N*self.unit,self.unit)
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
            self.calib=self.calib_avg[0:self.N]/max(self.calib_avg)
            self.use_calibrate.setEnabled(True)


    def showing_all_sequence(self):
        self.all_sequence=not self.all_sequence

    def use_calibration(self) :
        self.is_calibrate=not self.is_calibrate

    def open_shutter(self):
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan('Dev1/port0/line0')
            task.write(True)
            while not task.is_task_done() :
                pass

    def close_shutter(self):
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan('Dev1/port0/line0')
            task.write(False)
            while not task.is_task_done() :
                pass
                


    def save_data(self):
        fname = QFileDialog.getSaveFileName(self, 'Sava data','d:\\DATA\\',"Data files (*.txt *.csv)") # return ("path/to/file", "data type")
        fname=fname[0]
        if not ".txt" in fname :
            fname=fname+'.txt'
        with open(fname, "w") as file :
            xaxis=self.dynamic_line.get_xdata() # Both work and return lists
            yaxis=self.dynamic_line._y
            for i in range(len(xaxis)) :
                file.write("%5.4E \t %5.4E \n" % (xaxis[i],yaxis[i]))

    def moving_average(self,a, n=11) : # Return a moving average over n, starting on (n+1)/2 and ending on N-(n-1)/2
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n


    def add_trace(self):
        try : 
            self.static_line.remove() 
        except :
            pass
        xaxis=self.dynamic_line.get_xdata()
        yaxis=self.dynamic_line.get_ydata()
        if self.average_trace :
            yavg=self.moving_average(yaxis,n=11)
            xavg=xaxis[5:-5]
            self.static_line,=self.dynamic_ax.plot(xavg, yavg, 'r')
        else :
            self.static_line,=self.dynamic_ax.plot(xaxis, yaxis, 'r')



        







qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()

app.stop_measure()