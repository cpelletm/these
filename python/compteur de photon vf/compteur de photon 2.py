import sys
import time
import random
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.task
import nidaqmx.system

import numpy as np

from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure




class Photon_Counter(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #default integration time in s
        self.dt=0.03

        #Total number of points in the plot
        N=500


        ##Creation of the graphical interface##

        self.main = QWidget()
        self.setCentralWidget(self.main)

        layout= QHBoxLayout()
        Vbox_gauche=QVBoxLayout()
        Vbox = QVBoxLayout()
        Vbox_droite=QVBoxLayout()


        layout.addLayout(Vbox_gauche)
        layout.addLayout(Vbox)
        layout.addLayout(Vbox_droite)
        self.main.setLayout(layout)

        #Buttons on the right
        stop=QPushButton('Stop')
        start=QPushButton('Start')
        
        Vbox_droite.addWidget(start)
        Vbox_droite.addWidget(stop)
        
        #Labels on the left
        gras=QFont( "Arial", 40, QFont.Bold)

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

        
        #Plot in the middle + toolbar

        dynamic_canvas = FigureCanvas(Figure(figsize=(10, 5)))
        Vbox.addStretch(1)
        Vbox.addWidget(dynamic_canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))


        ## Matplotlib Setup ##

        self.dynamic_ax = dynamic_canvas.figure.subplots()
        self.t=np.zeros(N)
        self.y=np.zeros(N)
        
        self.line2,=self.dynamic_ax.plot(self.t, self.y)
        
        
        
        
        ## Timer Setup ##

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_canvas)         
        

        start.clicked.connect(self.start_timer)
        stop.clicked.connect(self.timer.stop)

    def update_canvas(self):       
        ##Update the plot and the value of the PL ##


        self.y=np.roll(self.y,-1)
        ctrmaintenant=self.ci.ci_count
        self.y[-1]=(ctrmaintenant-self.ctravant)/self.dt
        self.PL.setText("%3.2E" % self.y[-1])
        self.ctravant=ctrmaintenant
        self.line2.set_ydata(self.y)
        ymax=max(self.y)
        self.dynamic_ax.set_ylim([0,ymax])
        
        self.dynamic_ax.figure.canvas.draw()

    def start_timer(self):
        ## What happens when you click "start" ##

        #Task Creation
        self.task=nidaqmx.Task()
        self.task.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.ci=nidaqmx._task_modules.channels.ci_channel.CIChannel(self.task._handle,'Dev1/ctr0')
        

        #Reset the first "half" of the counter
        self.ctravant=0

        #Read integration time dt
        self.dt=np.float(self.textdt.text())

        #Adjust time axis
        self.t=np.arange(0,N*self.dt,self.dt)
        self.dynamic_line.set_xdata(self.t)
        xmax=max(self.t)
        self.dynamic_ax.set_xlim([0,xmax])

        #Set up the timer rate (in ms)
        self.timer.setInterval(self.dt*1e3)

        #Start the task, then the timer
        self.task.start()
        self.timer.start()

    def stop_timer(self):
        #Stop the timer and clear the task
        self.timer.stop()
        self.task.close()
        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.task.close()