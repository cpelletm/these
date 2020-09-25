import sys
import nidaqmx
import nidaqmx.task
from subprocess import check_output
from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
	QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QComboBox)


#ATTENTION : En pulseblaster tu peux rien lancer en même temps
class Photon_Counter(QMainWindow):
	def __init__(self):
		super().__init__()
		layout= QHBoxLayout()
		self.setWindowTitle("Switch AOM")
		self.main = QWidget()
		self.setCentralWidget(self.main)
		Vbox = QVBoxLayout()
		Vbox_right = QVBoxLayout()
		layout.addLayout(Vbox)
		layout.addLayout(Vbox_right)
		self.main.setLayout(layout)

		self.stop=QPushButton('AOM closed')
		self.start=QPushButton('AOM opened')
		Vbox.addWidget(self.start)
		Vbox.addWidget(self.stop)

		self.stop2=QPushButton('uW closed')
		self.start2=QPushButton('uW opened')
		Vbox_right.addWidget(self.start2)
		Vbox_right.addWidget(self.stop2)

		self.start.clicked.connect(self.open_AOM)
		self.stop.clicked.connect(self.close_AOM)
		self.start2.clicked.connect(self.open_uW)
		self.stop2.clicked.connect(self.close_uW)


	def open_AOM(self):
		def AOM_on():
			with open('PB_instructions.txt','w') as f:
				f.write('label: 0b 0100, 100 ms, branch, label')

		AOM_on()
		check_output('spbicl load pb_instructions.txt 500.0')
		check_output('spbicl start')
			
	def close_AOM(self):
		def AOM_off():
			with open('PB_instructions.txt','w') as f:
				f.write('label: 0b 0000, 100 ms, branch, label')

		AOM_off()
		check_output('spbicl load pb_instructions.txt 500.0')
		check_output('spbicl start')

	def open_uW(self):
		def AOM_on():
			with open('PB_instructions.txt','w') as f:
				f.write('label: 0b 0100, 100 ms, branch, label')

		AOM_on()
		check_output('spbicl load pb_instructions.txt 500.0')
		check_output('spbicl start')
			
	def close_uW(self):
		def uW_off():
			with open('PB_instructions.txt','w') as f:
				f.write('label: 0b 1100, 100 ms, branch, label')

		uW_off()
		check_output('spbicl load pb_instructions.txt 500.0')
		check_output('spbicl start')

qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
		