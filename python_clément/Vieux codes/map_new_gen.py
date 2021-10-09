import sys
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

        self.xrange=[0,12]
        self.yrange=[0,10]
        self.n_pxl_x=49
        self.n_pxl_y=11

        self.time_PL=300 #integration time in ms for the PL (for slow scan)
        self.time_line=(self.xrange[1]-self.xrange[0])/2 +0.6 #Time in s for a line scan (fast) (0.3 pour 13 points, 0.6 pour 49 points)

        self.freq_gate=int(1E4) # Sample frequency in Hz for the APD gate

        self.repeat=True

        

        ##Creation of the graphical interface##

        self.setWindowTitle("Map 2d usb")

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
        self.scan_type_combo=QComboBox()
        self.scan_type_combo.addItem('Fast')
        self.scan_type_combo.addItem('Slow')
        
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.start)
        Vbox_droite.addWidget(self.stop)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.labelIter)

        Vbox_gauche.addWidget(self.scan_type_combo)

        self.stop.setEnabled(False)
        
        
        #Plot in the middle
        dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
        Vbox.addStretch(1)
        Vbox.addWidget(dynamic_canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))
        self.dynamic_ax = dynamic_canvas.figure.subplots()

        self.thetaAxis=np.linspace(self.xrange[0],self.xrange[1],self.n_pxl_x+1)
        self.phiAxis=np.linspace(self.yrange[0],self.yrange[1],self.n_pxl_y+1)
        self.xy=np.zeros((self.n_pxl_x,self.n_pxl_y))
        self.c=self.dynamic_ax.pcolormesh(self.phiAxis,self.thetaAxis,self.xy)
        self.fig=self.dynamic_ax.get_figure()
        self.cb=self.fig.colorbar(self.c,ax=self.dynamic_ax)



              
        #Define the buttons' action 
        
        self.start.clicked.connect(self.start_measure)
        self.stop.clicked.connect(self.stop_measure)


         


       


    def measure_PL(self):

        self.gate.start()
        PL=self.counter.read()/(self.time_PL*1e-3)
        self.gate.stop()
        return(PL)



    def start_measure(self):
        ## What happens when you click "start" ##




        

        self.scan_type=self.scan_type_combo.currentIndex() #0 = Fast, 1=Slow


        qf = QFileDialog.getSaveFileName(self, 'Sava data','D:/DATA',"Data files (*.txt *.csv)") # return ("path/to/file", "data type")
        self.fname=qf[0]
        if not self.fname :
            return 0

        self.start.setEnabled(False)
        self.stop.setEnabled(True)

        self.f=open(self.fname,'w')

        self.n_iter=1.


        self.counter=nidaqmx.Task()
        self.counter.ci_channels.add_ci_pulse_width_chan('Dev1/ctr0',units=nidaqmx.constants.TimeUnits.TICKS)
        self.counter.channels.ci_ctr_timebase_src='/Dev1/PFI8'
        self.counter.start()

        if self.scan_type==0:
            self.time_bin=self.time_line/self.n_pxl_x
            N_bin=int(self.time_bin*self.freq_gate)
            signal=(N_bin*[True]+[False])*self.n_pxl_x
        elif self.scan_type==1:
            signal=[True]*int(self.time_PL*self.freq_gate/1000)+[False]

        self.gate=nidaqmx.Task()
        self.gate.do_channels.add_do_chan('Dev1/port0/line7')
        self.gate.timing.cfg_samp_clk_timing(self.freq_gate,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
        self.gate.write(signal)

        if self.scan_type==0:
            PL_line=self.measure_line()
            PL=sum(PL_line)/len(PL_line)
        elif self.scan_type==1:
            PL=self.measure_PL()
        self.xy=np.ones((self.n_pxl_x,self.n_pxl_y))*PL


        ml=apt.list_available_devices() #ml=[(31, 27254827), (31, 27255158)]

        self.motorX = apt.Motor(ml[1][1])
        self.motorY = apt.Motor(ml[0][1])
        
        self.x_list=np.linspace(self.xrange[0],self.xrange[1],self.n_pxl_x)
        self.y_list=np.linspace(self.yrange[0],self.yrange[1],self.n_pxl_y)

        self.x_index=0
        self.y_index=0

        self.motorX.move_to(self.x_list[self.x_index],blocking = True)
        self.motorY.move_to(self.y_list[self.y_index],blocking = True)

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

        
        self.motorX.move_to(self.x_list[self.x_index],blocking = True)
        PL=self.measure_PL()
        self.xy[self.x_index,self.y_index]=PL*(1/self.n_iter)+self.xy[self.x_index,self.y_index]*(1-1/self.n_iter)
        self.f.write('%4.3E \t'%PL)
        self.x_index+=1

        if self.x_index==len(self.x_list):
            if self.y_index==len(self.y_list)-1:
                if self.repeat :
                    self.x_index=0
                    self.y_index=0
                    self.motorY.move_to(self.y_list[self.y_index],blocking = True)
                    self.motorX.move_to(self.x_list[self.x_index],blocking = True)
                    self.n_iter+=1
                    self.f.write('\n\n\n')
                else :
                    self.stop_measure()
            else :
                self.x_index=0
                self.y_index+=1
                self.motorY.move_to(self.y_list[self.y_index],blocking = True)
                self.motorX.move_to(self.x_list[self.x_index],blocking = True)
                self.f.write('\n')


        
        self.c=self.dynamic_ax.pcolormesh(self.phiAxis,self.thetaAxis,self.xy)
        self.cb.update_normal(self.c)
        self.fig.canvas.draw()
        self.dead_time=True

        self.labelIter.setText("iter # %i"%self.n_iter)
        return()


    def measure_line(self):

        self.gate.start()
        PL=np.array(self.counter.read(self.n_pxl_x))/self.time_bin
        self.gate.stop()
        return(PL)

    def take_line(self):

        if self.dead_time :
            self.dead_time=False
            return()
        cpt=0
        while self.motorX.is_in_motion :
            cpt+=1
        print ('over wait %i'% cpt)
        self.motorY.move_to(self.y_list[self.y_index],blocking = False)# gain de 0.1s au moins
        self.motorX.move_to(self.xrange[0],blocking = True) 
        self.motorX.move_to(self.xrange[-1],blocking = False)
        PL=self.measure_line()
        

        self.xy[:,self.y_index]=self.xy[:,self.y_index]*(1-1/self.n_iter)+PL*(1/self.n_iter)

        for v in PL :
            self.f.write('%4.3E \t'%v)
        self.f.write('\n')

        self.y_index+=1
        if self.y_index==len(self.y_list):
            if self.repeat :
                self.y_index=0
                self.n_iter+=1
                self.f.write('\n\n\n')
                self.fig.canvas.draw()
                namefig=self.fname[:-4]        
                self.fig.canvas.draw()
                self.fig.savefig(namefig)
            else :
                self.stop_measure()

        self.c=self.dynamic_ax.pcolormesh(self.phiAxis,self.thetaAxis,self.xy)
        self.cb.update_normal(self.c)
        self.fig.canvas.draw()
        self.dead_time=True
        self.repeat+=1
        self.labelIter.setText("iter # %i"%self.n_iter)
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
        try :
            self.f.write('\n\n\n')
            for i in range(len(self.xy[:,0])):
                for j in range (len(self.xy[0,:])):
                    self.f.write('%4.3E \t'%self.xy[i,j])
                self.f.write('\n')
            self.f.close()
        except :
            pass

        self.stop.setEnabled(False)
        self.start.setEnabled(True)      
        self.fig.canvas.draw()
        namefig=self.fname[:-4]        
        self.fig.canvas.draw()
        self.fig.savefig(namefig)

        

        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()
apt._cleanup()