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
		

		self.sampling_rate=1E3 #Ne pas monter au dessus de 1E3
		self.n_points=601
		self.f_min=2.5
		self.f_max=3.2 #GHz      
		self.level=20 #dBm
		self.n_iter=30

		self.V_min=0
		self.V_max=10
		self.n_scan=100



		self.freq_list=np.linspace(self.f_min,self.f_max,self.n_points)



		

		##Creation of the graphical interface##

		self.setWindowTitle("Scans ESR")

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
		self.labelf_min=QLabel("f_min (GHz)")
		self.lectf_min=QLineEdit(str(self.f_min))
		Vbox_gauche.addWidget(self.labelf_min)
		Vbox_gauche.addWidget(self.lectf_min)

		self.labelf_max=QLabel("f_max (GHz)")
		self.lectf_max=QLineEdit(str(self.f_max))
		Vbox_gauche.addWidget(self.labelf_max)
		Vbox_gauche.addWidget(self.lectf_max)

		self.labellevel=QLabel("level (dBm)")
		self.lectlevel=QLineEdit(str(self.level))
		Vbox_gauche.addWidget(self.labellevel)
		Vbox_gauche.addWidget(self.lectlevel)

		self.labeln_points=QLabel("n_points")
		self.lectn_points=QLineEdit(str(self.n_points))
		Vbox_gauche.addWidget(self.labeln_points)
		Vbox_gauche.addWidget(self.lectn_points)

		self.labeln_iter=QLabel("n_iter")
		self.lectn_iter=QLineEdit(str(self.n_iter))
		Vbox_gauche.addWidget(self.labeln_iter)
		Vbox_gauche.addWidget(self.lectn_iter)

		Vbox_gauche.addStretch(1)

		self.labelV_min=QLabel("V_min (mm)")
		self.lectV_min=QLineEdit(str(self.V_min))
		Vbox_gauche.addWidget(self.labelV_min)
		Vbox_gauche.addWidget(self.lectV_min)

		self.labelV_max=QLabel("V_max (mm)")
		self.lectV_max=QLineEdit(str(self.V_max))
		Vbox_gauche.addWidget(self.labelV_max)
		Vbox_gauche.addWidget(self.lectV_max)

		self.labeln_scan=QLabel("n_scan")
		self.lectn_scan=QLineEdit(str(self.n_scan))
		Vbox_gauche.addWidget(self.labeln_scan)
		Vbox_gauche.addWidget(self.lectn_scan)




		#Buttons on the right
		self.stop=QPushButton('Stop')
		self.start=QPushButton('Start')
		self.keep_button=QPushButton('Keep trace')
		self.clear_button=QPushButton('Clear Last Trace')
		self.normalize_cb=QCheckBox('Normalize')

		
		self.labelIter=QLabel("iter # 0")
		self.labelscan=QLabel("scanr # 0")

		
		Vbox_droite.addWidget(self.normalize_cb)
		Vbox_droite.addStretch(1)
		Vbox_droite.addWidget(self.start)
		Vbox_droite.addWidget(self.stop)
		Vbox_droite.addStretch(1)
		Vbox_droite.addWidget(self.keep_button)
		Vbox_droite.addWidget(self.clear_button)
		Vbox_droite.addStretch(1)
		Vbox_droite.addWidget(self.labelIter)
		Vbox_droite.addWidget(self.labelscan)


		self.stop.setEnabled(False)
		
		
		#Plot in the middle
		dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
		Vbox.addStretch(1)
		Vbox.addWidget(dynamic_canvas)
		self.addToolBar(Qt.BottomToolBarArea,
						MyToolbar(dynamic_canvas, self))
		self.dynamic_ax= dynamic_canvas.figure.subplots()

		self.x=self.freq_list[:-1]
		self.y=np.zeros(self.n_points-1)
		self.dynamic_line,=self.dynamic_ax.plot(self.x, self.y)
  





			  
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
		self.f_min=np.float(self.lectf_min.text())
		self.f_max=np.float(self.lectf_max.text())
		self.level=np.float(self.lectlevel.text())
		self.V_min=np.float(self.lectV_min.text())
		self.V_max=np.float(self.lectV_max.text())

		self.n_points=np.int(self.lectn_points.text())
		self.n_scan=np.int(self.lectn_scan.text())
		self.n_iter=np.int(self.lectn_iter.text())

		self.freq_list=np.linspace(self.f_min,self.f_max,self.n_points)
		self.x=self.freq_list[:-1]
		self.y=np.zeros(self.n_points-1)
		xmin=min(self.x)
		xmax=max(self.x)
		self.dynamic_ax.set_xlim([xmin,xmax]) 

		self.dynamic_line.set_data(self.x,self.y)
	   

	def start_measure(self):

		
		
		
		self.fname, filter = QFileDialog.getSaveFileName(None,
										 "Choose a filename to save to",
										 "D:/DATA", "Documents texte (*.txt)")

		self.config_PS()
		with open(self.fname,'w') as f:
			f.write('f_min=%f \t f_max=%f \t V_min=%f \t V_max=%f \n'%(self.f_min,self.f_max,self.V_min,self.V_max))
		self.list_val=np.linspace(self.V_min,self.V_max,self.n_scan)
		self.index_val=0
		self.start_ESR()




	def start_ESR(self):
		## What happens when you click "start" ##

		self.start.setEnabled(False)
		self.stop.setEnabled(True)


		
		self.update_value()
		

		self.config_uW() #Pour une raison mysterieuse il vaut mieux le faire au début


		self.sample_clock=nidaqmx.Task()
		self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.sampling_rate)
		self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse


		self.apd=nidaqmx.Task()
		self.apd.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
		self.apd.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_points)

		self.trig_uW=nidaqmx.Task()
		self.trig_uW.do_channels.add_do_chan('Dev1/port0/line1')
		self.trig_uW.timing.cfg_samp_clk_timing(self.sampling_rate*2,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_points)


		self.sample_clock.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/do/StartTrigger')

		
		#self.trig_uW.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/Ctr1Source')  


		signal=([True]+[False])*self.n_points
		self.trig_uW.write(signal)

		self.sample_clock.start()	
		self.apd.start()
			
		
		self.repeat=1.

		#Start the timer     
		self.timer = QTimer(self,interval=0)        
		self.timer.timeout.connect(self.take_point)

		

		self.trig_uW.start()
		self.timer.start() 
		

		

	def take_point(self):

		if self.repeat >=self.n_iter :
			if self.index_val==self.n_scan-1:
				self.stop_measure()
				self.pi.close()
				return 0
			else :
				with open(self.fname,'a') as f:
					for val in self.y:
						f.write('%f \t'%val)
					f.write('\n')

				self.index_val+=1
				self.labelscan.setText("scan # %i"%self.index_val)
				newval=self.list_val[self.index_val]
				self.PG2.write('APPLY "%f,%f"' % (newval,1))
				self.PG2.write('*WAI')  

				
				self.stop_measure()
				self.start_ESR()






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
			self.sample_clock.close()
		except :
			pass
		try :
			self.PG.write('*RST')
			self.PG.write('*WAI')
			self.PG.close()
		except :
			pass
		try :
			self.trig_uW.close()

		except :
			pass
		

		
		
		self.start.setEnabled(True)
		self.stop.setEnabled(False)

		
		

	def config_uW(self):

		def create_list_freq(fmin,fmax,level,n_points) :
		#Frequecy given in GHz
			freq_list=np.linspace(fmin,fmax,n_points)
			instruction_f='SOUR:LIST:FREQ'
			for f in freq_list :
				if f==max(freq_list) :
					instruction_f+=' %f GHz'%f
				else :
					instruction_f+=' %f GHz,'%f
			instruction_pow='SOUR:LIST:POW'
			for f in freq_list :
				if f==max(freq_list) :
					instruction_pow+=' %f dBm'%level
				else :
					instruction_pow+=' %f dBm,'%level
			return instruction_f,instruction_pow

		freq_list,pow_list=create_list_freq(self.f_min,self.f_max,self.level,self.n_points)


		resourceString4 = 'TCPIP0::micro-onde.phys.ens.fr::inst0::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"

		rm = visa.ResourceManager()
		self.PG = rm.open_resource( resourceString4 )
		self.PG.write_termination = '\n'
		self.PG.timeout=10000

		self.PG.clear()  # Clear instrument io buffers and status
		self.PG.write('*WAI')

		self.PG.write(':LIST:DELete:ALL')
		self.PG.write('*WAI')

		self.PG.write('LIST:SEL "new_list"') #Il lui faut un nom, j'espere qu'il y a pas de blagues si je réécris dessus
		self.PG.write('*WAI')

		self.PG.write(freq_list)
		self.PG.write('*WAI')

		self.PG.write(pow_list)
		self.PG.write('*WAI')

		self.PG.write('LIST:LEAR') #Peut etre bien facultatif
		self.PG.write('*WAI')

		self.PG.write('LIST:MODE STEP')
		self.PG.write('*WAI')

		self.PG.write('LIST:TRIG:SOUR EXT')
		self.PG.write('*WAI')

		self.PG.write('OUTP ON') #OFF/ON pour allumer éteindre la uW
		self.PG.write('*WAI')

		self.PG.write('FREQ:MODE LIST') #on doit allumer la uW avant de passer en mode liste
		self.PG.write('*WAI')


		# with nidaqmx.Task() as trig :
		#     trig.do_channels.add_do_chan('Dev1/port0/line1')
		#     trig.timing.cfg_samp_clk_timing(self.sampling_rate*2,sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=self.n_points)
		#     trig.write([True,False]*self.n_points)
		#     trig.start()
		
		self.PG.write('LIST:RES') #Ca par contre ca a l'air de jouer curieusement
		self.PG.write('*WAI')

	def config_PS(self):
		resourceString4 = 'USB0::0x0AAD::0x0197::5601.3800k03-101213::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"
		rm = visa.ResourceManager()
		self.PG2 = rm.open_resource( resourceString4 )
		self.PG2.write_termination = '\n'
		self.PG2.clear()  # Clear instrument io buffers and status
		self.PG2.write('OUTP:GEN 0')
		self.PG2.write('*WAI')
		self.PG2.write('INST 1')
		self.PG2.write('*WAI')
		self.PG2.write('VOLTage:RAMP OFF')
		self.PG2.write('*WAI')
		self.PG2.write('OUTP:SEL 1')
		self.PG2.write('*WAI')
		self.PG2.write('APPLY "%f,%f"' % (self.V_min,1))
		self.PG2.write('*WAI') 
		self.PG2.write('OUTP:GEN 1')
		self.PG2.write('*WAI')







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
