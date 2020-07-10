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
		


		self.n_points=100
		self.f_uW=2.88   
		self.level=0 #dBm
		self.time_acq=1E-3 #in s

		self.time_polarization=2E-4 #in s
		self.time_read=1E-4 #in s
		self.time_pulse_uW=1E-6 #in s. The pulse time might not pe precise

		self.refresh_rate=0.1 #Screen max refresh rate (in s), below 0.1 is probably too fast


		self.sampling_rate=self.n_points/self.time_acq

		self.sampling_rate_switch_uW=((1/self.time_pulse_uW)//self.sampling_rate)*self.sampling_rate

		self.ratio_sample_clocks=int(self.sampling_rate_switch_uW//self.sampling_rate)

		self.n_pola=int(self.sampling_rate*self.time_polarization)
		self.n_read=int(self.sampling_rate*self.time_read)

		


		

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
		self.dynamic_ax= dynamic_canvas.figure.subplots()

		self.x=np.linspace(0,self.time_acq,self.n_points)
		self.y=np.zeros(self.n_points)
		self.dynamic_line,=self.dynamic_ax.plot(self.x, self.y)
  


		self.create_sequence()
		# self.plot_sequences()



			  
		#Define the buttons' action 
		
		self.start.clicked.connect(self.start_measure)
		self.stop.clicked.connect(self.stop_measure)

	def create_sequence(self):
		self.seq_aom=[]
		self.seq_switch=[]
		for i in range(1,self.n_points+1) :
			self.seq_aom+=[False]*(i*self.ratio_sample_clocks)+[True]*((self.n_points-i+self.n_pola)*self.ratio_sample_clocks)
			self.seq_aom+=[False]*(i*self.ratio_sample_clocks)+[True]*((self.n_points-i+self.n_pola)*self.ratio_sample_clocks)
			self.seq_switch+=[True]*(i*self.ratio_sample_clocks-1)+[False]+[True]*((self.n_points-i+self.n_pola)*self.ratio_sample_clocks)
			self.seq_switch+=[True]*((self.n_points+self.n_pola)*self.ratio_sample_clocks)
		self.PL_indices=[]
		for i in range(self.n_points) :
			self.PL_indices+=[[(2*i*(self.n_points+self.n_pola))+i+1,(2*i*(self.n_points+self.n_pola))+i+self.n_read+1,((2*i+1)*(self.n_points+self.n_pola))+i+1,((2*i+1)*(self.n_points+self.n_pola))+i+self.n_read+1]]

		self.n_digout=len(self.seq_switch)
		self.n_apd=2*self.n_points*(self.n_points+self.n_pola)

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

		self.sampling_rate=self.n_points/self.time_acq

		self.sampling_rate_switch_uW=((1/self.time_pulse_uW)//self.sampling_rate)*self.sampling_rate
		self.ratio_sample_clocks=int(self.sampling_rate_switch_uW//self.sampling_rate)

		self.n_pola=int(self.sampling_rate*self.time_polarization)
		self.n_read=int(self.sampling_rate*self.time_read)

		self.time_last_refresh=time.time()

		self.x=np.linspace(0,self.time_acq,self.n_points)
		self.y=np.zeros(self.n_points)
		xmin=min(self.x)
		xmax=max(self.x)
		self.dynamic_ax.set_xlim([xmin,xmax]) 

		self.dynamic_line.set_data(self.x,self.y)




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
		self.apd.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_apd)

		self.digout=nidaqmx.Task()
		self.digout.do_channels.add_do_chan('Dev1/port0/line2')
		self.digout.do_channels.add_do_chan('Dev1/port0/line3')
		self.digout.timing.cfg_samp_clk_timing(self.sampling_rate_switch_uW,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_digout)


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


		lecture=self.apd.read(self.n_apd)

		PL=np.array([(lecture[p[1]]-lecture[p[0]])-(lecture[p[3]]-lecture[p[2]]) for p in self.PL_indices])
		PL=PL*self.sampling_rate/self.n_read
		
		

		if min(PL) >= -1E8 : #Pour éviter les reset de compteur
			self.y=self.y*(1-1/self.repeat)+PL*(1/self.repeat)
			self.repeat+=1

		if time.time()-self.time_last_refresh>self.refresh_rate :
			self.dynamic_line.set_ydata(self.y)
			ymin=min(self.y)
			ymax=max(self.y)
			self.dynamic_ax.set_ylim([ymin,ymax]) 

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
