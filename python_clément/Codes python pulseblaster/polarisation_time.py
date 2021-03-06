import sys
import os
from subprocess import check_output
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
		

		self.dt='10 us'
		self.n_points=501
		self.f=2870 #MHz
		self.level=0 #dBm

		self.refresh_rate=0.1

		for s in self.dt.split() :
			try :
				self.dt_val=float(s)
			except :
				self.dt_unit=s
		if self.dt_unit=='ms' :
			self.dt_val=self.dt_val*1e-3
		if self.dt_unit=='us' :
			self.dt_val=self.dt_val*1e-6
		if self.dt_unit=='ns' :
			self.dt_val=self.dt_val*1e-9
		##Creation of the graphical interface##

		self.setWindowTitle("Polarisation time")

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
		self.choice_menu=QComboBox()
		self.choice_menu.addItem('Micro Wave')
		self.choice_menu.addItem('AOM')
		Vbox_gauche.addWidget(self.choice_menu)
		Vbox_gauche.addStretch(1)


		self.labelf=QLabel("f (MHz)")
		self.lectf=QLineEdit(str(self.f))
		Vbox_gauche.addWidget(self.labelf)
		Vbox_gauche.addWidget(self.lectf)
		Vbox_gauche.addStretch(1)


		self.labellevel=QLabel("level (dBm)")
		self.lectlevel=QLineEdit(str(self.level))
		Vbox_gauche.addWidget(self.labellevel)
		Vbox_gauche.addWidget(self.lectlevel)
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

		self.x=np.linspace(0,self.dt_val*self.n_points,self.n_points-1)
		self.y=np.zeros(self.n_points-1)
		self.dynamic_line,=self.dynamic_ax.plot(self.x, self.y)
		self.dynamic_ax.set_xlabel('time (s)')
  





			  
		#Define the buttons' action 
		
		self.start.clicked.connect(lambda : self.start_measure()) #De facon très étrange, sans la lambda fonction il me change initial en False...
		self.stop.clicked.connect(self.stop_measure)
		self.keep_button.clicked.connect(self.keep_trace)
		self.clear_button.clicked.connect(self.clear_trace)

	def keep_trace(self):
		self.dynamic_ax.plot(self.x,self.y)

	def clear_trace(self):
		lines=self.dynamic_ax.get_lines()
		line=lines[-1]
		if line != self.dynamic_line :
			line.remove()
		self.dynamic_ax.figure.canvas.draw()



		
	def update_value(self):
		self.f=np.float(self.lectf.text())
		self.level=np.float(self.lectlevel.text())
		self.n_points=np.int(self.lectn_points.text())

		self.sampling_rate=1/self.dt_val

		self.x=np.linspace(0,self.dt_val*self.n_points,self.n_points-1)
		self.y=np.zeros(self.n_points-1)
		xmin=min(self.x)
		xmax=max(self.x)
		self.dynamic_ax.set_xlim([xmin,xmax]) 

		self.dynamic_line.set_data(self.x,self.y)
	   


	def start_measure(self,initial=True):
		## What happens when you click "start" ##

		if initial :		
			self.update_value()
			self.repeat=1.

		self.start.setEnabled(False)
		self.stop.setEnabled(True)
		self.time_last_refresh=time.time()

		self.config_uW() #Pour une raison mysterieuse il vaut mieux le faire au début

		self.time_last_refresh=time.time()

		def t_pola(dt,n_points) :
			with open('PB_instructions.txt','w') as f:
				for i in range(n_points):
					if i == 0:
						f.write('label : ')
					else : 
						f.write('\t')
					if i < n_points/2 :
						if self.choice_menu.currentIndex()==0 :
							f.write('0b 1110, 20 ns\n')
							f.write('\t0b 1100, '+dt)
						if self.choice_menu.currentIndex()==1 :
							f.write('0b 0110, 20 ns\n')
							f.write('\t0b 0100, '+dt)
					else :
						if self.choice_menu.currentIndex()==0 :
							f.write('0b 0110, 20 ns\n')
							f.write('\t0b 0100, '+dt)
						if self.choice_menu.currentIndex()==1 :
							f.write('0b 0010, 20 ns\n')
							f.write('\t0b 0000, '+dt)
					if i==n_points-1:
						f.write(', branch, label')
					else :
						f.write('\n')

		t_pola(self.dt,self.n_points)
		check_output('spbicl load pb_instructions.txt 500.0')



		self.apd=nidaqmx.Task()
		self.apd.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
		self.apd.timing.cfg_samp_clk_timing(1E8,source='/Dev1/PFI9',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_points)


		self.apd.start()
			

		

		#Start the timer     
		self.timer = QTimer(self,interval=0)        
		self.timer.timeout.connect(self.measure)
		self.timer.start()

		check_output('spbicl start')
		
		
	def measure(self):
		try :
			self.take_point()
		except :
			self.stop_measure()
			self.start_measure(initial=False)
		

	def take_point(self):


		lecture=self.apd.read(self.n_points)


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


		if time.time()-self.time_last_refresh>self.refresh_rate :
			self.dynamic_line.set_ydata(self.y)
			if self.choice_menu.currentIndex()==0 :				
				ymin=min(self.y)
				ymax=max(self.y)
			if self.choice_menu.currentIndex()==1 :				
				ymin=min(self.y[1:self.n_points//2-1])
				ymax=max(self.y[1:self.n_points//2-1])
			self.dynamic_ax.set_ylim([ymin,ymax]) 

			self.dynamic_ax.figure.canvas.draw()

			self.labelIter.setText("iter # %i"%self.repeat)
			self.time_last_refresh=time.time()
	 

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
			self.PG.write('*RST')
			self.PG.write('*WAI')
		except :
			pass
		try :
			def AOM_on():
				with open('PB_instructions.txt','w') as f:
					f.write('label: 0b 0100, 100 ms, branch, label')

			AOM_on()
			check_output('spbicl load pb_instructions.txt 500.0')
			check_output('spbicl start')
		except :
			pass
		
		
		


		
		self.stop.setEnabled(False)
		self.start.setEnabled(True)  

	def config_uW(self):
		resourceString4 = 'TCPIP0::micro-onde.phys.ens.fr::inst0::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"

		rm = visa.ResourceManager()
		self.PG = rm.open_resource( resourceString4 )
		self.PG.write_termination = '\n'

		self.PG.clear()  # Clear instrument io buffers and status
		self.PG.write('*WAI')
		self.PG.write('FREQ %f MHz'%self.f)
		self.PG.write('*WAI')
		self.PG.write('POW %f dBm'%self.level)
		self.PG.write('*WAI')
		self.PG.write('OUTP ON')
		self.PG.write('*WAI')






class MyToolbar(NavigationToolbar): #Modification of the toolbar to save data with the plot
	
	def save_figure(self, *args): #Requires os and QFileDialog from PyQt5.QtWidgets

		try : #Test if there is a previous path saved
			if self.startpath :
				pass
		except :
			self.startpath="D:" #Default folder to save at
		
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
