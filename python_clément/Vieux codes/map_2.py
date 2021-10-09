import sys
import time
import random
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system
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

        self.dt=2 # value in s

        


        #Total number of points in the plot
        self.N=1000

        

        

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
        
        #Labels on the left
        gras=QFont( "Consolas", 40, QFont.Bold)


        self.textdt=QLineEdit(str(self.dt))
        self.labeldt=QLabel("dt (s) ")  
        

        

        Vbox_gauche.addWidget(self.labeldt)
        Vbox_gauche.addWidget(self.textdt)
        


      

              
        #Define the buttons' action 
        
        self.start.clicked.connect(self.start_measure)
        self.stop.clicked.connect(self.stop_measure)







    def keyPressEvent(self, event):

        
        if event.key() == Qt.Key_Z:
            self.measure()
            point=(self.data[1]-self.data[0])/self.dt
            self.f.write("%5.4f \t" % point)
            winsound.Beep(2500, 100)

        if event.key() == Qt.Key_Return:
            self.f.write("\n")
            winsound.Beep(2000, 200)


            


    


    def start_measure(self):
        ## What happens when you click "start" ##

        

        self.start.setEnabled(False)
        self.textdt.setEnabled(False)

        self.stop.setEnabled(True)

        qf = QFileDialog.getSaveFileName(self, 'Sava data','d:\\DATA\\',"Data files (*.txt *.csv)") # return ("path/to/file", "data type")
        self.fname=qf[0]

        self.f=open(self.fname,'w')

        #Read integration input values
        self.dt=np.float(self.textdt.text())

        #Sample Clock creation (On counter1)
        self.sample_clock=nidaqmx.Task()
        self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=1/self.dt)
        self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse
        self.sample_clock.start()

        

        




        

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
            self.f.close()
        except :
            pass
        self.stop.setEnabled(False)
        self.start.setEnabled(True)
        self.textdt.setEnabled(True)
        

    def measure(self) :

        

        
        #Task Creation
        self.task=nidaqmx.Task()
        self.task.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.task.timing.cfg_samp_clk_timing(1/self.dt,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=2)
        self.data=self.task.read(2)
        self.task.close()

        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()