#C'est un vieux code mais il marche bien et j'ai la flemme de l'actualiser

import sys

import numpy as np

import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system

from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
	QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QComboBox)


class Photon_Counter(QMainWindow):
	def __init__(self):
		super().__init__()

		self.V=0



		self.setWindowTitle("Control Voltage")

		self.main = QWidget()
		self.setCentralWidget(self.main)

		layout= QVBoxLayout()
		Hbox_haut_haut=QVBoxLayout()
		Hbox_haut=QHBoxLayout()
		Hbox = QHBoxLayout()
		Hbox_bas=QHBoxLayout()
		Hbox_bas_bas=QHBoxLayout()

		layout.addLayout(Hbox_haut_haut)
		layout.addLayout(Hbox_haut)
		layout.addLayout(Hbox)
		layout.addLayout(Hbox_bas)
		layout.addLayout(Hbox_bas_bas)
		self.main.setLayout(layout)

		self.source_menu=QComboBox()
		self.source_menu.addItem('Source 1')
		self.source_menu.addItem('Source 2')
		Hbox_haut_haut.addWidget(self.source_menu)

		self.textV=QLineEdit(str(self.V))

		self.plusdix1=QPushButton('+10^-1')
		self.plusdix2=QPushButton('+10^-2')
		self.plusdix3=QPushButton('+10^-3')

		self.apply_button=QPushButton("apply")

		self.moinsdix1=QPushButton('-10^-1')
		self.moinsdix2=QPushButton('-10^-2')
		self.moinsdix3=QPushButton('-10^-3')

		self.zero_hyst_button=QPushButton('Zero Hysteresys')

		Hbox_haut.addWidget(self.plusdix1)
		Hbox_haut.addWidget(self.plusdix2)
		Hbox_haut.addWidget(self.plusdix3)

		Hbox.addWidget(self.textV)
		Hbox.addWidget(self.apply_button)

		Hbox_bas.addWidget(self.moinsdix1)
		Hbox_bas.addWidget(self.moinsdix2)
		Hbox_bas.addWidget(self.moinsdix3)

		Hbox_bas_bas.addWidget(self.zero_hyst_button)

		self.apply_button.clicked.connect(self.apply_voltage)

		self.plusdix1.clicked.connect(self.pdix1)
		self.plusdix2.clicked.connect(self.pdix2)
		self.plusdix3.clicked.connect(self.pdix3)

		self.moinsdix1.clicked.connect(self.mdix1)
		self.moinsdix2.clicked.connect(self.mdix2)
		self.moinsdix3.clicked.connect(self.mdix3)

		self.zero_hyst_button.clicked.connect(self.zero_hyst)

	def apply_voltage(self):
		self.V=float(self.textV.text())
		with nidaqmx.Task() as task:
			source=self.source_menu.currentIndex()
			task.ao_channels.add_ao_voltage_chan('Dev1/ao'+str(source))
			task.write(self.V)
			task.start()

	def pdix1(self):
		self.V=self.V+1e-1
		self.textV.setText(str(self.V))
		self.apply_voltage()

	def pdix2(self):
		self.V=self.V+1e-2
		self.textV.setText(str(self.V))
		self.apply_voltage()

	def pdix3(self):
		self.V=self.V+1e-3
		self.textV.setText(str(self.V))
		self.apply_voltage()

	def mdix1(self):
		self.V=self.V-1e-1
		self.textV.setText(str(self.V))
		self.apply_voltage()

	def mdix2(self):
		self.V=self.V-1e-2
		self.textV.setText(str(self.V))
		self.apply_voltage()

	def mdix3(self):
		self.V=self.V-1e-3
		self.textV.setText(str(self.V))
		self.apply_voltage()

	def zero_hyst(self):
		dt=1E-3
		N=2000
		f_oscill=50

		f_acq=1/dt
		tmax=N*dt
		omega=f_oscill*2*np.pi
		t=np.linspace(0,tmax,N)
		Vlist=np.cos(t*omega)*(tmax-t)/tmax*5
		with nidaqmx.Task() as task:
			source=self.source_menu.currentIndex()
			task.ao_channels.add_ao_voltage_chan('Dev1/ao'+str(source))
			task.timing.cfg_samp_clk_timing(f_acq,sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=N)
			task.write(Vlist)
			task.start()
			while not task.is_task_done() :
				pass









qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()