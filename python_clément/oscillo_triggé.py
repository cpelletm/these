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

		self.dt=1e-4
		self.refresh_rate=0.1
		self.time_last_refresh=time.time()
		
		self.n_glissant=10

		#Total number of points in the plot
		self.N=200

		self.level=0

		

		##Creation of the graphical interface##

		self.setWindowTitle("Oscillo")

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


		self.textdt=QLineEdit('%3.2E'%(self.dt))
		self.labeldt=QLabel("dt (s) ")  
		self.textN=QLineEdit(str(self.N))
		self.labelN=QLabel("Number of points ")  
		self.labelPL=QLabel("photocounts (s-1)") 
		self.PL=QLabel()
		self.PL.setFont(gras)






		self.ymax=0 # for the semi-autoscale, ymax needs to have a memory

		Vbox_gauche.addWidget(self.labelPL)
		Vbox_gauche.addWidget(self.PL)

		self.labellevel=QLabel("level")
		self.lectlevel=QLineEdit(str(self.level))
		Vbox_gauche.addWidget(self.labellevel)
		Vbox_gauche.addWidget(self.lectlevel)
		Vbox_gauche.addStretch(1)
		Vbox_gauche.addWidget(self.labeldt)
		Vbox_gauche.addWidget(self.textdt)
		Vbox_gauche.addStretch(1)


		self.labeln_glissant=QLabel("n_glissant")
		self.lectn_glissant=QLineEdit(str(self.n_glissant))
		Vbox_gauche.addWidget(self.labeln_glissant)
		Vbox_gauche.addWidget(self.lectn_glissant)
		
		Vbox_gauche.addWidget(self.labelN)
		Vbox_gauche.addWidget(self.textN)


		
		#Plot in the middle + toolbar

		self.dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
		#print(dir(self.dynamic_canvas))
		Vbox.addStretch(1)
		Vbox.addWidget(self.dynamic_canvas)
		self.addToolBar(Qt.BottomToolBarArea,
						NavigationToolbar(self.dynamic_canvas, self))


		## Matplotlib Setup ##

		self.dynamic_ax= self.dynamic_canvas.figure.subplots()
		self.t=np.zeros(self.N+1) #Put to self.n if you want to start at 0
		self.y=np.zeros(self.N+1)
		
		self.dynamic_line,=self.dynamic_ax.plot(self.t, self.y)

		self.dynamic_ax.set_xlabel('time(s)')
		self.dynamic_ax.set_ylabel('PL(counts/s)')

		
			  
		#Define the buttons' action 
		
		self.start.clicked.connect(self.start_measure)
		self.stop.clicked.connect(self.stop_measure)

		## Timer Setup ##

		self.timer = QTimer(self,interval=0) 
		self.timer.timeout.connect(self.update_canvas)

			


	def update_canvas(self):       
		##Update the plot and the value of the PL ##




		lecture=self.tension.read(self.n_acq)    

		for i in range(self.N) :
			self.y[i]=sum(lecture[i*self.n_glissant:(i+1)*self.n_glissant])


		if time.time()-self.time_last_refresh>self.refresh_rate :
			self.time_last_refresh=time.time()
			self.PL.setText("%3.2E" % max(abs(self.y)))
	   
			self.dynamic_line.set_ydata(self.y)

			self.ymin=min(self.y)
			self.ymax=max(self.y)
			

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
		self.sampling_rate=1/self.dt*self.n_glissant

		self.n_acq=self.N*self.n_glissant

		#Sample Clock creation (On counter1)

		self.tension=nidaqmx.Task()
		self.tension.ai_channels.add_ai_voltage_chan("Dev1/ai11")
		self.tension.timing.cfg_samp_clk_timing(self.sampling_rate,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_acq)
		
 
			  
		#Adjust time axis
		self.t=np.linspace(0,self.N*self.dt,self.N)
		self.y=np.zeros(self.N)
		self.dynamic_line.set_data(self.t,self.y)
		xmax=max(self.t)
		self.dynamic_ax.set_xlim([0,xmax])

		


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
		self.stop.setEnabled(False)
		self.start.setEnabled(True)
		
		






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()