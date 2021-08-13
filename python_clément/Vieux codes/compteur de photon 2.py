import sys
import time
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.task
import nidaqmx.system

import numpy as np

from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow)
#from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure




class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self._main = QWidget()
        self.setCentralWidget(self._main)
        Vbox = QVBoxLayout()
        x=QDesktopWidget.width(self._main)*0.7
        y=QDesktopWidget.height(self._main)*0.7
        #self.setFixedSize(x,y)
        layout= QHBoxLayout()
        layout.addLayout(Vbox)
        stop=QPushButton('Stop')
        start=QPushButton('Start')
        Vbox2=QVBoxLayout()
        Vbox2.addWidget(start)
        Vbox2.addWidget(stop)
        
        layout.addLayout(Vbox2)
        self._main.setLayout(layout)
        #static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        #layout.addWidget(static_canvas)
        #self.addToolBar(NavigationToolbar(static_canvas, self))

        dynamic_canvas = FigureCanvas(Figure(figsize=(10, 5)))
        Vbox.addStretch(1)
        Vbox.addWidget(dynamic_canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        #self._static_ax = static_canvas.figure.subplots()
        self.t = np.linspace(0, 10, 501)
        #self._static_ax.plot(self.t, np.tan(self.t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self.y=np.zeros(len(self.t))
        self.line2,=self._dynamic_ax.plot(self.t, self.y)
        
        self.dt=0.03
        self.task=nidaqmx.Task()
        self.task.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.ci=nidaqmx._task_modules.channels.ci_channel.CIChannel(self.task._handle,'Dev1/ctr0')
        self.task.start()
        
        
        self.timer = QTimer(self)
        self.timer.setInterval(self.dt*1e3)
        self.timer.timeout.connect(self.update_canvas)

        

            
        

        start.clicked.connect(self.start_timer)
        stop.clicked.connect(self.timer.stop)

    def update_canvas(self):
        
        self.y=np.roll(self.y,-1)
        ctrmaintenant=self.ci.ci_count
        self.y[-1]=(ctrmaintenant-self.ctravant)/self.dt
        self.ctravant=ctrmaintenant
        self.line2.set_ydata(self.y)
        ymax=max(self.y)
        self._dynamic_ax.set_ylim([0,ymax])
        
        self._dynamic_ax.figure.canvas.draw()
    def start_timer(self):
        self.ctravant=self.ci.ci_count
        self.timer.start()






qapp = QApplication(sys.argv)
app = ApplicationWindow()
app.show()
qapp.exec_()
app.task.close()