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
		

		self.time_point=10e-3 #time per point in s.
		self.n_points=51
		self.f_min=2800
		self.f_max=2950    
		self.level=10 #dBm


		self.freq_list=np.linspace(self.f_min,self.f_max,self.n_points)



		

		##Creation of the graphical interface##

		self.setWindowTitle("ESR petite_uW")

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

		self.x=self.freq_list
		self.y=np.zeros(self.n_points)
		self.dynamic_line,=self.dynamic_ax.plot(self.x, self.y)
  





			  
		#Define the buttons' action 
		
		self.start.clicked.connect(self.start_measure)
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
		self.f_min=np.float(self.lectf_min.text())
		self.f_max=np.float(self.lectf_max.text())
		self.level=np.float(self.lectlevel.text())
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

		self.config_uW() #Pour une raison mysterieuse il vaut mieux le faire au début

		def ESR(t_scan='10 ms') :
			with open('PB_instructions.txt','w') as f:
				f.write('label: 0b 0110, 20 ns\n')
				f.write('\t0b 0100, '+t_scan+'\n')
				f.write('\t0b 0110, 20 ns\n')
				f.write('\t0b 0100, 10 s, branch, label')

		ESR('%f s'%self.time_point)
		check_output('spbicl load pb_instructions.txt 500.0')



		self.apd=nidaqmx.Task()
		self.apd.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
		self.apd.timing.cfg_samp_clk_timing(1E8,source='/Dev1/PFI9',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=2)


		self.apd.start()
			
		self.repeat=1.
		

		#Start the timer     
		self.timer = QTimer(self,interval=0)        
		self.timer.timeout.connect(self.take_point)
		self.timer.start()

		
		

		

	def take_point(self):

		PL=np.zeros(self.n_points)
		for i in range(self.n_points):

			self.ser.write(b'INIT:IMM \n')
			check_output('spbicl start')
			lecture=self.apd.read(2)
			check_output('spbicl stop')
			PL[i]=(lecture[1]-lecture[0])/self.time_point


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
			self.ser.close()
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

		self.ser = serial.Serial("COM6", 115200, timeout=1)
		time.sleep(0.1)#Ca fait office de *WAI
		self.ser.write(b'ABORT\n')
		time.sleep(0.1) 
		self.ser.write(b'POWER %i\n'%self.level)
		time.sleep(0.1) 
		self.ser.write(b'FREQ:START %f MHZ\n'%self.f_min)
		time.sleep(0.1)
		self.ser.write(b'FREQ:STOP %f MHZ\n'%self.f_max)
		time.sleep(0.1)
		self.ser.write(b'SWE:POINTS %i\n'%self.n_points)
		time.sleep(0.1)
		self.ser.write(b'INIT:CONT 1\n')
		time.sleep(0.1)
		self.ser.write(b'TRIG:STEP\n')
		time.sleep(0.1)
		self.ser.write(b'SWE:MODE SCAN\n')
		time.sleep(0.1)
		self.ser.write(b'OUTP:STAT ON\n')
		time.sleep(0.1)







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
