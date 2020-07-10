import sys
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
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QSlider)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class Servo_control(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Servo target")

        self.slider=QSlider()
        self.slider.minimum=0
        self.slider.maximum=180
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)


        self.main = QWidget()
        self.setCentralWidget(self.main)

        layout= QHBoxLayout()

        layout.addWidget(self.slider)

        self.main.setLayout(layout)

        self.slider.sliderReleased.connect(self.getTarget)

    def getTarget(self):
    	self.target=self.slider.value()
    	self.moveServo()

    def moveServo(self):
    	with nidaqmx.Task() as task:
	        task.ao_channels.add_ao_voltage_chan('Dev1/ao1')
	        tension=self.target*5./180.
	        task.write(tension)
	        time.sleep(0.5)



qapp = QApplication(sys.argv)
app = Servo_control()
app.show()
qapp.exec_()


