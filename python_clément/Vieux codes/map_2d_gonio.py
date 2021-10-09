import sys
import time
import random
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system
import nidaqmx.constants
import winsound

import numpy as np


from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


#Manual map in theta/phi. Use 'z' to take a point and 'return' to make a new line
class Photon_Counter(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Timing Parameter ##
        #The program aquires the total number of photons at a rate defined by real_sampling_rate, but will only display an average of it every dt

        self.sampling_rate=10
        self.step=1
        self.range=12
        self.NStep=int(self.range/self.step)
        self.timeStep=int(3*self.sampling_rate) # nb time bins for moving a step 
        self.timeZero=10 #time ine secondss

        

        

        ##Creation of the graphical interface##

        self.setWindowTitle("Map 2d")

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

        self.stop.setEnabled(False)
        
        
        #Plot in the middle
        dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
        Vbox.addStretch(1)
        Vbox.addWidget(dynamic_canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))
        self.dynamic_ax = dynamic_canvas.figure.subplots()

        self.thetaAxis=np.linspace(0,self.range,self.NStep+1)
        self.xy=np.zeros((self.NStep,self.NStep))
        self.c=self.dynamic_ax.pcolor(self.thetaAxis,self.thetaAxis,self.xy)
        self.fig=self.dynamic_ax.get_figure()
        self.cb=self.fig.colorbar(self.c,ax=self.dynamic_ax)



              
        #Define the buttons' action 
        
        self.start.clicked.connect(self.start_measure)
        self.stop.clicked.connect(self.stop_measure)


        self.timer = QTimer(self,interval=0)
        self.timer.timeout.connect(self.take_point)
       


    


    def start_measure(self):
        ## What happens when you click "start" ##

        self.nrow=0
        self.ncol=0


        self.start.setEnabled(False)
        self.stop.setEnabled(True)

        qf = QFileDialog.getSaveFileName(self, 'Sava data','./',"Data files (*.txt *.csv)") # return ("path/to/file", "data type")
        self.fname=qf[0]

        self.f=open(self.fname,'w')


        #Sample Clock creation (On counter1)
        self.sample_clock=nidaqmx.Task()
        self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.sampling_rate)
        self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse
        self.sample_clock.start()

        self.counter=nidaqmx.Task()
        self.counter.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.counter.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=100*self.timeStep)
        self.sr=nidaqmx.stream_readers.CounterReader(self.counter.in_stream)

        self.xStep=nidaqmx.Task()
        self.xStep.do_channels.add_do_chan('Dev1/port0/line1')
        self.xStep.start()

        self.xHome=nidaqmx.Task()
        self.xHome.do_channels.add_do_chan('Dev1/port0/line0')
        self.xHome.start()

        self.yStep=nidaqmx.Task()
        self.yStep.do_channels.add_do_chan('Dev1/port0/line2')
        self.yStep.start()



        self.pulse=[True]+[False]
        self.data=np.zeros(self.timeStep)

        #Start the timer 
        self.counter.start()
        self.timer.start() 


        

    def take_point(self):

        self.xStep.write(self.pulse)
        self.counter.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)
        self.sr.read_many_sample_double(self.data,number_of_samples_per_channel=len(self.data))
        if self.data[-1]-self.data[0]>0 : #Le compteur peut déborder de temps en temps 
            PL=(self.data[-1]-self.data[0])/(len(self.data)-1)*self.sampling_rate
        else :
            self.sr.read_many_sample_double(self.data,number_of_samples_per_channel=len(self.data))
            PL=(self.data[-1]-self.data[0])/(len(self.data)-1)*self.sampling_rate
        self.f.write("%5.4E \t"%(PL))

        if self.ncol==0 and self.nrow==0 :
            self.xy=np.ones((self.NStep,self.NStep))*PL

        self.xy[self.ncol,self.nrow]=PL
        self.c=self.dynamic_ax.pcolor(self.thetaAxis,self.thetaAxis,self.xy)
        self.cb.update_normal(self.c)
        self.fig.canvas.draw()


        self.ncol+=1

        if self.ncol==self.NStep :
            self.ncol=0
            self.nrow+=1
            self.xHome.write(self.pulse)
            self.yStep.write(self.pulse)
            self.f.write('\n')
            poubelle=np.zeros(int(self.timeZero*self.sampling_rate))
            self.counter.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)
            self.sr.read_many_sample_double(poubelle,number_of_samples_per_channel=len(poubelle))
        if self.nrow==self.NStep :
            self.stop_measure()
        

        






        

    def stop_measure(self):
        #Stop the measuring, clear the tasks on both counters
        try :
            self.timer.stop()
        except :
            pass
        try :
            self.xStep.close()
        except :
            pass
        try :
            self.xHome.close()
        except :
            pass  
        try :
            self.yStep.close()
        except :
            pass 
        try :
            self.counter.close()
        except :
            pass
        try :
            self.sample_clock.close()
        except :
            pass
        try :
            self.f.close()
        except :
            pass
        self.stop.setEnabled(False)
        self.start.setEnabled(True)

        namefig=self.fname[:-4]        
        self.fig.canvas.draw()
        self.fig.savefig(namefig)


        

        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()