import sys
import time
import random
import os



import numpy as np


from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


#This is a photon counter for the NI 6341 card when the TTL signal is plugged into ctr0/source which is on pin PFI8/P2.0/81

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

        self.stop.setEnabled(False)
        
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
                        MyToolbar(dynamic_canvas, self))


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

        self.test_signal()

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

        self.start.setEnabled(False)
        self.stop.setEnabled(True)

        #Read integration input values
        self.dt=np.float(self.textdt.text())
        self.N=np.int(self.textN.text())

        
        
        #Buffer creation
        self.data=np.zeros(2)
              
        #Adjust time axis
        self.t=np.arange(0,self.N*self.dt,self.dt)
        self.dynamic_line.set_xdata(self.t)
        xmax=max(self.t)
        self.dynamic_ax.set_xlim([0,xmax])

        


        #Start the task, then the timer
        self.timer.start() 


        #Adjust number of points
        if self.N != len(self.y) :
            self.test_signal()
            init_value=(self.data[1]-self.data[0])/self.dt
            self.y=np.ones(self.N)*init_value

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
        self.stop.setEnabled(False)
        self.start.setEnabled(True)

    def test_signal(self):
        self.data[0]=time.time()
        time.sleep(self.dt)
        self.data[1]=time.time()

        
        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()