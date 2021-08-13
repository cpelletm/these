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
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


#This is a photon counter for the NI 6341 card when the TTL signal is plugged into ctr0/source which is on pin PFI8/P2.0/81

class Photon_Counter(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Timing Parameter ##
        #The program aquires the total number of photons at a rate defined by real_sampling_rate, but will only display an average of it every dt

        self.dt=0.03 # value in s

        


        #Total number of points in the plot
        self.N=1000

        

        

        ##Creation of the graphical interface##

        self.setWindowTitle("Photon Counter")

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


        self.textdt=QLineEdit(str(self.dt))
        self.labeldt=QLabel("dt (s) ")  
        self.textN=QLineEdit(str(self.N))
        self.labelN=QLabel("Number of points ")  
        self.labelPL=QLabel("photocounts (s-1)") 
        self.PL=QLabel()
        self.PL.setFont(gras)
        self.cbsemiscale=QCheckBox('Semi Ymax auto-scale', self)
        self.cbdownautoscale=QCheckBox('Ymin auto-scale', self)

        self.cbsemiscale.stateChanged.connect(self.Set_semi_auto_scale)
        self.cbdownautoscale.stateChanged.connect(self.Set_ymin_auto_scale)

        self.semi_auto_scale=False
        self.ymin_auto_scale=False

        self.ymax=0 # for the semi-autoscale, ymax needs to have a memory

        Vbox_gauche.addWidget(self.labelPL)
        Vbox_gauche.addWidget(self.PL)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.cbsemiscale)
        Vbox_gauche.addWidget(self.cbdownautoscale)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labeldt)
        Vbox_gauche.addWidget(self.textdt)
        Vbox_gauche.addWidget(self.labelN)
        Vbox_gauche.addWidget(self.textN)


        
        #Plot in the middle + toolbar

        dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
        Vbox.addStretch(1)
        Vbox.addWidget(dynamic_canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))


        ## Matplotlib Setup ##

        self.dynamic_ax = dynamic_canvas.figure.subplots()
        self.t=np.zeros(self.N+1) #Put to self.n if you want to start at 0
        self.y=np.zeros(self.N+1)
        
        self.dynamic_line,=self.dynamic_ax.plot(self.t, self.y)
        
              
        #Define the buttons' action 
        
        self.start.clicked.connect(self.start_measure)
        self.stop.clicked.connect(self.stop_measure)

        ## Timer Setup ##

        self.timer = QTimer(self,interval=0) 
        self.timer.timeout.connect(self.update_canvas)

        #CheckBoxes
    def Set_semi_auto_scale(self,state) :
        self.semi_auto_scale = state == Qt.Checked

    def Set_ymin_auto_scale(self,state) :
        self.ymin_auto_scale = state == Qt.Checked
            


    def update_canvas(self):       
        ##Update the plot and the value of the PL ##


        self.y=np.roll(self.y,-1) #free a space at the end of the curve

        self.sr.read_many_sample_double(self.data,number_of_samples_per_channel=len(self.data)) #read the N value during dt
        

        self.y[-1]=(self.data[1]-self.data[0])/self.dt


        self.PL.setText("%3.2E" % self.y[-1])
   
        self.dynamic_line.set_ydata(self.y)

        if self.semi_auto_scale :
            self.ymax=max(self.ymax,max(self.y))
        else : 
            self.ymax=max(self.y)

        if self.ymin_auto_scale :
            self.ymin=min(self.y)
        else :
            self.ymin=0
        
        self.dynamic_ax.set_ylim([self.ymin,self.ymax])        
        self.dynamic_ax.figure.canvas.draw()


    def start_measure(self):
        ## What happens when you click "start" ##

        #Read integration input values
        self.dt=np.float(self.textdt.text())
        self.N=np.int(self.textN.text())

        #Sample Clock creation (On counter1)

        self.sample_clock=nidaqmx.Task()
        self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=1/self.dt)
        self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse
        self.sample_clock.start()

        
        #Task Creation
        self.task=nidaqmx.Task()
        self.task.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.task.timing.cfg_samp_clk_timing(1/self.dt,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=2)
        self.sr=nidaqmx.stream_readers.CounterReader(self.task.in_stream)
        
        #Buffer creation
        self.data=np.zeros(2)
              
        #Adjust time axis
        self.t=np.arange(0,self.N*self.dt,self.dt)
        self.dynamic_line.set_xdata(self.t)
        xmax=max(self.t)
        self.dynamic_ax.set_xlim([0,xmax])

        


        #Start the task, then the timer
        self.task.start()      
        self.timer.start() 


        #Adjust number of points
        if self.N != len(self.y) :
            self.sr.read_many_sample_double(self.data,number_of_samples_per_channel=len(self.data))
            init_value=(self.data[1]-self.data[0])/self.dt
            self.y=np.ones(self.N)*init_value

    def stop_measure(self):
        #Stop the measuring, clear the tasks on both counters
        self.timer.stop()
        self.task.close()
        self.sample_clock.close()
        
        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.task.close() #just in case
app.sample_clock.close()