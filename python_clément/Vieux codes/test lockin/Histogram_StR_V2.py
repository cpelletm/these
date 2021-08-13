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
		

		self.dt=0.01 #s
		self.n_bins=40
		self.refresh_rate=0.2 #s

		self.n_glissant=1

		self.xmin=0
		self.xmax=1



		

		##Creation of the graphical interface##

		self.setWindowTitle("Histogramme")

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

		self.labeldt=QLabel("dt")
		self.lectdt=QLineEdit(str(self.dt))
		Vbox_gauche.addWidget(self.labeldt)
		Vbox_gauche.addWidget(self.lectdt)
		Vbox_gauche.addStretch(1)

		self.labeln_glissant=QLabel("n_glissant")
		self.lectn_glissant=QLineEdit(str(self.n_glissant))
		Vbox_gauche.addWidget(self.labeln_glissant)
		Vbox_gauche.addWidget(self.lectn_glissant)
		Vbox_gauche.addStretch(1)

		self.labeln_bins=QLabel("n_bins")
		self.lectn_bins=QLineEdit(str(self.n_bins))
		Vbox_gauche.addWidget(self.labeln_bins)
		Vbox_gauche.addWidget(self.lectn_bins)
		Vbox_gauche.addStretch(1)


		self.labelxmin=QLabel("xmin")
		self.lectxmin=QLineEdit(str(self.xmin))
		Vbox_gauche.addWidget(self.labelxmin)
		Vbox_gauche.addWidget(self.lectxmin)


		self.labelxmax=QLabel("xmax")
		self.lectxmax=QLineEdit(str(self.xmax))
		Vbox_gauche.addWidget(self.labelxmax)
		Vbox_gauche.addWidget(self.lectxmax)
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
		self.inf_line,=self.dynamic_ax.plot(self.x,self.y,color='blue')
		self.sup_line,=self.dynamic_ax.plot(self.x,self.y,color='blue')

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


		
	def auto_xlims(self):
		with nidaqmx.Task() as tension :
			tension.ai_channels.add_ai_voltage_chan("Dev1/ai11")
			tension.timing.cfg_samp_clk_timing(1000,sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=1000)
			tension.start()
			lecture=tension.read(1000)
		self.xmin=min(lecture)
		self.lectxmin.setText('%3.2e'%self.xmin)
		self.xmax=max(lecture)
		self.lectxmax.setText('%3.2e'%self.xmax)



	def update_value(self):
		self.dt=np.float(self.lectdt.text())
		self.n_glissant=np.int(self.lectn_glissant.text())
		self.n_bins=np.int(self.lectn_bins.text())
		self.xmin=np.float(self.lectxmin.text())
		self.xmax=np.float(self.lectxmax.text())
		if self.auto_xlims_cb.isChecked():
			self.auto_xlims()



	def start_measure(self):
		## What happens when you click "start" ##


		self.start.setEnabled(False)
		self.stop.setEnabled(True)

		self.update_value()
		self.f_acq=self.n_glissant/self.dt
		self.n_acq=(int(self.refresh_rate/self.dt)+1)*self.n_glissant
		self.n_points=int(self.refresh_rate/self.dt)+1

		self.time_last_refresh=time.time()





		self.tension=nidaqmx.Task()
		self.tension.ai_channels.add_ai_voltage_chan("Dev1/ai11")
		self.tension.timing.cfg_samp_clk_timing(self.f_acq,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_acq)



		
		self.repeat=1.

		

		#Start the timer     
		self.timer = QTimer(self,interval=0)        
		self.timer.timeout.connect(self.take_point)
		self.tension.start()

		self.mu=0
		self.sigma=0

		self.x=np.linspace(self.xmin,self.xmax,self.n_bins)
		self.y=np.zeros(self.n_bins)
		self.dynamic_line.set_data(self.x,self.y)
		self.fit_line.set_data(self.x,self.y)
		self.dynamic_ax.set_xlim([self.xmin,self.xmax])
		self.timer.start() 
		

		

	def take_point(self):





		lecture_brut=self.tension.read(self.n_acq)

		lecture=np.zeros(self.n_points)
		for i in range(self.n_points) :
			lecture[i]=sum(lecture_brut[i*self.n_glissant:(i+1)*self.n_glissant])/self.n_glissant


		PL=np.histogram(lecture,density=True,bins=self.n_bins,range=[self.xmin,self.xmax])[0]	
		m=statistics.mean(lecture)
		s=statistics.pstdev(lecture)
		
		self.mu=self.mu*(1-1/self.repeat)+m*(1/self.repeat)
		self.sigma=self.sigma*(1-1/self.repeat)+s*(1/self.repeat)
		self.y=self.y*(1-1/self.repeat)+PL*(1/self.repeat)
		self.repeat+=1

		if time.time()-self.time_last_refresh>self.refresh_rate :
			self.time_last_refresh=time.time()


			yplot=self.y
			self.dynamic_line.set_ydata(yplot)
			ymin=min(yplot)
			ymax=max(yplot)
			self.dynamic_ax.set_ylim([ymin,ymax]) 
			yfit=1/(self.sigma*np.sqrt(2*np.pi))*np.exp(-0.5*((self.x-self.mu)/self.sigma)**2)
			self.fit_line.set_ydata(yfit)
			self.fit_line.set_label('mu=%4.3e ; sigma=%4.3e'%(self.mu,self.sigma))
			self.inf_line.set_data([self.mu-self.sigma,self.mu-self.sigma],[ymin,ymax])
			self.sup_line.set_data([self.mu+self.sigma,self.mu+self.sigma],[ymin,ymax])
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
			self.sample_clock.close()
		except :
			pass
		try :
			self.tension.close()
		except :
			pass
		try :
			self.trig_gbf.close()
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
