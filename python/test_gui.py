
import sys
import time
import random
import numpy as np

from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class FenetrteTest(QMainWindow) :
    def __init__(self):
        super().__init__()

        self.main = QWidget()
        self.setCentralWidget(self.main)

    def layout1(self):

        self.dt=0.03

        gras=QFont( "Arial", 40, QFont.Bold)

        self.main = QWidget()
        self.setCentralWidget(self.main)
        Vbox = QVBoxLayout()
        
        layout= QHBoxLayout()
        Vbox_gauche=QVBoxLayout()
        layout.addLayout(Vbox_gauche)
        layout.addLayout(Vbox)
        stop=QPushButton('Stop')
        start=QPushButton('Start')
        Vbox2=QVBoxLayout()
        Vbox2.addWidget(start)
        Vbox2.addWidget(stop)
        
        layout.addLayout(Vbox2)
        self.main.setLayout(layout)
        

        dynamic_canvas = FigureCanvas(Figure(figsize=(10, 5)))
        Vbox.addStretch(1)
        Vbox.addWidget(dynamic_canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        self.textdt=QLineEdit(str(self.dt))
        self.labeldt=QLabel("dt (s) ")   
        self.labelPL=QLabel("photocounts (s-1)") 
        self.PL=QLabel()
        self.PL.setFont(gras)

        Vbox_gauche.addWidget(self.labelPL)
        Vbox_gauche.addWidget(self.PL)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.labeldt)
        Vbox_gauche.addWidget(self.textdt)

        self.dynamic_ax = dynamic_canvas.figure.subplots()
        self.t=np.arange(0,501*self.dt,self.dt)
        self.y=np.zeros(len(self.t))
        
        self.dynamic_line,=self.dynamic_ax.plot(self.t, self.y)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_layout1)

         
        start.clicked.connect(self.start_timer)
        stop.clicked.connect(self.timer.stop)

    def update_layout1(self):
        
        self.y=np.roll(self.y,-1)
        self.y[-1]=np.sin(time.time())**2
        self.PL.setText("%3.2E" % self.y[-1])
        self.dynamic_line.set_ydata(self.y)
        ymax=max(self.y)*1.05
        self.dynamic_ax.set_ylim([0,ymax])
        
        self.dynamic_ax.figure.canvas.draw()

    def start_timer(self):
        self.dt=np.float(self.textdt.text())
        self.t=np.arange(0,501*self.dt,self.dt)
        self.dynamic_line.set_xdata(self.t)
        xmax=max(self.t)
        self.dynamic_ax.set_xlim([0,xmax])
        self.timer.setInterval(self.dt*1e3)
        self.timer.start()



qapp = QApplication(sys.argv)
app = FenetrteTest()
app.layout1()
app.show()
qapp.exec_()