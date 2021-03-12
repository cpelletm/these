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
import matplotlib.pyplot as plt


from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
	QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QComboBox)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure



class Photon_Counter(QMainWindow):
	def __init__(self):
		super().__init__()
		


		self.n_points=80
		self.f_uW=2.865
		self.level=15 #dBm
		self.time_acq=5E-4 #in s

		self.time_polarization=2.5E-4 #in s
		self.time_read=2.5E-4 #in s
		self.time_pulse_uW=10E-6 #in s. The pulse time might not pe precise
		self.n_min_wait=1 #n_wait = l'unité de temps d'attente (le dt entre chaque point du dark time). n_min_wait dis à combien de dt est-ce qu'on commence, parce qu'il y a des pb si le temps d'attente est plus court que la pulse uw
		#§ATTENTION : n_min_wait ne fonctionne pas pour l'instant (pb d'indices dans PL_indices). Laisser à 1

		self.refresh_rate=0.1 #Screen max refresh rate (in s), below 0.1 is probably too fast



		self.sampling_rate=5E5

		self.n_pulse=int(self.time_pulse_uW*self.sampling_rate)
		if self.n_pulse < 1 :
			print('Warning : no uW')
		self.n_pola=int(self.sampling_rate*self.time_polarization)
		self.n_read=int(self.sampling_rate*self.time_read)
		self.n_wait=int(self.time_acq/self.n_points*self.sampling_rate)
		self.n_cycle=self.n_wait*self.n_points+self.n_read+self.n_pola

		if self.n_pulse >= self.n_wait*self.n_min_wait :
			print("Pulse trop longue par rapport au premier dark time")
		


		

		##Creation of the graphical interface##

		self.setWindowTitle("TdV soustraction")

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
		self.labelf_uW=QLabel("f_uW (GHz)")
		self.lectf_uW=QLineEdit(str(self.f_uW))
		Vbox_gauche.addWidget(self.labelf_uW)
		Vbox_gauche.addWidget(self.lectf_uW)
		Vbox_gauche.addStretch(1)


		self.labellevel=QLabel("level (dBm)")
		self.lectlevel=QLineEdit(str(self.level))
		Vbox_gauche.addWidget(self.labellevel)
		Vbox_gauche.addWidget(self.lectlevel)
		Vbox_gauche.addStretch(1)

		self.labeltime_acq=QLabel("time_acq")
		self.lecttime_acq=QLineEdit(str(self.time_acq))
		Vbox_gauche.addWidget(self.labeltime_acq)
		Vbox_gauche.addWidget(self.lecttime_acq)
		Vbox_gauche.addStretch(1)

		self.labeln_points=QLabel("n_points")
		self.lectn_points=QLineEdit(str(self.n_points))
		Vbox_gauche.addWidget(self.labeln_points)
		Vbox_gauche.addWidget(self.lectn_points)


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
		self.dynamic_ax,self.direct_ax,self.pulse_ax= dynamic_canvas.figure.subplots(3)

		self.x=np.linspace(0,self.time_acq,self.n_points)
		self.y=np.zeros(self.n_points)
		self.dynamic_line,=self.dynamic_ax.plot(self.x, self.y)
		self.direct_line,=self.direct_ax.plot(self.x, self.y)
		self.pulse_line,=self.pulse_ax.plot(self.x, self.y)

  


		self.create_sequence()
		# self.plot_sequences()



			  
		#Define the buttons' action 
		
		self.start.clicked.connect(self.start_measure)
		self.stop.clicked.connect(self.stop_measure)

	def create_sequence(self):
		self.seq_aom=[]
		self.seq_switch=[]
		for i in range(1,self.n_points+1) :
			if i <= self.n_min_wait :
				i=self.n_min_wait
			self.seq_aom+=[False]*(i*self.n_wait)+[True]*(self.n_cycle-i*self.n_wait)
			self.seq_aom+=[False]*(i*self.n_wait)+[True]*(self.n_cycle-i*self.n_wait)
			self.seq_switch+=[True]*(i*self.n_wait-self.n_pulse)+[False]*self.n_pulse+[True]*(self.n_cycle-i*self.n_wait)
			self.seq_switch+=[True]*(self.n_cycle)
		self.PL_indices=[]
		for i in range(self.n_points) :
			self.PL_indices+=[[(2*i*(self.n_cycle))+i*self.n_wait+1,(2*i*(self.n_cycle))+i*self.n_wait+self.n_read+1,((2*i+1)*(self.n_cycle))+i*self.n_wait+1,((2*i+1)*(self.n_cycle))+i*self.n_wait+self.n_read+1]]

		self.n_seq=len(self.seq_aom)
		#Jprint(len(self.seq_aom),len(self.seq_switch),self.PL_indices[-1])

	def plot_sequences(self):
		x_aom=np.arange(2*self.n_points*(self.n_points+self.n_pola))/self.sampling_rate
		x_switch=np.arange(len(self.seq_switch))/self.sampling_rate_switch_uW
		for p in self.PL_indices :
			print(p)
		y_PL=np.zeros(2*self.n_points*(self.n_points+self.n_pola))


		for pair in self.PL_indices :
			y_PL[pair[0]:pair[1]]=np.ones(len(y_PL[pair[0]:pair[1]]))
			y_PL[pair[2]:pair[3]]=-np.ones(len(y_PL[pair[0]:pair[1]]))



		self.seq_aom=np.array(self.seq_aom)+0.01
		self.seq_switch=np.array(self.seq_switch)-0.01
		plt.plot(x_switch,self.seq_aom,label='AOM')
		plt.plot(x_switch,self.seq_switch,label='switch')
		plt.plot(x_aom,y_PL,label='PL')
		plt.legend()
		plt.show()


		
	def update_value(self):
		self.f_uW=np.float(self.lectf_uW.text())
		self.level=np.float(self.lectlevel.text())
		self.n_points=np.int(self.lectn_points.text())


		self.time_acq=np.float(self.lecttime_acq.text())

		self.n_pulse=int(self.time_pulse_uW*self.sampling_rate)
		if self.n_pulse < 1 :
			print('Warning : no uW')
		self.n_pola=int(self.sampling_rate*self.time_polarization)
		self.n_read=int(self.sampling_rate*self.time_read)
		self.n_wait=int(self.time_acq/self.n_points*self.sampling_rate)
		self.n_cycle=self.n_wait*self.n_points+self.n_read+self.n_pola


		self.time_last_refresh=time.time()

		self.x=np.linspace(0,self.time_acq,self.n_points)
		self.y=np.zeros(self.n_points)
		self.y2=np.zeros(self.n_points)
		self.y3=np.zeros(self.n_points)
		xmin=min(self.x)
		xmax=max(self.x)
		self.dynamic_ax.set_xlim([xmin,xmax]) 
		self.direct_ax.set_xlim([xmin,xmax]) 
		self.pulse_ax.set_xlim([xmin,xmax]) 

		self.dynamic_line.set_data(self.x,self.y)
		self.direct_line.set_data(self.x,self.y2)
		self.pulse_line.set_data(self.x,self.y3)




	def start_measure(self):
		## What happens when you click "start" ##


		self.start.setEnabled(False)
		self.stop.setEnabled(True)

		self.update_value()

		self.config_uW() #Pour une raison mysterieuse il vaut mieux le faire au début
		self.create_sequence()

		self.sample_clock=nidaqmx.Task()
		self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.sampling_rate)
		self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse


		self.apd=nidaqmx.Task()
		self.apd.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
		self.apd.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_seq)

		self.digout=nidaqmx.Task()
		self.digout.do_channels.add_do_chan('Dev1/port0/line2')
		self.digout.do_channels.add_do_chan('Dev1/port0/line3')
		self.digout.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_seq)


		self.sample_clock.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/do/StartTrigger')
 
		signal=[self.seq_aom,self.seq_switch]
		self.digout.write(signal)

		self.sample_clock.start()	
		self.apd.start()
			
		self.repeat=1.
		

		#Start the timer     
		self.timer = QTimer(self,interval=0)        
		self.timer.timeout.connect(self.take_point)

		

		self.digout.start()
		self.timer.start() 
		

		

	def take_point(self):


		lecture=self.apd.read(self.n_seq)

		PL_direct=np.array([(lecture[p[3]]-lecture[p[2]]) for p in self.PL_indices])*self.sampling_rate/self.n_read
		PL_pulse=np.array([(lecture[p[1]]-lecture[p[0]]) for p in self.PL_indices])*self.sampling_rate/self.n_read
		PL=PL_direct-PL_pulse
		
		

		if min(PL_direct)>=0 and min(PL_pulse)>=0 : #Pour éviter les reset de compteur
			self.y=self.y*(1-1/self.repeat)+PL*(1/self.repeat)
			self.y2=self.y2*(1-1/self.repeat)+PL_direct*(1/self.repeat)
			self.y3=self.y3*(1-1/self.repeat)+PL_pulse*(1/self.repeat)
			self.repeat+=1

		if time.time()-self.time_last_refresh>self.refresh_rate :
			self.dynamic_line.set_ydata(self.y)
			self.direct_line.set_data(self.x,self.y2)
			self.pulse_line.set_data(self.x,self.y3)

			ymin=min(self.y)
			ymax=max(self.y)
			self.dynamic_ax.set_ylim([ymin,ymax]) 
			ymin=min(self.y2)
			ymax=max(self.y2)
			self.direct_ax.set_ylim([ymin,ymax]) 
			ymin=min(self.y3)
			ymax=max(self.y3)
			self.pulse_ax.set_ylim([ymin,ymax]) 

			# print(len(self.dynamic_line.get_xdata()))
			# print(len(self.dynamic_line.get_ydata()))
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
			self.sample_clock.close()
		except :
			pass
		try :
			self.PG.write('*RST')
			self.PG.write('*WAI')
		except :
			pass
		try :
			self.digout.close()
			self.digout=nidaqmx.Task()
			self.digout.do_channels.add_do_chan('Dev1/port0/line3')
			self.digout.write([False])
			self.digout.close()
			self.digout=nidaqmx.Task()
			self.digout.do_channels.add_do_chan('Dev1/port0/line2')
			self.digout.write([True])
			self.digout.close()

		except :
			pass
		
		
		


		
		self.stop.setEnabled(False)
		self.start.setEnabled(True)  

	def config_uW(self):


		resourceString4 = 'USB0::0x0AAD::0x0054::110693::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"

		rm = visa.ResourceManager()
		self.PG = rm.open_resource( resourceString4 )
		self.PG.write_termination = '\n'

		self.PG.clear()  # Clear instrument io buffers and status
		self.PG.write('*WAI')

		self.PG.write('FREQ %f GHz'%self.f_uW)
		self.PG.write('*WAI')

		self.PG.write('POW %f dBm'%self.level)
		self.PG.write('*WAI')

		self.PG.write('OUTP ON') #OFF/ON pour allumer éteindre la uW
		self.PG.write('*WAI')




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
		lmax=0
		for ax in self.canvas.figure.get_axes() :
			for line in ax.get_lines() :
				if len(line._x)>lmax :
					lmax=len(line._x)

		for ax in self.canvas.figure.get_axes() :
			for line in ax.get_lines() :
				x=list(line._x)
				if len(x) < lmax :
					x+=[-1]*(lmax-len(x))
				y=list(line._y)
				if len(y) < lmax :
					y+=[-1]*(lmax-len(y))
				data+=[x]
				data+=[y]

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
