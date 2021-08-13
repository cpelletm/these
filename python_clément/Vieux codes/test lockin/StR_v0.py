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
import statistics



from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
	QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QComboBox)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure



class Photon_Counter(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.VtoB=1e-3
		self.bande_passante=1e-2 #s

		self.dt_meas=1e-3
		self.dt_V=1

		self.rising_ratio=0.1

		self.V_0=0
		self.dV=5e-2

		self.n_bins=40
		self.refresh_rate=0.2 #s

		self.f_acq=1/self.dt_meas
		self.n_acq=2*int(self.dt_V/self.dt_meas)
		self.nplus=int(self.dt_V/self.dt_meas)

		self.xmin=-1
		self.xmax=1

		self.StR=0

		self.n_points=100
		self.V_min=-2
		self.V_max=2
		self.V_0_list=np.linspace(self.V_min,self.V_max,self.n_points)
		self.n_per_point=10

		##Creation of the graphical interface##

		self.setWindowTitle("StR V0")

		self.main = QWidget()
		self.setCentralWidget(self.main)

		layout= QHBoxLayout()
		Vbox_gauche = QVBoxLayout()
		Vbox = QVBoxLayout()
		Vbox_droite=QVBoxLayout()

		layout.addLayout(Vbox_gauche)
		layout.addLayout(Vbox)
		layout.addLayout(Vbox_droite)
		self.main.setLayout(layout)

		gras=QFont( "Consolas", 40, QFont.Bold)
		self.StR_label=QLabel()
		self.StR_label.setFont(gras)
		Vbox_gauche.addWidget(self.StR_label)
		Vbox_gauche.addStretch(1)

		self.labelV_0=QLabel("V_0")
		self.lectV_0=QLineEdit(str(self.V_0))
		Vbox_gauche.addWidget(self.labelV_0)
		Vbox_gauche.addWidget(self.lectV_0)
		Vbox_gauche.addStretch(1)

		self.labeldV=QLabel("dV")
		self.lectdV=QLineEdit(str(self.dV))
		Vbox_gauche.addWidget(self.labeldV)
		Vbox_gauche.addWidget(self.lectdV)
		Vbox_gauche.addStretch(1)

		self.labeln_bins=QLabel("n_bins")
		self.lectn_bins=QLineEdit(str(self.n_bins))
		Vbox_gauche.addWidget(self.labeln_bins)
		Vbox_gauche.addWidget(self.lectn_bins)
		Vbox_gauche.addStretch(1)

		


		#Buttons on the right

		self.stop=QPushButton('Stop')
		self.start=QPushButton('Start')
		self.keep_button=QPushButton('Keep trace')
		self.clear_button=QPushButton('Clear Last Trace')
		self.auto_xlims_cb=QCheckBox('Auto lims')
		self.auto_xlims_cb.setChecked(True)

		
		self.labelIter=QLabel("iter # 0")


		Vbox_droite.addStretch(1)
		Vbox_droite.addWidget(self.auto_xlims_cb)
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

		self.x=self.V_0_list
		self.y=np.ones(self.n_points)
		self.dynamic_line,=self.dynamic_ax.plot(self.x,self.y,'x')

		self.dynamic_ax.set_yscale("log")




			  
		#Define the buttons' action 
		

		self.start.clicked.connect(self.start_measure)
		self.stop.clicked.connect(self.stop_measure)
		self.keep_button.clicked.connect(self.keep_trace)
		self.clear_button.clicked.connect(self.clear_trace)

	def keep_trace(self):
		self.dynamic_ax.plot(self.dynamic_line_line._x,self.dunamic_line._y)

	def clear_trace(self):
		lines=self.dynamic_ax.get_lines()
		line=lines[-1]
		if line != self.dynamic_line :
			line.remove()
		self.dynamic_ax.figure.canvas.draw()


		



	def update_value(self):
		self.n_bins=np.int(self.lectn_bins.text())
		self.V_0=np.float(self.lectV_0.text())
		self.dV=np.float(self.lectdV.text())

		self.f_acq=1/self.dt_meas
		self.n_acq=2*int(self.dt_V/self.dt_meas)
		self.nplus=int(self.dt_V/self.dt_meas)
		self.n_rising=int(self.nplus*self.rising_ratio)




	def start_measure(self):
		## What happens when you click "start" ##


		self.start.setEnabled(False)
		self.stop.setEnabled(True)

		self.update_value()
		

		




		#Start the timer     
		self.timer = QTimer(self,interval=0)        
		self.timer.timeout.connect(self.take_point)
				
		self.n_current_index=0		
		self.timer.start() 
		

		

	def take_point(self):

		self.V_0=self.V_0_list[self.n_current_index]

		voltage_list=[self.V_0-self.dV/2]*self.nplus+[self.V_0+self.dV/2]*self.nplus

		self.voltage_out=nidaqmx.Task()
		self.voltage_out.ao_channels.add_ao_voltage_chan('Dev1/ao0')
		self.voltage_out.timing.cfg_samp_clk_timing(self.f_acq,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_acq)

		self.voltage_out.write(voltage_list)


		self.tension=nidaqmx.Task()
		self.tension.ai_channels.add_ai_voltage_chan("Dev1/ai11")
		self.tension.timing.cfg_samp_clk_timing(self.f_acq,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_acq)

		self.tension.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/ao/StartTrigger')
		self.tension.start()
		self.voltage_out.start()

		self.hist_data=[]
		for i in range(self.n_per_point) :
			lecture_brut=self.tension.read(self.n_acq)

			lecture=np.array(lecture_brut[self.n_rising:self.nplus])-np.array(lecture_brut[self.nplus+self.n_rising:])
			lecture=list(lecture)

			self.hist_data+=lecture

		self.tension.close()
		self.voltage_out.close()

		mu=statistics.mean(self.hist_data)
		sigma=statistics.pstdev(self.hist_data)

		StR=sigma/abs(mu)*self.VtoB*self.dV*np.sqrt(self.bande_passante)
		self.y[self.n_current_index]=StR
		ymin=min(self.y)
		ymax=max(self.y)
		self.dynamic_ax.set_ylim([ymin,ymax])
		self.dynamic_line.set_ydata(self.y)
		self.dynamic_ax.figure.canvas.draw()

		if self.n_current_index==self.n_points-1:
			self.stop_measure()
		else :
			self.n_current_index+=1
			time.sleep(5)

		

		self.labelIter.setText("iter # %i"%self.n_current_index)
			
	 

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
