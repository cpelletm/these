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
from pipython import GCSDevice, pitools


from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
	QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QComboBox)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure



class Photon_Counter(QMainWindow):
	def __init__(self):
		super().__init__()
		

		self.n_points=1001
		self.pos_min=0
		self.pos_max=15       



		self.velocity=0.6 #max=0.65



		

		##Creation of the graphical interface##

		self.setWindowTitle("Scan platine")

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


		#Fields on the left
		self.labelpos_min=QLabel("pos_min (mm)")
		self.lectpos_min=QLineEdit(str(self.pos_min))
		Vbox_gauche.addWidget(self.labelpos_min)
		Vbox_gauche.addWidget(self.lectpos_min)
		Vbox_gauche.addStretch(1)

		self.labelpos_max=QLabel("pos_max (mm)")
		self.lectpos_max=QLineEdit(str(self.pos_max))
		Vbox_gauche.addWidget(self.labelpos_max)
		Vbox_gauche.addWidget(self.lectpos_max)
		Vbox_gauche.addStretch(1)

		self.labeln_points=QLabel("n_points")
		self.lectn_points=QLineEdit(str(self.n_points))
		Vbox_gauche.addWidget(self.labeln_points)
		Vbox_gauche.addWidget(self.lectn_points)


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
		self.dynamic_ax= dynamic_canvas.figure.subplots()

		self.x=np.zeros(100)
		self.y=np.zeros(100)
		self.dynamic_line,=self.dynamic_ax.plot(self.x, self.y)
		self.real_time_line,=self.dynamic_ax.plot(self.x, self.y, '--')
  





			  
		#Define the buttons' action 
		
		self.start.clicked.connect(self.start_measure)
		self.stop.clicked.connect(self.stop_measure)
		self.keep_button.clicked.connect(self.keep_trace)
		self.clear_button.clicked.connect(self.clear_trace)


	def keep_trace(self):
		self.dynamic_ax.plot(self.x,self.y,'--')

	def clear_trace(self):
		lines=self.dynamic_ax.get_lines()
		line=lines[-1]
		if line != self.dynamic_line :
			line.remove()
		self.dynamic_ax.figure.canvas.draw()



		
	def update_value(self):
		self.pos_min=np.float(self.lectpos_min.text())
		self.pos_max=np.float(self.lectpos_max.text())
		self.n_points=np.int(self.lectn_points.text())

		self.time_scan=(self.pos_max-self.pos_min)/self.velocity*1.1
		self.dt=self.time_scan/self.n_points
		self.sampling_rate=1/self.dt


		self.x=self.pos_max-np.linspace(0,self.time_scan*self.velocity,self.n_points-1)
		self.y=np.zeros(len(self.x))
		xmin=min(self.x)
		xmax=max(self.x)
		self.dynamic_ax.set_xlim([xmax,xmin]) 

		self.dynamic_line.set_data(self.x,self.y)
		self.real_time_line.set_data(self.x,self.y)
	   


	def start_measure(self):
		## What happens when you click "start" ##


		self.start.setEnabled(False)
		self.stop.setEnabled(True)

		self.update_value()

		self.config_pi()


		self.sample_clock=nidaqmx.Task()
		self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.sampling_rate)
		self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=self.n_points) #Else the clock sends a single pulse


		self.apd=nidaqmx.Task()
		self.apd.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
		self.apd.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_points)


		
		#self.trig_uW.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/Ctr1Source')  




		
		self.apd.start()
			
		self.repeat=1.
		

		#Start the timer     
		self.timer = QTimer(self,interval=0)        
		self.timer.timeout.connect(self.take_point)

		

			
		self.timer.start() 
		

		

	def take_point(self):

		if  not self.pi.qONT(1)[1] :
			return 0

		self.sample_clock.start()
		self.pi.MOV(1,self.pos_min)
		lecture=self.apd.read(self.n_points, timeout=self.time_scan*2)
		while not self.sample_clock.is_task_done() :
			pass #c'est con mais j'ai un messsage d'erreur sinon, parce que read s'arrete sur le front montant et il reste la dernière pulse...
		self.sample_clock.stop()



		# PL=np.array([(lecture[i+1]-lecture[i])*self.sampling_rate for i in range(len(lecture)-1)])

		lecture=np.array(lecture)
		PL=lecture[1:]-lecture[:-1]
		if self.normalize_cb.isChecked() :
			PL=PL/max(PL)
		else : 
			PL=PL*self.sampling_rate
		

		if min(PL) >= 0 : #Pour éviter les reset de compteur
			self.y=self.y*(1-1/self.repeat)+PL*(1/self.repeat)
			self.repeat+=1

		self.dynamic_line.set_ydata(self.y)
		ymin=min(self.y)
		ymax=max(self.y)
		self.dynamic_ax.set_ylim([ymin,ymax]) 

		self.real_time_line.set_ydata(PL)


		# print(len(self.dynamic_line.get_xdata()))
		# print(len(self.dynamic_line.get_ydata()))
		self.dynamic_ax.figure.canvas.draw()

		self.labelIter.setText("iter # %i"%self.repeat)

		# print(self.PG.query('SYSTem:ERRor:NEXT?'))
		# if self.repeat > 1:
		#     self.stop_measure()

		self.pi.MOV(1,self.pos_max)
		# pitools.waitontarget(self.pi, axes=1)


	 

	def config_pi(self):
		CONTROLLERNAME = 'C-863.11'  # 'C-863' will also work
		STAGES = ['M-111.1VG']
		REFMODES = ['FNL', 'FRF']
		self.pi=GCSDevice(CONTROLLERNAME)
		self.pi.ConnectUSB(serialnum='0165500259')
		pitools.startup(self.pi, stages=STAGES, refmodes=REFMODES)
		self.pi.VEL(1,self.velocity)
		self.pi.MOV(1,self.pos_max)
		pitools.waitontarget(self.pi, axes=1)

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
			self.sample_clock.close()
		except :
			pass
		try :
			self.pi.close()
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
