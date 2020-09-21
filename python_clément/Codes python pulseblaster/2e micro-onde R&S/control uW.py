import sys
import nidaqmx
import nidaqmx.task
import visa
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
		layout.addLayout(Vbox_gauche)
		layout.addLayout(Vbox_right)
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

		self.stop.setEnabled(False)
		self.start.setEnabled(True) 
		self.start.clicked.connect(self.open_uW)
		self.stop.clicked.connect(self.close_uW)

		resourceString4 = 'USB0::0x0AAD::0x0054::110140::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"

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
		

qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
		