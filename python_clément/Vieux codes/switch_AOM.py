import sys
import nidaqmx
import nidaqmx.task
from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
	QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QComboBox)

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
		with nidaqmx.Task() as write :
			write.do_channels.add_do_chan('Dev1/port0/line2')
			write.write([True])
			
	def close_AOM(self):
		with nidaqmx.Task() as write :
			write.do_channels.add_do_chan('Dev1/port0/line2')
			write.write([False])

	def open_uW(self):
		with nidaqmx.Task() as write :
			write.do_channels.add_do_chan('Dev1/port0/line3')
			write.write([False])
			
	def close_uW(self):
		with nidaqmx.Task() as write :
			write.do_channels.add_do_chan('Dev1/port0/line3')
			write.write([True])

qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
		