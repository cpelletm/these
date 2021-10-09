import sys
import time
import os
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
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QFileDialog)

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
            self.startpath="./" #Default folder to save at
        
        start = os.path.join(self.startpath, self.canvas.get_default_filename())
        

        fname, filter = QFileDialog.getSaveFileName(self.canvas.parent(),
                                         "Choose a filename to save to",
                                         start, "Images (*.png)")

        data=[]
        for ax in self.canvas.figure.get_axes() :
            for line in ax.get_lines() :
                data+=[line._x]
                data+=[line._y]

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



        self.sampling_rate=100
        self.step=1
        self.range=12
        self.NStep=int(self.range/self.step)
        self.timeStep=int(1.5*self.sampling_rate) # nb time bins for moving a step (Warning! just for one rising/falling edgd) 0.1deg=0.7sec; 
        self.timeZero=int(5*self.sampling_rate)
        self.timeTotal=self.NStep*self.timeStep*2+self.timeZero


     
        self.is_calibrate=False

        

        
 
        ##Creation of the graphical interface##

        self.setWindowTitle("Acqusition gonio")

        self.main = QWidget()
        self.setCentralWidget(self.main)

        layout= QHBoxLayout()
        Vbox = QVBoxLayout()
        Vbox_droite=QVBoxLayout()


        layout.addLayout(Vbox)
        layout.addLayout(Vbox_droite)
        self.main.setLayout(layout)

        #Buttons on the right
        self.stop=QPushButton('Stop')
        self.start=QPushButton('Start')

        self.start_calib=QPushButton('Start Calibration')
        self.stop_calib=QPushButton('Stop Calibration')

        self.stop_calib.setEnabled(False)
        self.start.setEnabled(False)
        self.stop.setEnabled(False)


        Vbox_droite.addWidget(self.start_calib)
        Vbox_droite.addWidget(self.stop_calib)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.start)
        Vbox_droite.addWidget(self.stop)
        

        
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
        self.stop.clicked.connect(self.stop_measure)

        self.start_calib.clicked.connect(self.start_calibrating)       
        self.stop_calib.clicked.connect(self.stop_calibrating)

        ## Timer Setup ##

        self.timer = QTimer(self,interval=0)
        self.timer.timeout.connect(self.update_canvas)

    def update_canvas(self):       
        ##Update the plot by averaging##

        self.n_iter+=1

        #Counter creation
        self.counter=nidaqmx.Task()
        self.counter.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.counter.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=self.timeTotal)
        self.sr=nidaqmx.stream_readers.CounterReader(self.counter.in_stream)

        self.counter.triggers.arm_start_trigger.dig_edge_src='/Dev1/100kHzTimebase'
        self.counter.triggers.arm_start_trigger.trig_type=nidaqmx.constants.TriggerType.DIGITAL_EDGE


        
        
        #xmoving signal creation
        self.xmoving=nidaqmx.Task()
        self.xmoving.do_channels.add_do_chan('Dev1/port0/line1')
        self.xmoving.do_channels.add_do_chan('Dev1/port0/line0')
        self.xmoving.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=self.timeTotal)
        self.xmoving.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/Ctr0ArmStartTrigger') 
        #self.xmoving.write(self.signalx1)
        self.xmoving.write([self.signalx1,self.signalx2])
        self.xmoving.start()

        self.sr.read_many_sample_double(self.data,number_of_samples_per_channel=len(self.data),timeout=nidaqmx.constants.WAIT_INFINITELY)

        self.counter.close()
        self.xmoving.close()



        
        
        
        if self.is_calibrate :
            self.y=(self.data[1:]-self.data[:-1])*self.sampling_rate/self.calib
        else :
            self.y=(self.data[1:]-self.data[:-1])*self.sampling_rate

        self.y_avg=self.y*1/self.n_iter+self.y_avg*(1-1/self.n_iter)
        self.dynamic_line.set_ydata(self.y_avg)
        ymax=max(self.y_avg)
        ymin=min(self.y_avg)
        self.dynamic_ax.set_ylim([ymin,ymax])  
        self.dynamic_ax.figure.canvas.draw()


    def start_measure(self):
        ## What happens when you click "start" ##
        if self.is_calibrate :
            self.stop.setEnabled(True)
            self.start.setEnabled(False)

        

        self.n_iter=0
        #Sample Clock creation (On counter1)

        self.sample_clock=nidaqmx.Task()
        self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.sampling_rate)
        self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse
        self.sample_clock.start()

        



        

        #Creation of signal and data buffer
        
        self.signalx1=([True]*self.timeStep+[False]*self.timeStep)*self.NStep+[False]*self.timeZero
        self.signalx2=[False]*self.timeStep*self.NStep*2+[True]*(self.timeZero-1)+[False]
        self.data=np.zeros(self.timeTotal)

        if len(self.signalx1)==len(self.signalx2) and len(self.signalx1)==len(self.data) :
            pass
        else : 
            print("Tables legnth don't match")

        


               

        
        
        #Adjust time axis
        timeUnit=1/self.sampling_rate
        length=self.timeTotal-1
        self.t=np.arange(0,length*timeUnit,timeUnit)
        self.dynamic_line.set_xdata(self.t)
        xmax=max(self.t)
        self.dynamic_ax.set_xlim([0,xmax])

        #Create y-axis
        self.y_avg=np.zeros(length)

        #Start the timer 
        self.timer.start() 

        
        
 
        

        

        
        

    def stop_measure(self):
        #Stop the measuring, clear the tasks on both counters
        if self.is_calibrate :
            self.stop.setEnabled(False)
            self.start.setEnabled(True)
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
            self.xmoving.close()
        except :
            pass

    def start_calibrating(self):
        self.is_calibrate=False
        self.stop_calib.setEnabled(True)
        self.start_calib.setEnabled(False)
        self.start_measure()

    def stop_calibrating(self):
        self.stop_calib.setEnabled(False)
        self.start_calib.setEnabled(True)
        self.stop_measure()
        self.calib=self.y_avg
        self.is_calibrate=True
        self.start.setEnabled(True)



        

        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()