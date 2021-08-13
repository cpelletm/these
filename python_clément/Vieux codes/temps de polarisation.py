import sys
import time
import random
import os
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

        self.unit=1e-6
        self.tecl=400
        self.twait=400
        self.tread=200
        self.nrepeat=10 #number of repetition between each plot update

        


     
        

        

        

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
        
        Vbox_droite.addWidget(self.start)
        Vbox_droite.addWidget(self.stop)
        
        #Labels on the left
        gras=QFont( "Consolas", 40, QFont.Bold)

        self.labelunit=QLabel("unité de temps (s)")
        self.labelecl=QLabel("n eclairage ")
        self.labelwait=QLabel("n wait ")   
        self.labelread=QLabel("n read ") 
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
        ##Update the plot and the value of the PL ##
        self.N_iter+=1


        #Counter creation
        self.counter=nidaqmx.Task()
        self.counter.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.counter.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=self.N)
        self.sr=nidaqmx.stream_readers.CounterReader(self.counter.in_stream)

        self.counter.triggers.arm_start_trigger.dig_edge_src='/Dev1/100kHzTimebase'
        self.counter.triggers.arm_start_trigger.trig_type=nidaqmx.constants.TriggerType.DIGITAL_EDGE


        
        
        #Pulse signal creation
        self.pulsed=nidaqmx.Task()
        self.pulsed.do_channels.add_do_chan('Dev1/port0/line0')
        self.pulsed.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=self.N)

        self.pulsed.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/Ctr0ArmStartTrigger') 
        self.pulsed.write(self.signal)
        self.pulsed.start()

        self.sr.read_many_sample_double(self.data,number_of_samples_per_channel=len(self.data)) #read the N value during dt

        self.counter.close()
        self.pulsed.close()
        
        temp=np.zeros(len(self.y))
        for i in range(self.nrepeat) :
            temp+=(self.data[i*self.N_monocycle+self.tecl+self.twait+1:(i+1)*self.N_monocycle]-self.data[i*self.N_monocycle+self.tecl+self.twait:(i+1)*self.N_monocycle-1])*self.sampling_rate
        temp=temp/self.nrepeat
        self.y=temp/self.N_iter+self.y*(1-1/self.N_iter)




   
        self.dynamic_line.set_ydata(self.y)
        ymax=max(self.y)
        ymin=min(self.y[1:])
        self.dynamic_ax.set_ylim([ymin,ymax])        
        self.dynamic_ax.figure.canvas.draw()


    def start_measure(self):
        self.stop.setEnabled(True)
        self.start.setEnabled(False)
        ## What happens when you click "start" ##

        #Read parameters
        self.tecl=np.int(self.lectecl.text())
        self.twait=np.int(self.lectwait.text())
        self.tread=np.int(self.lectread.text())
        self.unit=np.float(self.lectunit.text())
        self.nrepeat=np.int(self.lectnrepeat.text())

        self.sampling_rate=1/self.unit

        
        self.N_monocycle=self.tecl+self.twait+self.tread
        self.N=self.N_monocycle*self.nrepeat

        self.data=np.zeros(self.N)


        #Sample Clock creation (On counter1)

        self.sample_clock=nidaqmx.Task()
        self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.sampling_rate)
        self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse
        self.sample_clock.start()

        



        


        
        self.signal=([True]*self.tecl+[False]*self.twait+[True]*self.tread)*self.nrepeat

        self.y=np.zeros(self.tread -1)

        self.N_iter=0


        

               

        


   
        self.timer.start() 

        
        
        

        
        



            
        

        #Adjust time axis
        self.t=np.arange(0,self.unit*(len(self.y)),self.unit)
        self.dynamic_line.set_xdata(self.t)
        xmax=max(self.t)
        self.dynamic_ax.set_xlim([0,xmax])

        
        

    def stop_measure(self):
        #Stop the measuring, clear the tasks on both counters
        try :
            self.timer.stop()
        except :
            pass
        try :
            self.task.close()
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
        self.stop.setEnabled(False)
        self.start.setEnabled(True)
        
        
        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()