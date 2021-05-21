import sys
import time
import random
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system
import os

import numpy as np
import statistics


from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
	QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


#This is a photon counter for the NI 6341 card when the TTL signal is plugged into ctr0/source which is on pin PFI8/P2.0/81

class Photon_Counter(QMainWindow):
	def __init__(self):
		super().__init__()
		
		#Timing Parameter ##
		#The program aquires the total number of photons at a rate defined by real_sampling_rate, but will only display an average of it every dt

		self.dt=0.03 # value in s
		self.refresh_rate=0.5
		self.time_last_refresh=time.time()
		


		self.n_bins=40

		

		##Creation of the graphical interface##

		self.setWindowTitle("Histogramme")

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





		self.ymax=0 # for the semi-autoscale, ymax needs to have a memory

		Vbox_gauche.addStretch(1)
		Vbox_gauche.addWidget(self.labeldt)
		Vbox_gauche.addWidget(self.textdt)
		Vbox_gauche.addStretch(1)



		
		#Plot in the middle + toolbar

		self.dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
		#print(dir(self.dynamic_canvas))
		Vbox.addStretch(1)
		Vbox.addWidget(self.dynamic_canvas)
		self.addToolBar(Qt.BottomToolBarArea,
						MyToolbar(self.dynamic_canvas, self))


		## Matplotlib Setup ##

		self.dynamic_ax= self.dynamic_canvas.figure.subplots()
		self.t=np.zeros(100)
		self.y=np.zeros(100)
		self.dynamic_line,=self.dynamic_ax.plot(self.t, self.y)

		


		self.dynamic_ax.set_xlabel('Tensions (V)')



		self.normalize_cb=QCheckBox('Normalize')
		Vbox_droite.addWidget(self.normalize_cb)
			  
		#Define the buttons' action 
		
		self.start.clicked.connect(self.start_measure)
		self.stop.clicked.connect(self.stop_measure)

		## Timer Setup ##

		self.timer = QTimer(self,interval=0) 
		self.timer.timeout.connect(self.update_canvas)

		#CheckBoxes
			


	def update_canvas(self):       
		##Update the plot and the value of the PL ##



		lecture=self.tension.read(self.n_per_measure)        

		self.data=self.data+lecture

		if self.normalize_cb.isChecked() :
			pass

			
		

		if time.time()-self.time_last_refresh>self.refresh_rate :
			self.time_last_refresh=time.time()
			
			hist=np.histogram(x,bins=self.n_bins,density=True)
			self.dynamic_ax.hist(self.x,bins=self.n_bins,density=True,histtype='step')
			m=statistics.mean(self.x)
			sigma=statistics.pstdev(self.x)
			t=np.linspace(m-5*sigma,m+5*sigma,200)
			y=1/(sigma*np.sqrt(2*np.pi))*np.exp(-0.5*((t-m)/sigma)**2)
			self.dynamic_ax.plot(t,y,label='mu=%4.3e ; sigma=%4.3e'%(m,sigma))
			self.dynamic_ax.legend()

			xmax=max(self.x)
			xmin=min(self.x)
			self.dynamic_ax.set_xlim([xmin,xmax])
			  
			self.dynamic_canvas.draw()

		


	def start_measure(self):
		## What happens when you click "start" ##

		self.start.setEnabled(False)
		self.stop.setEnabled(True)

		#Read integration input values
		self.dt=np.float(self.textdt.text())
		self.n_per_measure=int(self.refresh_rate/self.dt)+1
		self.sampling_rate=1/self.dt

		#Sample Clock creation (On counter1)

		self.tension=nidaqmx.Task()
		self.tension.ai_channels.add_ai_voltage_chan("Dev1/ai11")
		self.tension.timing.cfg_samp_clk_timing(self.sampling_rate,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_per_measure)
		
 
		self.data=[]

		

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