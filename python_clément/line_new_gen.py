import sys
import os
import time
import random
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system
import nidaqmx.constants

import thorlabs_apt as apt #LANCER PUIS FERMER KINESIS SI LE PROGRAMME PLANTE (...)


import numpy as np


from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QComboBox)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure



class Photon_Counter(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Timing Parameter ##
        #The program aquires the total number of photons at a rate defined by real_sampling_rate, but will only display an average of it every dt

        self.range=[7,12]
        self.N_scan=101 #nb of points per scan

        self.time_PL=100 #integration time in ms for the PL (for slow scan)
        self.time_line=6.7 #Time in s for a line scan (fast) (6.7 for motor 1)

        self.freq_gate=int(1E4) # Sample frequency in Hz for the APD gate

        

        ##Creation of the graphical interface##

        self.setWindowTitle("Line Scan")

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

        self.motor_choice=QComboBox()
        self.motor_choice.addItem('Motor 1')
        self.motor_choice.addItem('Motor 2')

        self.scan_type_combo=QComboBox()
        self.scan_type_combo.addItem('Fast')
        self.scan_type_combo.addItem('Slow')


        self.labelIter=QLabel("iter # 0")

        
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.start)
        Vbox_droite.addWidget(self.stop)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.labelIter)

        Vbox_gauche.addWidget(self.scan_type_combo)
        Vbox_gauche.addWidget(self.motor_choice)

        self.stop.setEnabled(False)
        
        
        #Plot in the middle
        dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
        Vbox.addStretch(1)
        Vbox.addWidget(dynamic_canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        MyToolbar(dynamic_canvas, self))
        self.dynamic_ax = dynamic_canvas.figure.subplots()

        self.x=np.linspace(self.range[0],self.range[1],self.N_scan)
        self.y=np.zeros(self.N_scan)
        self.dynamic_line,=self.dynamic_ax.plot(self.x, self.y)



              
        #Define the buttons' action 
        
        self.start.clicked.connect(self.start_measure)
        self.stop.clicked.connect(self.stop_measure)


        

       


    def measure_PL(self):

        self.gate.start()
        PL=self.counter.read()/(self.time_PL*1e-3)
        self.gate.stop()
        return(PL)

    def measure_line(self):

        self.gate.start()
        PL=np.array(self.counter.read(self.N_scan))/self.time_bin
        self.gate.stop()
        return(PL)



    def start_measure(self):
        ## What happens when you click "start" ##




        self.start.setEnabled(False)
        self.stop.setEnabled(True)

        
        self.scan_type=self.scan_type_combo.currentIndex() #0 = Fast, 1=Slow



        self.counter=nidaqmx.Task()
        self.counter.ci_channels.add_ci_pulse_width_chan('Dev1/ctr0',units=nidaqmx.constants.TimeUnits.TICKS)
        self.counter.channels.ci_ctr_timebase_src='/Dev1/PFI8'
        self.counter.start()

        if self.scan_type==0:
            self.time_bin=self.time_line/self.N_scan
            N_bin=int(self.time_bin*self.freq_gate)
            signal=(N_bin*[True]+[False])*self.N_scan
        elif self.scan_type==1:
            signal=[True]*int(self.time_PL*self.freq_gate/1000)+[False]

        self.gate=nidaqmx.Task()
        self.gate.do_channels.add_do_chan('Dev1/port0/line7')
        self.gate.timing.cfg_samp_clk_timing(self.freq_gate,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
        self.gate.write(signal)



        ml=apt.list_available_devices() #ml=[(31, 27254827), (31, 27255158)]


        self.motor_chosen=self.motor_choice.currentIndex()

        if self.motor_chosen==1 :
            self.motor = apt.Motor(ml[0][1])
        if self.motor_chosen==0 :
            self.motor = apt.Motor(ml[1][1])
        
        
        self.index=0
        self.repeat=1.
        self.y=np.zeros(self.N_scan)
        

        #Start the timer     
        self.timer = QTimer(self,interval=0)
        if self.scan_type==0 :
            self.timer.timeout.connect(self.take_line)
        elif self.scan_type==1 :
            self.timer.timeout.connect(self.take_point)
        self.dead_time=False # Pour afficher à chaque fois...    
        self.timer.start() 
        

        

    def take_point(self):

        if self.dead_time :
            self.dead_time=False
            return()

        self.motor.move_to(self.x[self.index],blocking = True)
        PL=self.measure_PL()
        self.y[self.index]=self.y[self.index]*(1-1/self.repeat)+PL*(1/self.repeat)

        self.index+=1
        if self.index>=len(self.x) :
            self.index=0
            self.repeat+=1

        self.dynamic_line.set_ydata(self.y)
        ymin=min(self.y)
        ymax=max(self.y)
        self.dynamic_ax.set_ylim([ymin,ymax]) 
        self.dynamic_ax.figure.canvas.draw()
        self.dead_time=True

        self.labelIter.setText("iter # %i"%self.repeat)
        return()

    def take_line(self):

        if self.dead_time :
            self.dead_time=False
            return()

        self.motor.move_to(0,blocking = True) 
        self.motor.move_velocity(direction=2)
        PL=self.measure_line()
        cpt=0
        while self.motor.is_in_motion :
            cpt+=1
        print ('over wait %i'% cpt)
        

        self.y=self.y*(1-1/self.repeat)+PL*(1/self.repeat)

        self.dynamic_line.set_ydata(self.y)
        ymin=min(self.y)
        ymax=max(self.y)
        self.dynamic_ax.set_ylim([ymin,ymax]) 
        self.dynamic_ax.figure.canvas.draw()
        self.dead_time=True
        self.repeat+=1
        self.labelIter.setText("iter # %i"%self.repeat)
        return()

     

    def stop_measure(self):
        #A ameliorer en recuperant dirrectement les tasks depuis system.truc
        try :
            self.timer.stop()
        except :
            pass
        try :
            self.counter.close()
        except :
            pass
        try :
            self.gate.close()
        except :
            pass
        


        
        self.stop.setEnabled(False)
        self.start.setEnabled(True)     


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

        

        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()
apt._cleanup()