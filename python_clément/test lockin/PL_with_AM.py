import sys
import time
import random
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system

import numpy as np

import visa
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

        self.refresh_rate=0.1


        #Total number of points in the plot
        self.N=200
        self.frequency=2865 #MHz
        self.power=10 #dBm

        
        self.n_glissant=10
        

        ##Creation of the graphical interface##

        self.setWindowTitle("PL AM")

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
        self.ymin_auto_scale=True
        self.cbdownautoscale.setChecked(True)

        self.ymax=0 # for the semi-autoscale, ymax needs to have a memory



        Vbox_gauche.addWidget(self.labelPL)
        Vbox_gauche.addWidget(self.PL)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.cbsemiscale)
        Vbox_gauche.addWidget(self.cbdownautoscale)
        Vbox_gauche.addStretch(1)
        self.labelfrequency=QLabel("frequency (MHz)")
        self.lectfrequency=QLineEdit(str(self.frequency))
        Vbox_gauche.addWidget(self.labelfrequency)
        Vbox_gauche.addWidget(self.lectfrequency)
        self.labelpower=QLabel("power (dBm)")
        self.lectpower=QLineEdit(str(self.power))
        Vbox_gauche.addWidget(self.labelpower)
        Vbox_gauche.addWidget(self.lectpower)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labeldt)
        Vbox_gauche.addWidget(self.textdt)
        Vbox_gauche.addWidget(self.labelN)
        Vbox_gauche.addWidget(self.textN)

        self.labeln_glissant=QLabel("n_glissant (min=2)")
        self.lectn_glissant=QLineEdit(str(self.n_glissant))
        Vbox_gauche.addWidget(self.labeln_glissant)
        Vbox_gauche.addWidget(self.lectn_glissant)




        
        #Plot in the middle + toolbar

        self.dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
        #print(dir(self.dynamic_canvas))
        Vbox.addStretch(1)
        Vbox.addWidget(self.dynamic_canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        NavigationToolbar(self.dynamic_canvas, self))


        ## Matplotlib Setup ##

        self.dynamic_ax= self.dynamic_canvas.figure.subplots()
        self.t=np.zeros(self.N) #Put to self.n if you want to start at 0
        self.y=np.zeros(self.N)
        
        self.dynamic_line,=self.dynamic_ax.plot(self.t, self.y)

        self.dynamic_ax.set_xlabel('time(s)')
        self.dynamic_ax.set_ylabel('PL(counts/s)')

        
              
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

        V=self.tension.read(self.n_glissant)        

        V_avg=sum(V)/self.n_glissant
        self.y[-1]=V_avg


        if time.time()-self.time_last_refresh>self.refresh_rate :
            self.time_last_refresh=time.time()

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
            self.dynamic_canvas.draw()

        


    def start_measure(self):
        ## What happens when you click "start" ##

        self.start.setEnabled(False)
        self.stop.setEnabled(True)

        #Read integration input values
        self.dt=np.float(self.textdt.text())
        self.N=np.int(self.textN.text())
        self.n_glissant=np.int(self.lectn_glissant.text())
        
        self.frequency=float(self.lectfrequency.text())
        self.power=float(self.lectpower.text())

        self.sampling_rate=1/self.dt*self.n_glissant

        #Sample Clock creation (On counter1)

        self.config_uW()

        self.tension=nidaqmx.Task()
        self.tension.ai_channels.add_ai_voltage_chan("Dev1/ai11")
        self.tension.timing.cfg_samp_clk_timing(self.sampling_rate,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N)
        
 
              
        #Adjust time axis
        self.t=np.linspace(0,self.N*self.dt,self.N)
        self.dynamic_line.set_data(self.t,self.y)
        xmax=max(self.t)
        self.dynamic_ax.set_xlim([0,xmax])

        
        self.time_last_refresh=time.time()

        #Start the task, then the timer
        self.tension.start()      
        self.timer.start() 


    def stop_measure(self):
        #Stop the measuring, clear the tasks on both counters
        try :
            self.timer.stop()
        except :
            pass
        try :
            self.tension.close()
        except :
            pass
        try :
            self.PG.write('*RST')
            self.PG.write('*WAI')
        except :
            pass
        self.stop.setEnabled(False)
        self.start.setEnabled(True)

    def config_uW(self):

        #TCPIP0::micro-onde.phys.ens.fr::inst0::INSTR
        #USB0::0x0AAD::0x0054::110140::0::INSTR
        resourceString4 = 'TCPIP0::micro-onde.phys.ens.fr::inst0::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"

        rm = visa.ResourceManager()
        self.PG = rm.open_resource( resourceString4 )
        self.PG.write_termination = '\n'
        self.PG.timeout=8000

        self.PG.clear()  # Clear instrument io buffers and status
        self.PG.write('*WAI')
        self.PG.write('FREQ %f MHz'%self.frequency)
        self.PG.write('*WAI')
        self.PG.write('POW %f dBm'%self.power)
        self.PG.write('*WAI')
        self.PG.write(':SOUR:AM:SOUR EXT')
        self.PG.write('*WAI')
        self.PG.write(':SOUR:AM:DEPT 50')
        self.PG.write('*WAI')
        self.PG.write(':SOUR:AM:STATe ON')
        self.PG.write('*WAI')       
        self.PG.write('OUTP ON')
        self.PG.write('*WAI')
        
        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()