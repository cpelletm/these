import sys
import os
from subprocess import check_output,call
import time
import random
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system
import nidaqmx.constants

import serial
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
		



		self.n_echo_per_point=10
		self.n_points=201
		self.f_min=500 #MHz
		self.f_max=700
		self.level_uW_2=18 #dBm


		self.freq_list=np.linspace(self.f_min,self.f_max,self.n_points)


		self.t_echo='400 ns'
		self.t_ecl='60 us'
		self.t_lect='60 us'
		self.f=2359 #MHz
		self.level_uW_1=20 #dBm

		self.t_lect_val=self.value_s(self.t_lect)

		self.pulse_pi='180 ns'
		self.pulse_pi_sur_2='90 ns'

		

		##Creation of the graphical interface##

		self.setWindowTitle("DEER uW 2")

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
		self.labelf_min=QLabel("f_min (MHz)")
		self.lectf_min=QLineEdit(str(self.f_min))
		Vbox_gauche.addWidget(self.labelf_min)
		Vbox_gauche.addWidget(self.lectf_min)
		Vbox_gauche.addStretch(1)

		self.labelf_max=QLabel("f_max (MHz)")
		self.lectf_max=QLineEdit(str(self.f_max))
		Vbox_gauche.addWidget(self.labelf_max)
		Vbox_gauche.addWidget(self.lectf_max)
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


		self.x=self.freq_list
		self.y=np.zeros(self.n_points)
		self.dynamic_line,=self.dynamic_ax.plot(self.x, self.y)
  





			  
		#Define the buttons' action 
		
		self.start.clicked.connect(self.start_measure)
		self.stop.clicked.connect(self.stop_measure)
		self.keep_button.clicked.connect(self.keep_trace)
		self.clear_button.clicked.connect(self.clear_trace)

	def value_s(self,pb_time): #give the value of a pulse blaster instruction time in s.
		for s in pb_time.split() :
			try :
				pb_time_val=float(s)
			except :
				pb_time_unit=s
		if pb_time_unit=='ms' :
			pb_time_val=pb_time_val*1e-3
		if pb_time_unit=='us' :
			pb_time_val=pb_time_val*1e-6
		if pb_time_unit=='ns' :
			pb_time_val=pb_time_val*1e-9
		return(pb_time_val)

	def keep_trace(self):
		self.dynamic_ax.plot(self.x,self.y)

	def clear_trace(self):
		lines=self.dynamic_ax.get_lines()
		line=lines[-1]
		if line != self.dynamic_line :
			line.remove()
		self.dynamic_ax.figure.canvas.draw()



		
	def update_value(self):
		self.f_min=np.float(self.lectf_min.text())
		self.f_max=np.float(self.lectf_max.text())
		self.n_points=np.int(self.lectn_points.text())

		self.freq_list=np.linspace(self.f_min,self.f_max,self.n_points)
		self.x=self.freq_list
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

		self.config_uW_1() #Pour une raison mysterieuse il vaut mieux le faire au début
		self.config_uW_2()

		def DEER(t_echo,t_lect,t_ecl,pulse_pi_sur_2,pulse_pi):
			with open('PB_instructions.txt','w') as f:

				f.write('label :0b 1100, 20 ns \n')
				for i in range(self.n_echo_per_point):
					f.write('\t0b 1100, '+t_ecl+'\n')
					f.write('\t0b 0000, '+pulse_pi_sur_2+'\n')
					f.write('\t0b 1000, '+t_echo+'\n')
					f.write('\t0b 0000, '+pulse_pi+'\n')
					f.write('\t0b 1000, '+t_echo+'\n')
					f.write('\t0b 0000, '+pulse_pi_sur_2+'\n')
					f.write('\t0b 1110, 20 ns \n') 
					f.write('\t0b 1100, '+t_lect+'\n') 
					f.write('\t0b 1110, 20 ns \n') 
				f.write('\t0b 1101, 1 us, branch, label') 
				

		DEER(self.t_echo,self.t_lect,self.t_ecl,self.pulse_pi_sur_2,self.pulse_pi)
		check_output('spbicl load pb_instructions.txt 500.0')




		self.apd=nidaqmx.Task()
		self.apd.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
		self.apd.timing.cfg_samp_clk_timing(1E8,source='/Dev1/PFI9',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=2*self.n_echo_per_point*self.n_points)


		self.apd.start()
			
		self.repeat=1.
		

		#Start the timer     
		self.timer = QTimer(self,interval=0)        
		self.timer.timeout.connect(self.measure)
		self.timer.start()
		check_output('spbicl start')

		
		
	def measure(self):
		try :
			self.take_point()
		except :
			fig=self.dynamic_ax.figure
			data=[]
			for ax in fig.get_axes() :
				for line in ax.get_lines() :
					data+=[line._x]
					data+=[line._y]

			fname='aborted measure'
			fdataname=fname+".txt"
			with open(fdataname,'w') as f: #Needs an update if the lines have differents sizes
				for i in range(len(data[0])) :
					for ligne in data :
						f.write("%5.4E \t"%ligne[i]) #Format = 5 significative numbers, scientific notation

					f.write("\n")
			fig.savefig(fname+'.png')
			

	def take_point(self):

		PL=np.zeros(self.n_points)
		lect=self.apd.read(2*self.n_echo_per_point*self.n_points)
		for i in range(self.n_points):
			for j in range(self.n_echo_per_point):
				PL[i]+=lect[i*self.n_echo_per_point*2+2*j+1]-lect[i*self.n_echo_per_point*2+2*j]
		
		PL=PL/self.n_echo_per_point/self.t_lect_val	


		if self.normalize_cb.isChecked() :
			PL=PL/max(PL)

		

		if min(PL) >= 0 : #Pour éviter les reset de compteur
			self.y=self.y*(1-1/self.repeat)+PL*(1/self.repeat)
			self.repeat+=1

		self.dynamic_line.set_ydata(self.y)
		ymin=min(self.y)
		ymax=max(self.y)
		self.dynamic_ax.set_ylim([ymin,ymax]) 

		# print(len(self.dynamic_line.get_xdata()))
		# print(len(self.dynamic_line.get_ydata()))
		self.dynamic_ax.figure.canvas.draw()

		self.labelIter.setText("iter # %i"%self.repeat)

		# print(self.PG.query('SYSTem:ERRor:NEXT?'))
		# if self.repeat > 1:
		#     self.stop_measure()
	 

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
			self.ser.write(b'OUTP:STAT OFF\n')
		except :
			pass
		try :
			check_output('spbicl stop')
		except :
			pass
		try :
			self.PG1.write('*RST')
			self.PG1.write('*WAI')
		except :
			pass
		try :
			self.PG2.write('*RST')
			self.PG2.write('*WAI')
		except :
			pass
		
		
		


		
		self.stop.setEnabled(False)
		self.start.setEnabled(True)  


	def config_uW_1(self):
		resourceString1 = 'USB0::0x0AAD::0x0054::110693::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"

		rm1 = visa.ResourceManager()
		self.PG1 = rm1.open_resource( resourceString1 )
		self.PG1.write_termination = '\n'

		self.PG1.clear()  # Clear instrument io buffers and status
		self.PG1.write('*WAI')
		self.PG1.write('FREQ %f MHz'%self.f)
		self.PG1.write('*WAI')
		self.PG1.write('POW %f dBm'%self.level_uW_1)
		self.PG1.write('*WAI')
		self.PG1.write('OUTP ON')
		self.PG1.write('*WAI')

	def config_uW_2(self):

		def create_list_freq(fmin,fmax,level,n_points) :
		#Frequecy given in GHz
			freq_list=np.linspace(fmin,fmax,n_points)
			instruction_f='SOUR:LIST:FREQ'
			for f in freq_list :
				if f==max(freq_list) :
					instruction_f+=' %f MHz'%f
				else :
					instruction_f+=' %f MHz,'%f
			instruction_pow='SOUR:LIST:POW'
			for f in freq_list :
				if f==max(freq_list) :
					instruction_pow+=' %f dBm'%level
				else :
					instruction_pow+=' %f dBm,'%level
			return instruction_f,instruction_pow

		freq_list,pow_list=create_list_freq(self.f_min,self.f_max,self.level_uW_2,self.n_points)


		resourceString2 = 'USB0::0x0AAD::0x0054::110140::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"

		rm2 = visa.ResourceManager()
		self.PG2 = rm2.open_resource( resourceString2 )
		self.PG2.write_termination = '\n'
		self.PG2.timeout=3000

		self.PG2.clear()  # Clear instrument io buffers and status
		self.PG2.write('*WAI')

		self.PG2.write(':LIST:DELete:ALL')
		self.PG2.write('*WAI')

		self.PG2.write('LIST:SEL "new_list"') #Il lui faut un nom, j'espere qu'il y a pas de blagues si je réécris dessus
		self.PG2.write('*WAI')

		self.PG2.write(freq_list)
		self.PG2.write('*WAI')

		self.PG2.write(pow_list)
		self.PG2.write('*WAI')

		self.PG2.write('LIST:LEAR') #Peut etre bien facultatif
		self.PG2.write('*WAI')

		self.PG2.write('LIST:MODE STEP')
		self.PG2.write('*WAI')

		self.PG2.write('LIST:TRIG:SOUR EXT')
		self.PG2.write('*WAI')

		self.PG2.write('OUTP ON') #OFF/ON pour allumer éteindre la uW
		self.PG2.write('*WAI')

		self.PG2.write('FREQ:MODE LIST') #on doit allumer la uW avant de passer en mode liste
		self.PG2.write('*WAI')


		# with nidaqmx.Task() as trig :
		#     trig.do_channels.add_do_chan('Dev1/port0/line1')
		#     trig.timing.cfg_samp_clk_timing(self.sampling_rate*2,sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=self.n_points)
		#     trig.write([True,False]*self.n_points)
		#     trig.start()

		self.PG2.write('LIST:RES') #Ca par contre ca a l'air de jouer curieusement
		self.PG2.write('*WAI')








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
