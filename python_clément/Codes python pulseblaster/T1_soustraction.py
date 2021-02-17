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
		
		self.setWindowTitle("T1_sub")

		self.t_max='1.5 ms'
		self.t_ecl='300 us'
		self.t_lect='300 us'
		self.n_points=200
		
		self.zoom_proportion=0.5 #Proportions of points in the zoomed area
		self.zoom_range=0.25 #Size of the zoomed area in proportion of total time scanned. Keep at same value than zoom_proportion for no zoom
		self.refresh_rate=0.1

		self.frequency=2865 # MHz
		self.power=15 # dBm
		self.t_pulse="1000 ns"

		self.t_min="2000 ns"
		
		##Creation of the graphical interface##

		

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
		self.labelt_max=QLabel("t_max")
		self.lectt_max=QLineEdit(str(self.t_max))
		Vbox_gauche.addWidget(self.labelt_max)
		Vbox_gauche.addWidget(self.lectt_max)
		Vbox_gauche.addStretch(1)

		self.labelt_ecl=QLabel("t_ecl")
		self.lectt_ecl=QLineEdit(str(self.t_ecl))
		Vbox_gauche.addWidget(self.labelt_ecl)
		Vbox_gauche.addWidget(self.lectt_ecl)
		Vbox_gauche.addStretch(1)

		self.labelt_lect=QLabel("t_lect")
		self.lectt_lect=QLineEdit(str(self.t_lect))
		Vbox_gauche.addWidget(self.labelt_lect)
		Vbox_gauche.addWidget(self.lectt_lect)
		Vbox_gauche.addStretch(1)

		self.labeln_points=QLabel("n_points")
		self.lectn_points=QLineEdit(str(self.n_points))
		Vbox_gauche.addWidget(self.labeln_points)
		Vbox_gauche.addWidget(self.lectn_points)

		self.labelfrequency=QLabel("frequency (MHz)")
		self.lectfrequency=QLineEdit(str(self.frequency))
		Vbox_gauche.addWidget(self.labelfrequency)
		Vbox_gauche.addWidget(self.lectfrequency)
		Vbox_gauche.addStretch(1)

		self.labelpower=QLabel("power (dBm)")
		self.lectpower=QLineEdit(str(self.power))
		Vbox_gauche.addWidget(self.labelpower)
		Vbox_gauche.addWidget(self.lectpower)
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
		self.dynamic_ax= dynamic_canvas.figure.subplots()

		self.x=np.zeros(self.n_points)
		self.y=np.zeros(self.n_points)
		self.dynamic_line,=self.dynamic_ax.plot(self.x, self.y)
		self.dynamic_ax.set_xlabel('time (s)')
  


		self.update_value()


			  
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

	def num_val(self,pbtext):
		for s in pbtext.split() :
			try :
				val=float(s)
			except :
				unit=s
		if unit=='ms' :
			val=val*1e-3
		if unit=='us' :
			val=val*1e-6
		if unit=='ns' :
			val=val*1e-9
		return val

	def make_taux_list(self,t_max,n_points,zoom_proportion,zoom_range,t_pulse,t_min):

		t_max_val=self.num_val(t_max)
		t_max_zoom=t_max_val*zoom_range
		t_pulse_val=self.num_val(t_pulse)
		t_min_val=self.num_val(t_min)

		n_zoom=int(n_points*zoom_proportion)
		n_pas_zoom=n_points-n_zoom
		taux_zoom=np.linspace(t_min_val,t_max_zoom,n_zoom)
		taux_pas_zoom=np.linspace(t_max_zoom,t_max_val,n_pas_zoom)
		taux=[]
		x=[]
		for t in taux_zoom :
			taux+=['%i ns'%((t-t_pulse_val)*1e9)]
			x+=[t]
		for t in taux_pas_zoom :
			taux+=['%i ns'%((t-t_pulse_val)*1e9)]
			x+=[t]
		x=np.array(x)
		return(taux,x)
		
	def update_value(self):
		self.t_max=self.lectt_max.text()
		self.t_ecl=self.lectt_ecl.text()
		self.t_lect=self.lectt_lect.text()
		self.n_points=int(self.lectn_points.text())
		self.frequency=float(self.lectfrequency.text())
		self.power=float(self.lectpower.text())

		self.config_uW()

		self.t_lect_val=self.num_val(self.t_lect)
		self.taux,self.x=self.make_taux_list(self.t_max,self.n_points,self.zoom_proportion,self.zoom_range,self.t_pulse,self.t_min)		
		self.n_points=len(self.taux)
		self.y=np.zeros(self.n_points)
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

		def T1_soustraction(taux,t_lect,t_ecl,t_pulse):
			with open('PB_instructions.txt','w') as f:
				for i in range(len(taux)) :
					tau=taux[i]
					if i == 0:
						f.write('label : ')
					else : 
						f.write('\t')

					f.write('0b 0100, '+t_ecl+'\n')
					f.write('\t0b 0000, '+tau+'\n')
					f.write('\t0b 0000, '+t_pulse+'\n')
					f.write('\t0b 0110, 20 ns \n') 
					f.write('\t0b 0100, '+t_lect+'\n') 
					f.write('\t0b 0110, 20 ns \n') 

					f.write('\t0b 0100, '+t_ecl+'\n')
					f.write('\t0b 0000, '+tau+'\n')
					f.write('\t0b 1000, '+t_pulse+'\n')
					f.write('\t0b 0110, 20 ns \n') 
					f.write('\t0b 0100, '+t_lect+'\n') 
					f.write('\t0b 0110, 20 ns') 
					if i==len(taux)-1:
						f.write(', branch, label')
					else :
						f.write('\n')

		T1_soustraction(self.taux,self.t_lect,self.t_ecl,self.t_pulse)
		check_output('spbicl load pb_instructions.txt 500.0')



		self.apd=nidaqmx.Task()
		self.apd.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
		self.apd.timing.cfg_samp_clk_timing(100E6,source='/Dev1/PFI9',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_points)


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


		lecture=self.apd.read(4*self.n_points)


		# PL=np.array([(lecture[i+1]-lecture[i])*self.sampling_rate for i in range(len(lecture)-1)])

		lecture=np.array(lecture)
		PL1=np.zeros(self.n_points)
		PL2=np.zeros(self.n_points)
		for i in range(self.n_points):
			PL1[i]=(lecture[4*i+1]-lecture[4*i])/self.t_lect_val
			PL2[i]=(lecture[4*i+3]-lecture[4*i+2])/self.t_lect_val

		PL=PL1-PL2
		if self.normalize_cb.isChecked() :
			PL=PL/max(PL)

		

		if min(PL1) >= 0 and min(PL2) >= 0: #Pour éviter les reset de compteur
			self.y=self.y*(1-1/self.repeat)+PL*(1/self.repeat)
			self.repeat+=1


		if time.time()-self.time_last_refresh>self.refresh_rate :
			self.dynamic_line.set_ydata(self.y)
			ymin=min(self.y)
			ymax=max(self.y)
			self.dynamic_ax.set_ylim([ymin,ymax]) 

			self.dynamic_ax.figure.canvas.draw()

			self.labelIter.setText("iter # %i"%self.repeat)
			self.time_last_refresh=time.time()
	 

	def config_uW(self):
		resourceString4 = 'TCPIP0::micro-onde.phys.ens.fr::inst0::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"

		rm = visa.ResourceManager()
		self.PG = rm.open_resource( resourceString4 )
		self.PG.write_termination = '\n'

		self.PG.clear()  # Clear instrument io buffers and status
		self.PG.write('*WAI')
		self.PG.write('FREQ %f MHz'%self.frequency)
		self.PG.write('*WAI')
		self.PG.write('POW %f dBm'%self.power)
		self.PG.write('*WAI')
		self.PG.write('OUTP ON')
		self.PG.write('*WAI')


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
			self.PG.close()
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
