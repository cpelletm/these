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
            self.startpath="D:/DATA" #Default folder to save at
        
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

        self.unit=1e-5
        self.tecl=40
        self.twait=40
        self.tread=20
        self.nrepeat=10

        


     
        

        

        

        ##Creation of the graphical interface##

        self.setWindowTitle("Temps de vie")

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
        
        Vbox_droite.addWidget(self.start)
        Vbox_droite.addWidget(self.stop)
        
        #Labels on the left
        gras=QFont( "Consolas", 40, QFont.Bold)

        self.labelunit=QLabel("unité de temps (s)")
        self.labelecl=QLabel("n eclairage ")
        self.labelwait=QLabel("n wait (scan) ")   
        self.labelread=QLabel("n read (min 3)") 
        self.labelnrepeat=QLabel("n repeat ") 

        self.lectunit=QLineEdit(str(self.unit))
        self.lectecl=QLineEdit(str(self.tecl))
        self.lectwait=QLineEdit(str(self.twait))
        self.lectread=QLineEdit(str(self.tread))
        self.lectnrepeat=QLineEdit(str(self.nrepeat))
        

        Vbox_gauche.addWidget(self.labelunit)
        Vbox_gauche.addWidget(self.lectunit)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labelecl)
        Vbox_gauche.addWidget(self.lectecl)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labelwait)
        Vbox_gauche.addWidget(self.lectwait)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labelread)
        Vbox_gauche.addWidget(self.lectread)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labelnrepeat)
        Vbox_gauche.addWidget(self.lectnrepeat)

        
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

        ## Timer Setup ##

        self.timer = QTimer(self,interval=0)
        self.timer.timeout.connect(self.update_canvas)

    def update_canvas(self):       
        ##Update the plot by averaging##

        self.n_iter+=1

        #Counter creation
        self.counter=nidaqmx.Task()
        self.counter.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.counter.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N)
        self.sr=nidaqmx.stream_readers.CounterReader(self.counter.in_stream)

        self.counter.triggers.arm_start_trigger.dig_edge_src='/Dev1/100kHzTimebase'
        self.counter.triggers.arm_start_trigger.trig_type=nidaqmx.constants.TriggerType.DIGITAL_EDGE


        
        
        #Pulse signal creation
        self.pulsed=nidaqmx.Task()
        self.pulsed.do_channels.add_do_chan('Dev1/port0/line2')
        self.pulsed.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N)

        self.pulsed.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/Ctr0ArmStartTrigger') 
        self.pulsed.write(self.signal)
        self.pulsed.start()

        self.sr.read_many_sample_double(self.data,number_of_samples_per_channel=len(self.data))

        self.counter.close()
        self.pulsed.close()

        temp_rep=np.zeros(self.twait) #y for nrepeat time
        temp=np.zeros(self.twait) #y for 1 try
        for j in range(self.nrepeat) :
            data_local=self.data[j*self.N:(j+1)*self.N] #Counter for 1 sequence
            for i in range (1,self.twait+1) : #look for the values at the beginning and the end of the readout
                temp[i-1]=(data_local[int(self.tecl*i+i*(i+1)/2+self.tread*i-1)]-data_local[int(self.tecl*i+i*(i+1)/2+self.tread*(i-1))+1])/((self.tread-2)*self.unit) #I skip the first point, not sure it is worth
            temp_rep+=temp*1/self.nrepeat

        self.y_avg=self.y_avg*((self.n_iter-1)/self.n_iter)+temp_rep*1/self.n_iter
        
   
        self.dynamic_line.set_ydata(self.y_avg)
        ymax=max(self.y_avg)
        ymin=min(self.y_avg)
        self.dynamic_ax.set_ylim([ymin,ymax])  
        self.dynamic_ax.figure.canvas.draw()


    def start_measure(self):
        ## What happens when you click "start" ##
        self.stop.setEnabled(True)
        self.start.setEnabled(False)

        #Read parameters
        self.tecl=np.int(self.lectecl.text())
        self.twait=np.int(self.lectwait.text())
        self.tread=np.int(self.lectread.text())
        self.unit=np.float(self.lectunit.text())
        self.nrepeat=np.int(self.lectnrepeat.text())

        self.sampling_rate=1/self.unit

        self.N=int(self.tecl*self.twait+self.tread*self.twait+self.twait*(self.twait+1)/2)
        self.N_rep=self.N*self.nrepeat

        self.n_iter=0
        #Sample Clock creation (On counter1)

        self.sample_clock=nidaqmx.Task()
        self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.sampling_rate)
        self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse
        self.sample_clock.start()

        



        


        
        self.signal=[]
        for i in range(1,self.twait+1):
            self.signal=self.signal+self.tecl*[True]+i*[False]+self.tread*[True]
        self.signal=self.signal*self.nrepeat

        

               
        #PL buffer creation
        self.data=np.zeros(self.N_rep)
        
        #Adjust time axis
        self.t=np.arange(0,self.twait*self.unit,self.unit)
        self.dynamic_line.set_xdata(self.t)
        xmax=max(self.t)
        self.dynamic_ax.set_xlim([0,xmax])

        #Create y-axis
        self.y_avg=np.zeros(self.twait)

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