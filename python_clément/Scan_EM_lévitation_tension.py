import sys
import os
import time
import random
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system

import numpy as np


from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
	QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


#This is a photon counter for the NI 6341 card when the TTL signal is plugged into ctr0/source which is on pin PFI8/P2.0/81

class Photon_Counter(QMainWindow):
	def __init__(self):
		super().__init__()
		


		self.n_points=301
		self.t_scan=1
		self.V_min=-5
		self.V_max=+5

		self.n_glissant=10

		self.n_lect_min=0
		self.n_lect_max=-1

		self.time_last_refresh=time.time()
		self.refresh_rate=0.1
		
		self.setWindowTitle("Scan EM")

		##Creation of the graphical interface##

		self.main = QWidget()
		self.setCentralWidget(self.main)

		layout= QHBoxLayout()
		Vbox = QVBoxLayout()
		Vbox_gauche=QVBoxLayout()
		Vbox_droite=QVBoxLayout()

		layout.addLayout(Vbox_gauche)
		layout.addLayout(Vbox)
		layout.addLayout(Vbox_droite)
		self.main.setLayout(layout)

		#Fields on the left

		self.labelV_min=QLabel("V_min")
		self.lectV_min=QLineEdit(str(self.V_min))
		Vbox_gauche.addWidget(self.labelV_min)
		Vbox_gauche.addWidget(self.lectV_min)

		self.labelV_max=QLabel("V_max")
		self.lectV_max=QLineEdit(str(self.V_max))
		Vbox_gauche.addWidget(self.labelV_max)
		Vbox_gauche.addWidget(self.lectV_max)
		Vbox_gauche.addStretch(1)

		self.labelt_scan=QLabel("t_scan")
		self.lectt_scan=QLineEdit(str(self.t_scan))
		Vbox_gauche.addWidget(self.labelt_scan)
		Vbox_gauche.addWidget(self.lectt_scan)
		Vbox_gauche.addStretch(1)

		self.labeln_points=QLabel("n_points")
		self.lectn_points=QLineEdit(str(self.n_points))
		Vbox_gauche.addWidget(self.labeln_points)
		Vbox_gauche.addWidget(self.lectn_points)
		Vbox_gauche.addStretch(1)

		#Buttons on the right
		self.stop=QPushButton('Stop')
		self.start=QPushButton('Start')
		self.keep_button=QPushButton('Keep trace')
		self.clear_button=QPushButton('Clear Last Trace')
		self.fit_button=QPushButton('Fit')
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
		Vbox_droite.addWidget(self.fit_button)
		Vbox_droite.addStretch(1)
		Vbox_droite.addWidget(self.labelIter)


		self.stop.setEnabled(False)
		
		
		#Plot in the middle
		self.dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
		Vbox.addStretch(1)
		Vbox.addWidget(self.dynamic_canvas)
		self.addToolBar(Qt.BottomToolBarArea,
						MyToolbar(self.dynamic_canvas, self))


		## Matplotlib Setup ##


		self.dynamic_ax= self.dynamic_canvas.figure.subplots()

		self.t=np.linspace(0,100,100)
		self.y=np.zeros(100)	
		self.dynamic_line,=self.dynamic_ax.plot(self.t, self.y)

		self.dynamic_ax.set_xlabel('time(s)')
		self.dynamic_ax.set_ylabel('PL(counts/s)')

		
			  
		#Define the buttons' action 
		
		self.start.clicked.connect(self.start_measure)
		self.stop.clicked.connect(self.stop_measure)
		self.keep_button.clicked.connect(self.keep_trace)
		self.clear_button.clicked.connect(self.clear_trace)
		self.fit_button.clicked.connect(self.auto_fit)

		## Timer Setup ##

		self.timer = QTimer(self,interval=0) 
		self.timer.timeout.connect(self.update_canvas)

	def update_value(self):

		self.n_points=np.int(self.lectn_points.text())
		self.t_scan=np.float(self.lectt_scan.text())
		self.V_min=np.float(self.lectV_min.text())
		self.V_max=np.float(self.lectV_max.text())


		self.t_tot=2*self.t_scan
		self.n_tot=2*self.n_points*self.n_glissant

		self.n_lect_min=0
		self.n_lect_max=self.n_points

		self.f_acq=self.n_tot/self.t_tot
		Vm=(self.V_min+self.V_max)/2
		Nm=self.n_points*self.n_glissant//2
		self.V_list=list(np.linspace(Vm,self.V_min,Nm))+list(np.linspace(self.V_min,self.V_max,2*Nm))+list(np.linspace(self.V_max,Vm,self.n_tot-3*Nm))

		self.x=np.linspace(self.V_min,self.V_max,self.n_points)
		self.y=np.zeros(self.n_points)
		self.dynamic_line.set_data(self.x[self.n_lect_min:self.n_lect_max],self.y[self.n_lect_min:self.n_lect_max])
		self.set_lim(x=self.x[self.n_lect_min:self.n_lect_max],y=self.y[self.n_lect_min:self.n_lect_max])



		
			
	def keep_trace(self):
		self.dynamic_ax.plot(self.dynamic_line._x,self.dynamic_line._y)

	def clear_trace(self):
		lines=self.dynamic_ax.get_lines()
		line=lines[-1]
		if line != self.dynamic_line :
			line.remove()
		self.dynamic_ax.figure.canvas.draw()

	def auto_fit(self):
		from scipy.optimize import curve_fit,root_scalar
		x=self.dynamic_line._x[self.n_lect_min:self.n_lect_max]
		y=self.dynamic_line._y[self.n_lect_min:self.n_lect_max]
		
		def exp_fit(x,y,Amp=None,ss=None,tau=None) :
			if not Amp :
				Amp=max(y)-min(y)
			if not ss :
				ss=y[-1]
			if not tau :
				tau=x[int(len(x)/10)]-x[0]
			def f(x,Amp,ss,tau) :
				return Amp*np.exp(-x/tau)+ss
			p0=[Amp,ss,tau]
			popt, pcov = curve_fit(f, x, y, p0)
			return(popt,f(x,popt[0],popt[1],popt[2]))

		popt,yfit=exp_fit(x,y)
		self.dynamic_ax.plot(x,yfit,label='tau=%4.3e'%popt[2])
		self.dynamic_ax.legend()
		self.dynamic_canvas.draw()




	def set_lim(self,axes='both',x=[],y=[],line=None,ax=None):
		if not line:
			line=self.dynamic_line
		if not ax:
			ax=self.dynamic_ax
		if len(x)==0:
			x=line._x
		if len(y)==0:
			y=line._y
		xmin=min(x)
		xmax=max(x)
		ymin=min(y)
		ymax=max(y)
		Dx=xmax-xmin
		Dy=ymax-ymin
		dx=0.01*Dx+1e-15
		dy=0.01*Dy+1e-15
		if axes=='both' :
			ax.set_xlim([xmin-dx,xmax+dx])
			ax.set_ylim([ymin-dy,ymax+dy])
		if axes=='x' :
			ax.set_xlim([xmin-dx,xmax+dx])
		if axes=='y' :
			ax.set_ylim([ymin-dy,ymax+dy])

	def update_canvas(self):       
		##Update the plot and the value of the PL ##



		lecture=np.array(self.tension.read(self.n_tot,timeout=nidaqmx.constants.WAIT_INFINITELY))    

		PL=[sum(lecture[i*self.n_glissant:(i+1)*self.n_glissant])/self.n_glissant for i in range(self.n_points//2,3*self.n_points//2)]
		PL=np.array(PL)



		self.y=self.y*(1-1/self.repeat)+PL*(1/self.repeat)
		self.repeat+=1

		if time.time()-self.time_last_refresh>self.refresh_rate :
			self.time_last_refresh=time.time()

			if self.normalize_cb.isChecked() :
				ytoplot=self.y/max(self.y) 
			else :
				ytoplot=self.y

			self.dynamic_line.set_ydata(ytoplot[self.n_lect_min:self.n_lect_max])
			self.set_lim(x=self.x[self.n_lect_min:self.n_lect_max],y=ytoplot[self.n_lect_min:self.n_lect_max])

			self.dynamic_canvas.draw()

			self.labelIter.setText("iter # %i"%self.repeat)

		


	def start_measure(self):
		## What happens when you click "start" ##

		self.start.setEnabled(False)
		self.stop.setEnabled(True)

		#Read integration input values
		self.update_value()

		self.tension=nidaqmx.Task()
		self.tension.ai_channels.add_ai_voltage_chan("Dev1/ai11",min_val=-10,max_val=10)
		self.tension.timing.cfg_samp_clk_timing(self.f_acq,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_tot)

		self.voltage_out=nidaqmx.Task()
		self.voltage_out.ao_channels.add_ao_voltage_chan('Dev1/ao0')
		self.voltage_out.timing.cfg_samp_clk_timing(self.f_acq,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_tot)
		self.voltage_out.write(self.V_list)

		self.tension.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/ao/StartTrigger')
		self.tension.start()

		self.repeat=1


		#Start the task, then the timer
		
		self.voltage_out.start()
		self.timer.start() 


	def stop_measure(self):
		#Stop the measuring, clear the tasks on both counters
		try :
			self.timer.stop()
		except :
			pass
		try :
			self.tension.close()
		except :
			pass
		try :
			self.voltage_out.close()
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