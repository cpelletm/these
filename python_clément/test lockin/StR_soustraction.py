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
		
		self.VtoB=4e-3
		self.bande_passante=1e-2 #s

		self.dt_meas=1e-3
		self.dt_V=1

		self.rising_ratio=0.1

		self.V_0=0.05
		self.dV=1e-2

		self.n_bins=40
		self.refresh_rate=0.2 #s

		self.f_acq=1/self.dt_meas
		self.n_acq=2*int(self.dt_V/self.dt_meas)
		self.nplus=int(self.dt_V/self.dt_meas)

		self.xmin=-1
		self.xmax=1

		self.StR=0

		

		##Creation of the graphical interface##

		self.setWindowTitle("StR")

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

		self.x=np.zeros(100)
		self.y=np.zeros(100)
		self.dynamic_line,=self.dynamic_ax.plot(self.x,self.y,'x')
		self.fit_line,=self.dynamic_ax.plot(self.x,self.y,label='fit')
		# self.testpline,=self.dynamic_ax.plot(self.x,self.y,'o')
		# self.testmline,=self.dynamic_ax.plot(self.x,self.y,'v')
		self.zero_line=self.dynamic_ax.plot([0,0],[0,1000])

		self.dynamic_ax.legend()





			  
		#Define the buttons' action 
		

		self.start.clicked.connect(self.start_measure)
		self.stop.clicked.connect(self.stop_measure)
		self.keep_button.clicked.connect(self.keep_trace)
		self.clear_button.clicked.connect(self.clear_trace)

	def keep_trace(self):
		self.dynamic_ax.plot(self.fit_line._x,self.fit_line._y,label='mu=%4.3e ; sigma=%4.3e'%(self.mu,self.sigma))

	def clear_trace(self):
		lines=self.dynamic_ax.get_lines()
		line=lines[-1]
		if line != self.dynamic_line and line != self.fit_line :
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
		

		self.time_last_refresh=time.time()

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

		self.hist_data=[]	
		self.hist_data_plus=[]
		self.hist_data_moins=[]
		self.repeat=0

		#Start the timer     
		self.timer = QTimer(self,interval=0)        
		self.timer.timeout.connect(self.take_point)
		self.voltage_out.start()				
		self.timer.start() 
		

		

	def take_point(self):





		lecture_brut=self.tension.read(self.n_acq)

		# print(lecture_brut)

		lecture=np.array(lecture_brut[self.n_rising:self.nplus])-np.array(lecture_brut[self.nplus+self.n_rising:])
		lecture=list(lecture)

		self.hist_data+=lecture
		self.hist_data_plus+=lecture_brut[self.n_rising:self.nplus]
		self.hist_data_moins+=lecture_brut[self.nplus+self.n_rising:]

		self.mu=statistics.mean(self.hist_data)
		self.sigma=statistics.pstdev(self.hist_data)

		self.StR=self.sigma/abs(self.mu)*self.VtoB*self.dV*np.sqrt(self.bande_passante)

		if self.auto_xlims_cb.isChecked():
			self.xmin=self.mu-3*self.sigma
			self.xmax=self.mu+3*self.sigma

		hist=np.histogram(self.hist_data,density=True,bins=self.n_bins,range=[self.xmin,self.xmax])
		self.y=hist[0]	
		self.x=(hist[1][:-1]+hist[1][1:])/2

		hist_plus=np.histogram(self.hist_data_plus,density=True,bins=self.n_bins,range=[self.xmin,self.xmax])
		hist_moins=np.histogram(self.hist_data_moins,density=True,bins=self.n_bins,range=[self.xmin,self.xmax])

		self.repeat+=1


		if time.time()-self.time_last_refresh>self.refresh_rate :
			self.time_last_refresh=time.time()

			self.StR_label.setText("%3.2E"%(self.StR))
			yplot=self.y
			self.dynamic_line.set_data(self.x,yplot)
			# self.testpline.set_data(self.x,hist_plus[0])
			# self.testmline.set_data(self.x,hist_moins[0])
			ymin=min(yplot)
			ymax=max(yplot)
			self.dynamic_ax.set_ylim([ymin,ymax]) 
			self.dynamic_ax.set_xlim([self.xmin,self.xmax])

			yfit=1/(self.sigma*np.sqrt(2*np.pi))*np.exp(-0.5*((self.x-self.mu)/self.sigma)**2)
			self.fit_line.set_data(self.x,yfit)
			self.fit_line.set_label('mu=%4.3e ; sigma=%4.3e'%(self.mu,self.sigma))
			self.dynamic_ax.legend()
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

		if fname:
			# Save dir for next time, unless empty str (i.e., use cwd).
			self.startpath = os.path.dirname(fname)

			try :
				fdataname=fname[:-4]+".csv"
				import csv
				with open(fdataname,'w',newline='') as csvfile :
					spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
					for ax in self.canvas.figure.get_axes() :
						for line in ax.get_lines() :
							spamwriter.writerow(line._x)
							spamwriter.writerow(line._y)
			except :
				print('Could not save data !')

			try:
				self.canvas.figure.savefig(fname)
			except :
				print('Could not save file !')

		

		






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()
