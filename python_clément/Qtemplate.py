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
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class Window(QMainWindow) :
    def __init__(self,type,titre): #Type = "plot" or "map"
        self.qapp = QApplication(sys.argv)
        super().__init__()
        

        self.setWindowTitle(titre)

        self.main = QWidget()
        self.setCentralWidget(self.main)

        self.layout= QHBoxLayout()
        self.Vbox_left=QVBoxLayout()
        self.fields=[]
        self.Vbox_plot = QVBoxLayout()
        self.Vbox_right=QVBoxLayout()
        self.buttons=[]


        self.layout.addLayout(self.Vbox_left)
        self.layout.addLayout(self.Vbox_plot)
        self.layout.addLayout(self.Vbox_right)
        self.main.setLayout(self.layout)

    def display(self):
        self.show()
        self.qapp.exec_()





    def add_field(self,field_name,param,location='left') : #dtype = 'float' or 'int'
        label=QLabel(field_name)
        field=QLineEdit(str(param.v))
        if location == 'left' :
            self.Vbox_left.addWidget(label)
            self.Vbox_left.addWidget(field)
            self.Vbox_left.addStretch(1)
        elif location == 'right' :
            self.Vbox_right.addWidget(label)
            self.Vbox_right.addWidget(field)
            self.Vbox_right.addStretch(1)

        self.fields+=[[field,param]]

    def update_fields(self):
        for field in self.fields :
            field[1].update(field[0].text())

    







    

class PL():
    def __init__(self,window,location='left'):
        self.PL_display=QLabel("%3.2E" % 0)
        self.PL_display.setFont(QFont( "Consolas", 40, QFont.Bold))
        if location == 'left' :
            window.Vbox_left.addWidget(self.PL_display)
        elif location == 'right' :
            window.Vbox_right.addWidget(self.PL_display)

    def update(self,new_value):
        self.PL_display.setText("%3.2E" % new_value)

class parameter():
    def __init__(self,value):
        self.v=value
        self.dtype=type(self.v)
    def update(self,new_value):
        if self.dtype==type(1):
            self.v=int(new_value)
        elif self.dtype==type(1.):
            self.v=float(new_value)











toto=Window("toto","tutu")
photolum=PL(toto)
toto.display()

