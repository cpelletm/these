import sys
import time
import random
import os
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system
import visa

import numpy as np

from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QFileDialog, QCheckBox)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


#This is a photon counter for the NI 6341 card when the TTL signal is plugged into ctr0/source which is on pin PFI8/P2.0/81
#Physical channels used : ctr0 for APD, ctr1 for sample clock

class MyToolbar(NavigationToolbar): #Modification of the toolbar to save data with the plot
    
    def save_figure(self, *args): #Requires os and QFileDialog from PyQt5.QtWidgets

        try : #Test if there is a previous path saved
            if self.startpath :
                pass
        except :
            self.startpath="D:/DATA" #Default folder to save at
        
        start = os.path.join(self.startpath, self.canvas.get_default_filename())
        

        fname, filter = QFileDialog.getSaveFileName(self.canvas.parent(),
                                         "Choose a filename to save to",
                                         start, "Images (*.png)")

        data=[]
        lmax=0
        for ax in self.canvas.figure.get_axes() :
            for line in ax.get_lines() :
                if len(line._x)>lmax :
                    lmax=len(line._x)

        for ax in self.canvas.figure.get_axes() :
            for line in ax.get_lines() :
                x=list(line._x)
                if len(x) < lmax :
                    x+=[-1]*(lmax-len(x))
                y=list(line._y)
                if len(y) < lmax :
                    y+=[-1]*(lmax-len(y))
                data+=[x]
                data+=[y]

        fdataname=fname[:-4]+".txt"
        with open(fdataname,'w') as f: #Needs an update if the lines have differents sizes
            for i in range(len(data[0])) :
                for ligne in data :
                    f.write("%5.4E \t"%ligne[i]) #Format = 5 significative numbers, scientific notation

                f.write("\n")


        if fname:
            # Save dir for next time, unless empty str (i.e., use cwd).
            self.startpath = os.path.dirname(fname)
            try:
                self.canvas.figure.savefig(fname)
            except :
                print('Could not save file !')

class Photon_Counter(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Timing Parameter ##
        #The program aquires the total number of photons at a rate defined by real_sampling_rate, but will only display an average of it every dt

        self.unit=2e-6
        self.time_pola=100
        self.time_wait=200
        self.time_read=200
        self.freq=2865
        self.puissance=10

        self.time_total=self.time_pola+self.time_wait+self.time_read
        


     
        self.refresh_rate=0.1  
        self.time_last_refresh=time.time()

        

        ##Creation of the graphical interface##

        self.setWindowTitle("Temps de polarisation")

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
        self.labelIter=QLabel("iter # 0")
        self.normalize_cb=QCheckBox('Normalize')
        self.keep_button=QPushButton('Keep trace')
        self.clear_button=QPushButton('Clear Last Trace')

        Vbox_droite.addWidget(self.normalize_cb)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.start)
        Vbox_droite.addWidget(self.stop)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.keep_button)
        Vbox_droite.addWidget(self.clear_button)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.labelIter)
        
        #Labels on the left
        gras=QFont( "Consolas", 40, QFont.Bold)

        self.labelunit=QLabel("unité de temps (s)")
        self.lectunit=QLineEdit(str(self.unit))   
        Vbox_gauche.addWidget(self.labelunit)
        Vbox_gauche.addWidget(self.lectunit)
        Vbox_gauche.addStretch(1)
        self.labeltime_pola=QLabel("time_pola")
        self.lecttime_pola=QLineEdit(str(self.time_pola))
        Vbox_gauche.addWidget(self.labeltime_pola)
        Vbox_gauche.addWidget(self.lecttime_pola)
        self.labeltime_wait=QLabel("time_wait")
        self.lecttime_wait=QLineEdit(str(self.time_wait))
        Vbox_gauche.addWidget(self.labeltime_wait)
        Vbox_gauche.addWidget(self.lecttime_wait)
        self.labeltime_read=QLabel("time_read")
        self.lecttime_read=QLineEdit(str(self.time_read))
        Vbox_gauche.addWidget(self.labeltime_read)
        Vbox_gauche.addWidget(self.lecttime_read)
        Vbox_gauche.addStretch(1)
        self.labelfreq=QLabel("freq")
        self.lectfreq=QLineEdit(str(self.freq))
        Vbox_gauche.addWidget(self.labelfreq)
        Vbox_gauche.addWidget(self.lectfreq)
        Vbox_gauche.addStretch(1)
        self.labelpuissance=QLabel("puissance")
        self.lectpuissance=QLineEdit(str(self.puissance))
        Vbox_gauche.addWidget(self.labelpuissance)
        Vbox_gauche.addWidget(self.lectpuissance)
        Vbox_gauche.addStretch(1)


        
        #Plot in the middle + toolbar

        dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
        Vbox.addStretch(1)
        Vbox.addWidget(dynamic_canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        MyToolbar(dynamic_canvas, self))


        ## Matplotlib Setup ##

        self.dynamic_ax = dynamic_canvas.figure.subplots()
        self.t=np.zeros(100)
        self.y=np.zeros(100)
        
        self.dynamic_line,=self.dynamic_ax.plot(self.t, self.y)
        
              
        #Define the buttons' action 
        
        self.start.clicked.connect(self.start_measure)
        self.stop.setEnabled(False)
        self.stop.clicked.connect(self.stop_measure)
        self.keep_button.clicked.connect(self.keep_trace)
        self.clear_button.clicked.connect(self.clear_trace)

        ## Timer Setup ##

        self.timer = QTimer(self,interval=0)
        self.timer.timeout.connect(self.update_canvas)

    def keep_trace(self):
        self.dynamic_ax.plot(self.dynamic_line._x,self.dynamic_line._y)

    def clear_trace(self):
        lines=self.dynamic_ax.get_lines()
        line=lines[-1]
        if line != self.dynamic_line :
            line.remove()
        self.dynamic_ax.figure.canvas.draw()


    def update_value(self):
        self.unit=np.float(self.lectunit.text())
        self.time_pola=np.int(self.lecttime_pola.text())
        self.time_wait=np.int(self.lecttime_wait.text())
        self.time_read=np.int(self.lecttime_read.text())

        self.freq=np.float(self.lectfreq.text())
        self.puissance=np.float(self.lectpuissance.text())

        self.time_total=self.time_pola+self.time_wait+self.time_read
        self.N_tot=self.time_total+1
        self.dt=self.unit
        self.sampling_rate=1/self.dt

        self.x=np.arange(self.N_tot-1)*self.dt
        self.y=np.zeros(self.N_tot-1)
        xmin=min(self.x)
        xmax=max(self.x)
        self.dynamic_ax.set_xlim([xmin,xmax]) 
        self.dynamic_line.set_data(self.x,self.y)

        self.data=np.zeros(self.N_tot)

        self.N_iter=1
        

    def update_canvas(self):       
        ##Update the plot and the value of the PL ##

        self.sr.read_many_sample_double(self.data,number_of_samples_per_channel=len(self.data)) #read the N value during dt
      

        PL=(self.data[1:]-self.data[:-1])*self.sampling_rate


        
        if min(PL) >= 0 :
            self.y=PL/self.N_iter+self.y*(1-1/self.N_iter)
            self.N_iter+=1

        if self.normalize_cb.isChecked() :
            yplot=self.y/max(self.y)
        else :
            yplot=self.y
        if time.time()-self.time_last_refresh>self.refresh_rate :
            self.time_last_refresh=time.time()
            self.dynamic_line.set_ydata(yplot)
            y_relevant=list(yplot[:self.time_pola])+list(yplot[self.time_pola+self.time_wait+1:])
            ymax=max(y_relevant)
            ymin=min(y_relevant)
            self.dynamic_ax.set_ylim([ymin,ymax])        
            self.dynamic_ax.figure.canvas.draw()
            self.labelIter.setText("iter # %i"%self.N_iter)
            


    def start_measure(self):
        self.stop.setEnabled(True)
        self.start.setEnabled(False)
        ## What happens when you click "start" ##

        #Read parameters
        self.update_value()
        # self.config_uW()
        #Sample Clock creation (On counter1)

        self.sample_clock=nidaqmx.Task()
        self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.sampling_rate)
        self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse
        self.sample_clock.start()


        
        self.signal=[True]*(self.time_pola)+[False]*(self.time_wait)+[True]*(self.N_tot-self.time_pola-self.time_wait)



        

        #Counter creation
        self.counter=nidaqmx.Task()
        self.counter.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.counter.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N_tot)
        self.sr=nidaqmx.stream_readers.CounterReader(self.counter.in_stream)

        self.counter.triggers.arm_start_trigger.dig_edge_src='/Dev1/100kHzTimebase'
        self.counter.triggers.arm_start_trigger.trig_type=nidaqmx.constants.TriggerType.DIGITAL_EDGE


        
        
        #Pulse signal creation
        self.pulsed=nidaqmx.Task()
        self.pulsed.do_channels.add_do_chan('Dev1/port0/line2')
        self.pulsed.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N_tot)

        self.pulsed.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/Ctr0ArmStartTrigger') 
        self.pulsed.write(self.signal)
        self.pulsed.start()

        


   
        self.timer.start() 

    def config_uW(self):


        resourceString4 = 'USB0::0x0AAD::0x0054::110693::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"

        rm = visa.ResourceManager()
        self.PG = rm.open_resource( resourceString4 )
        self.PG.write_termination = '\n'

        self.PG.clear()  # Clear instrument io buffers and status
        self.PG.write('*WAI')

        self.PG.write('FREQ %f MHz'%self.freq)
        self.PG.write('*WAI')

        self.PG.write('POW %f dBm'%self.puissance)
        self.PG.write('*WAI')

        self.PG.write('OUTP ON') #OFF/ON pour allumer éteindre la uW
        self.PG.write('*WAI')        

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
            self.pulsed.close()
        except :
            pass
        try :
            self.counter.close()
        except :
            pass
        try :
            self.PG.write('*RST')
            self.PG.write('*WAI')
        except :
            pass
        with nidaqmx.Task() as pulsed :
            pulsed.do_channels.add_do_chan('Dev1/port0/line2')
            pulsed.write(True)
        self.stop.setEnabled(False)
        self.start.setEnabled(True)
        
        
        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()