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


import visa
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

        self.N_scan=201 #nb of points per scan
        self.Vmin=0 #V
        self.Vmax=1 #V

        self.Imax=1 #A
        self.N_iter_max=100

        self.time_scan=1.1 #s
        self.time_rampe=1 #s, doit être un multiple de 1s pour une raison mysterieuse

        self.sampling_rate=self.N_scan/self.time_scan



        

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


        #Fields on the left
        self.labelVmin=QLabel("V min (V)")
        self.labelVmax=QLabel("V max (V)")
        self.labelNscan=QLabel("Number of points")

        self.lectVmin=QLineEdit(str(self.Vmin))
        self.lectVmin.setEnabled(False)
        self.lectVmax=QLineEdit(str(self.Vmax))
        self.lectNscan=QLineEdit(str(self.N_scan))

        Vbox_gauche.addStretch(3)
        Vbox_gauche.addWidget(self.labelVmin)
        Vbox_gauche.addWidget(self.lectVmin)
        Vbox_gauche.addWidget(self.labelVmax)
        Vbox_gauche.addWidget(self.lectVmax)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labelNscan)
        Vbox_gauche.addWidget(self.lectNscan)
        Vbox_gauche.addStretch(3)


        #Buttons on the right
        self.stop=QPushButton('Stop')
        self.start=QPushButton('Start')

        
        self.labelIter=QLabel("iter # 0")

        
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.start)
        Vbox_droite.addWidget(self.stop)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.labelIter)


        self.stop.setEnabled(False)
        
        
        #Plot in the middle
        dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
        Vbox.addStretch(1)
        Vbox.addWidget(dynamic_canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        MyToolbar(dynamic_canvas, self))
        self.dynamic_ax,self.tension_plot_ax = dynamic_canvas.figure.subplots(2)

        self.x=np.zeros(self.N_scan)
        self.y=np.zeros(self.N_scan)
        self.dynamic_line,=self.dynamic_ax.plot(self.x, self.y)
        self.tension_plot_line,=self.tension_plot_ax.plot(self.x, self.y)





              
        #Define the buttons' action 
        
        self.start.clicked.connect(self.start_measure)
        self.stop.clicked.connect(self.stop_measure)


        

       


    def start_measure(self):
        ## What happens when you click "start" ##


        self.start.setEnabled(False)
        self.stop.setEnabled(True)

        self.N_scan=np.int(self.lectNscan.text())
        self.Vmax=np.float(self.lectVmax.text())
        self.Vmin=np.float(self.lectVmin.text())

        self.PLS=[[]]*self.N_scan

        self.t=np.linspace(0,self.time_scan,self.N_scan)
        self.V=np.linspace(0,self.Vmax,self.N_scan)
        self.y= np.zeros(self.N_scan)

        self.dynamic_line.set_data(self.V,self.y)
        self.tension_plot_line.set_data(self.t,self.y)


        marge=(self.Vmax-self.Vmin)*0.05
        self.tension_plot_ax.set_ylim([self.Vmin-marge,self.Vmax+marge])
        self.tension_plot_ax.set_xlim([0,self.time_scan])
        self.dynamic_ax.set_xlim([self.Vmin-marge,self.Vmax+marge])

        self.sampling_rate=self.N_scan/self.time_scan


        
        self.sample_clock=nidaqmx.Task()
        self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.sampling_rate)
        self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse
        self.sample_clock.start()

        self.counter=nidaqmx.Task()
        self.counter.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.counter.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N_scan+1)

        self.tension=nidaqmx.Task()
        self.tension.ai_channels.add_ai_voltage_chan("Dev1/ai11")
        self.tension.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N_scan+1)
        

        


        resourceString4 = 'USB0::0x0AAD::0x0197::5601.3800k03-101213::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"
        rm = visa.ResourceManager()
        self.PG = rm.open_resource( resourceString4 )
        self.PG.write_termination = '\n'
        self.PG.clear()  # Clear instrument io buffers and status
        self.PG.write('OUTP:GEN 0')
        self.PG.write('*WAI')



        
        self.repeat=1.
        self.y=np.zeros(self.N_scan)
        

        #Start the timer     
        self.timer = QTimer(self,interval=0)        
        self.timer.timeout.connect(self.take_point)
        self.counter.start()
        self.tension.start()
        self.timer.start() 
        

        

    def take_point(self):

        if self.repeat>=self.N_iter_max :
            self.stop_measure()
            return(0)

        self.PG.write('INST 1')
        self.PG.write('*WAI')
        self.PG.write('VOLTage:RAMP ON')
        self.PG.write('*WAI')
        self.PG.write('VOLTage:EASYramp:TIME %f'% self.time_rampe)#le temps est en secondes et j'arrive pas à faire 0.1 sec...
        self.PG.write('*WAI')
        self.PG.write('OUTP:SEL 1')
        self.PG.write('*WAI')
        self.PG.write('APPLY "%f,%f"' % (self.Vmax,self.Imax))
        self.PG.write('*WAI')        
        

        self.PG.write('OUTP:GEN 1')
        self.PG.write('*WAI')

        time.sleep(1.1) #♣le temps de la rampe
        self.PG.write('OUTP:GEN 0')
        self.PG.write('*WAI')
        time.sleep(0.5) #le temps que le générateur se remette à 0

        lecture=self.counter.read(self.N_scan+1)
        tensions=self.tension.read(self.N_scan) #piquets intervalles etc 

        self.counter.read(nidaqmx.constants.READ_ALL_AVAILABLE)#clears the buffer
        self.tension.read(nidaqmx.constants.READ_ALL_AVAILABLE)#clears the buffer

        PL=np.array([(lecture[i+1]-lecture[i])*self.sampling_rate for i in range(len(lecture)-1)])

        for i in range(self.N_scan) :
            v=tensions[i]
            j=int((self.N_scan-1)*v/self.Vmax)
            if j >= self.N_scan :
                print('tension trop grande')
                break
            if PL[i] > 0 :
                self.PLS[j]=self.PLS[j]+[PL[i]]

        for i in range(self.N_scan):
            if len(self.PLS[i]) >0 :
                self.y[i]=sum(self.PLS[i])/len(self.PLS[i])

        
        


        self.tension_plot_line.set_ydata(tensions) 
        
        

        
                

        self.repeat+=1

        self.dynamic_line.set_ydata(self.y)
        ymin=min(v for v in self.y if v!=0)
        ymax=max(self.y)
        self.dynamic_ax.set_ylim([ymin,ymax]) 
        self.dynamic_ax.figure.canvas.draw()

        self.labelIter.setText("iter # %i"%self.repeat)
     

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
            self.sample_clock.close()
        except :
            pass
        try :
            self.tension.close()
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

        

        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()
