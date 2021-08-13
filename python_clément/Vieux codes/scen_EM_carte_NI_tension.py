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
		

		self.f_cycle=0.1 #ATTENTION : régler le GBF à une fréquence plus lente (genre 0.095 Hz)
		self.n_acq=10000
		self.refresh_rate=0.1

		self.n_glissant=10


		self.n_points=int(self.n_acq/self.n_glissant)
		self.n_up=self.n_points//2
		self.n_down=self.n_points-self.n_up

		self.f_acq=self.f_cycle*self.n_acq


		self.V_min=-1
		self.V_max=+1



		

		##Creation of the graphical interface##

		self.setWindowTitle("Line Scan tension")

		self.main = QWidget()
		self.setCentralWidget(self.main)

		layout= QHBoxLayout()
		Vbox = QVBoxLayout()
		Vbox_droite=QVBoxLayout()
		Vbox_gauche=QVBoxLayout()

		layout.addLayout(Vbox_gauche)
		layout.addLayout(Vbox)
		layout.addLayout(Vbox_droite)
		self.main.setLayout(layout)

		Vbox_gauche.addStretch(1)
		self.labelV_min=QLabel("V_min")
		self.lectV_min=QLineEdit(str(self.V_min))
		Vbox_gauche.addWidget(self.labelV_min)
		Vbox_gauche.addWidget(self.lectV_min)
		

		self.labelV_max=QLabel("V_max")
		self.lectV_max=QLineEdit(str(self.V_max))
		Vbox_gauche.addWidget(self.labelV_max)
		Vbox_gauche.addWidget(self.lectV_max)
		Vbox_gauche.addStretch(1)


		#Buttons on the right
		self.stop=QPushButton('Stop')
		self.start=QPushButton('Start')
		self.keep_button=QPushButton('Keep trace')
		self.clear_button=QPushButton('Clear Last Trace')
		self.normalize_cb=QCheckBox('Normalize')

		
		self.labelIter=QLabel("iter # 0")

		Vbox_droite.addWidget(self.normalize_cb)
		Vbox_droite.addStretch(1)
		Vbox_droite.addWidget(self.start)
		Vbox_droite.addWidget(self.stop)
		Vbox_droite.addStretch(1)
		Vbox_droite.addWidget(self.keep_button)
		Vbox_droite.addWidget(self.clear_button)
		Vbox_droite.addStretch(1)
		Vbox_droite.addWidget(self.labelIter)


		self.stop.setEnabled(False)
		
		
		#Plot in the middle
		dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
		Vbox.addStretch(1)
		Vbox.addWidget(dynamic_canvas)
		self.addToolBar(Qt.BottomToolBarArea,
						MyToolbar(dynamic_canvas, self))
		self.dynamic_ax = dynamic_canvas.figure.subplots()

		#♪self.t=np.linspace(0,1/self.f_cycle,self.n_points)
		self.x=np.linspace(self.V_min,self.V_max,self.n_up)
		self.y=np.zeros(self.n_up)
		self.dynamic_line,=self.dynamic_ax.plot(self.x,self.y)





			  
		#Define the buttons' action 
		
		self.start.clicked.connect(self.start_measure)
		self.stop.clicked.connect(self.stop_measure)
		self.keep_button.clicked.connect(self.keep_trace)
		self.clear_button.clicked.connect(self.clear_trace)

	def keep_trace(self):
		self.dynamic_ax.plot(self.dynamic_line._x,self.dynamic_line._y)

	def clear_trace(self):
		lines=self.dynamic_ax.get_lines()
		line=lines[-1]
		if line != self.dynamic_line :
			line.remove()
		self.dynamic_ax.figure.canvas.draw()


		

	   


	def start_measure(self):
		## What happens when you click "start" ##


		self.start.setEnabled(False)
		self.stop.setEnabled(True)

		self.V_min=np.float(self.lectV_min.text())
		self.V_max=np.float(self.lectV_max.text())

		self.time_last_refresh=time.time()

		self.x=np.linspace(self.V_min,self.V_max,self.n_up)
		self.dynamic_line.set_xdata(self.x)
		xmin=min(self.x)
		xmax=max(self.x)
		self.dynamic_ax.set_xlim([xmin,xmax]) 
		voltage_list=list(np.linspace(self.V_max,self.V_min,self.n_acq-self.n_up*self.n_glissant))+list(np.linspace(self.V_min,self.V_max,self.n_up*self.n_glissant))

		self.voltage_out=nidaqmx.Task()
		self.voltage_out.ao_channels.add_ao_voltage_chan('Dev1/ao0')
		self.voltage_out.timing.cfg_samp_clk_timing(self.f_acq,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_acq)

		self.voltage_out.write(voltage_list)


		self.tension=nidaqmx.Task()
		self.tension.ai_channels.add_ai_voltage_chan("Dev1/ai11")
		self.tension.timing.cfg_samp_clk_timing(self.f_acq,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_acq)


		self.tension.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/ao/StartTrigger')



		self.tension.start()

		
		


		
		self.repeat=1.
		self.y=np.zeros(self.n_points)
		

		#Start the timer     
		self.timer = QTimer(self,interval=0)        
		self.timer.timeout.connect(self.take_point)
		self.voltage_out.start()
		self.timer.start() 
		

		

	def take_point(self):





		PL_brut=self.tension.read(self.n_acq,timeout=nidaqmx.constants.WAIT_INFINITELY)

		PL=np.zeros(self.n_points)
		for i in range(self.n_points) :
			PL[i]=sum(PL_brut[i*self.n_glissant:(i+1)*self.n_glissant])/self.n_glissant


		



		
		
		

		self.y=self.y*(1-1/self.repeat)+PL*(1/self.repeat)
		self.repeat+=1

		if time.time()-self.time_last_refresh>self.refresh_rate :
			self.time_last_refresh=time.time()

			if self.normalize_cb.isChecked() :
				yplot=self.y/max(self.y)
			else :
				yplot=self.y
			self.dynamic_line.set_ydata(yplot[self.n_up:])
			ymin=min(yplot[self.n_up:])
			ymax=max(yplot[self.n_up:])
			self.dynamic_ax.set_ylim([ymin,ymax]) 

			# print(len(self.dynamic_line.get_xdata()))
			# print(len(self.dynamic_line.get_ydata()))
			# print(len(self.tension_plot_line.get_xdata()))
			# print(len(self.tension_plot_line.get_ydata()))
			self.dynamic_ax.figure.canvas.draw()

			self.labelIter.setText("iter # %i"%self.repeat)
			
	 

	def stop_measure(self):
		#A ameliorer en recuperant dirrectement les tasks depuis system.truc
		try :
			self.timer.stop()
		except :
			pass
		try :
			self.apd.close()
		except :
			pass
		try :
			self.voltage_out.close()
		except :
			pass
		try :
			self.tension.close()
		except :
			pass
		try :
			self.trig_gbf.close()
		except :
			pass
		try :
			with nidaqmx.Task() as task:
				task.ao_channels.add_ao_voltage_chan('Dev1/ao0')
				task.write(0)
				task.start()
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
