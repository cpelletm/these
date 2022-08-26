import sys
import nidaqmx
import nidaqmx.task
import pyvisa as visa
from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
	QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QComboBox)

class Photon_Counter(QMainWindow):
	def __init__(self):
		super().__init__()
		layout= QHBoxLayout()
		self.setWindowTitle("Control uW")
		self.main = QWidget()
		self.setCentralWidget(self.main)
		Vbox_gauche = QVBoxLayout()
		Vbox_right = QVBoxLayout()
		Vbox_right2 = QVBoxLayout()
		layout.addLayout(Vbox_gauche)
		layout.addLayout(Vbox_right)
		layout.addLayout(Vbox_right2)
		self.main.setLayout(layout)

		self.frequency=2800
		self.power=0


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


		self.stop=QPushButton('stop')
		self.start=QPushButton('start')
		Vbox_right.addWidget(self.start)
		Vbox_right.addWidget(self.stop)

		self.AM_on=QPushButton('AM On')
		self.AM_off=QPushButton('AM off')
		Vbox_right2.addWidget(self.AM_on)
		Vbox_right2.addWidget(self.AM_off)

		self.stop.setEnabled(False)
		self.start.setEnabled(True) 
		self.start.clicked.connect(self.open_uW)
		self.stop.clicked.connect(self.close_uW)
		self.AM_on.clicked.connect(self.open_AM)
		self.AM_off.clicked.connect(self.close_AM)

		#uW réseau : TCPIP0::micro-onde.phys.ens.fr::inst0::INSTR
		# USB0::0x0AAD::0x0054::110140::0::INSTR

		resourceString4 = 'TCPIP0::micro-onde.phys.ens.fr::inst0::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"

		rm = visa.ResourceManager()
		self.PG = rm.open_resource( resourceString4 )
		self.PG.write_termination = '\n'

		

	def open_uW(self):
		self.stop.setEnabled(True)
		self.start.setEnabled(False) 
		self.frequency=float(self.lectfrequency.text())
		self.power=float(self.lectpower.text())

		self.PG.clear()  # Clear instrument io buffers and status
		self.PG.write('*WAI')
		self.PG.write('FREQ %f MHz'%self.frequency)
		self.PG.write('*WAI')
		self.PG.write('POW %f dBm'%self.power)
		self.PG.write('*WAI')
		self.PG.write('OUTP ON')
		self.PG.write('*WAI')
		

			
	def close_uW(self):
		self.PG.write('*RST')
		self.PG.write('*WAI')
		self.stop.setEnabled(False)
		self.start.setEnabled(True) 

	def open_AM(self):
		self.PG.write(':SOUR:AM:SOUR EXT')
		self.PG.write('*WAI')
		self.PG.write(':SOUR:AM:DEPT 50')
		self.PG.write('*WAI')
		self.PG.write(':SOUR:AM:STATe ON')
		self.PG.write('*WAI')  

	def close_AM(self):
		self.PG.write(':SOUR:AM:STATe OFF')
		self.PG.write('*WAI') 
	
		

qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
		