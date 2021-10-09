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

		self.f_acq=1E5
		self.t_up=100E-3
		self.t_down=100E-3
		
		self.n_up=int(self.f_acq*self.t_up)
		self.n_down=int(self.f_acq*self.t_down)


		# self.n_lect_min=0
		# self.n_lect_max=-1
		self.n_lect_min=self.n_up-100
		self.n_lect_max=self.n_up+300

		self.time_last_refresh=time.time()
		self.refresh_rate=0.1
		

		#Total number of points in the plot
		self.N=self.n_up+self.n_down



		

		##Creation of the graphical interface##

		self.setWindowTitle("Pulse EdH")

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


	






		self.ymax=0 # for the semi-autoscale, ymax needs to have a memory

		


		
		#Plot in the middle + toolbar

		self.dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
		#print(dir(self.dynamic_canvas))
		Vbox.addStretch(1)
		Vbox.addWidget(self.dynamic_canvas)
		self.addToolBar(Qt.BottomToolBarArea,
						NavigationToolbar(self.dynamic_canvas, self))


		## Matplotlib Setup ##

		self.dynamic_ax,self.tension_plot_ax= self.dynamic_canvas.figure.subplots(2)

		self.t_PL=np.linspace(0,self.t_up+self.t_down,self.N-1) 
		self.y_PL=np.zeros(self.N-1)		
		self.dynamic_line,=self.dynamic_ax.plot(self.t_PL[self.n_lect_min:self.n_lect_max], self.y_PL[self.n_lect_min:self.n_lect_max])
		self.t_V=np.linspace(0,self.t_up+self.t_down,self.N) 
		self.y_V=np.zeros(self.N)	
		self.tension_plot_line,=self.tension_plot_ax.plot(self.t_V[self.n_lect_min:self.n_lect_max], self.y_V[self.n_lect_min:self.n_lect_max])

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




		lecture=self.tension.read(self.N)    
		PL_brut=self.apd.read(self.N)

		PL=np.array([(PL_brut[i+1]-PL_brut[i])*self.f_acq for i in range(len(PL_brut)-1)])
		self.y_PL=self.y_PL*(1-1/self.repeat)+PL*(1/self.repeat)
		self.repeat+=1

		if time.time()-self.time_last_refresh>self.refresh_rate :
			self.time_last_refresh=time.time()

			self.y_V=lecture	   
			self.tension_plot_line.set_ydata(self.y_V[self.n_lect_min:self.n_lect_max])
			ymin=min(self.y_V[self.n_lect_min:self.n_lect_max])
			ymax=max(self.y_V[self.n_lect_min:self.n_lect_max])
			self.tension_plot_ax.set_ylim([ymin,ymax])   

			self.dynamic_line.set_ydata(self.y_PL[self.n_lect_min:self.n_lect_max])
			ymin=min(self.y_PL[self.n_lect_min:self.n_lect_max])
			ymax=max(self.y_PL[self.n_lect_min:self.n_lect_max])
			self.dynamic_ax.set_ylim([ymin,ymax])  

			self.dynamic_canvas.draw()

		


	def start_measure(self):
		## What happens when you click "start" ##

		self.start.setEnabled(False)
		self.stop.setEnabled(True)

		#Read integration input values


		#Sample Clock creation (On counter1)

		self.sample_clock=nidaqmx.Task()
		self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.f_acq)
		self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse


		self.apd=nidaqmx.Task()
		self.apd.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
		self.apd.timing.cfg_samp_clk_timing(self.f_acq,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N)

		self.tension=nidaqmx.Task()
		self.tension.ai_channels.add_ai_voltage_chan("Dev1/ai11")
		self.tension.timing.cfg_samp_clk_timing(self.f_acq,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N)
	
		self.TTL=nidaqmx.Task()
		self.TTL.do_channels.add_do_chan('Dev1/port0/line3')	
		self.TTL.timing.cfg_samp_clk_timing(self.f_acq,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N)



		self.signal=[True]*self.n_up+[False]*self.n_down
		self.TTL.write(self.signal)
 
		self.tension.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/do/StartTrigger')
		self.sample_clock.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/do/StartTrigger')
		self.sample_clock.start()
		self.apd.start()
		self.tension.start()  
		self.TTL.start()

		self.repeat=1


		#Start the task, then the timer
		    
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
			self.TTL.close()
		except :
			pass
		try :
			self.sample_clock.close()
		except :
			pass
		try :
			self.apd.close()
		except :
			pass	
		try  :
			with nidaqmx.Task() as TTL :
				TTL.do_channels.add_do_chan('Dev1/port0/line3')	
				TTL.write(False)
		except :
			pass

		self.stop.setEnabled(False)
		self.start.setEnabled(True)
		
		






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()