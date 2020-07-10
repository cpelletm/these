


import sys
import time
import random
import os
import matplotlib.pyplot as plt
import numpy as np

from scipy.optimize import curve_fit



from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QComboBox)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


#This is a photon counter for the NI 6341 card when the TTL signal is plugged into ctr0/source which is on pin PFI8/P2.0/81


class curveFitting(): # import numpy as np // from scipy.optimize import curve_fit
    def __init__(self,x,y):
        self.x=np.array(x)
        self.y=np.array(y)
        self.fit=np.zeros(len(x))

        self.coefs=[]

    def lin(self): #fit : ax+b
        A=np.vstack([self.x,np.ones(len(self.x))]).T
        a,b = np.linalg.lstsq(A, self.y, rcond=None)[0]
        self.coefs=[a,b]
        self.fit=a*x+b
        self.label="%3.2Ex+%3.2E"%(a,b)

    def exp(self,tau=1,A=1,B=0): #fit : B+A*exp(-x/tau)
        def f(x,A,B,tau):
            return B+A*np.exp(-x/tau)
        
        #C'est crade mais tant pis il est 19h
        B=self.y[-1]
        A=self.y[0]-self.y[-1]
        tau=self.x[-1]
        p0=[A,B,tau]

        popt, pcov = curve_fit(f, self.x, self.y, p0)
        self.coefs=popt
        A=popt[0]
        B=popt[1]
        tau=popt[2]
        
        self.fit=B+A*np.exp(-self.x/tau)
        self.label="tau=%4.3E"%tau

    def stretch_exp(self,tau=1,A=1,B=0): #fit : B+A*exp(-sqrt(x/tau))
        def f(x,A,B,tau):
            return B+A*np.exp(-np.sqrt(x/tau))
        
        #C'est crade mais tant pis il est 19h
        B=self.y[-1]
        A=self.y[0]-self.y[-1]
        tau=self.x[-1]/3
        p0=[A,B,tau]

        popt, pcov = curve_fit(f, self.x, self.y, p0)
        self.coefs=popt
        A=popt[0]
        B=popt[1]
        tau=popt[2]
        
        self.fit=B+A*np.exp(-np.sqrt(self.x/tau))
        self.label="tau=%4.3E"%tau







class Photon_Counter(QMainWindow):
    def __init__(self):
        super().__init__()
        
        

        

        

        ##Creation of the graphical interface##

        self.setWindowTitle("Data Fit")

        self.main = QWidget()
        self.setCentralWidget(self.main)

        layout= QHBoxLayout()
        Vbox_gauche=QVBoxLayout()
        Vbox = QVBoxLayout()



        layout.addLayout(Vbox_gauche)
        layout.addLayout(Vbox)

        self.main.setLayout(layout)

        #Buttons on the left
        self.open=QPushButton('Open')
        self.choseline=QComboBox()
        self.choseline.setEnabled(False)
        self.fitMenu=QComboBox()
        self.fitMenu.setEnabled(False)
        self.reset=QPushButton('Clear File')
        
        Vbox_gauche.addWidget(self.open)
        Vbox_gauche.addWidget(self.choseline)
        Vbox_gauche.addWidget(self.fitMenu)
        Vbox_gauche.addStretch(1)
        Vbox_gauche.addWidget(self.reset)

        #Plot in the middle

        self.canvas = FigureCanvas(Figure(figsize=(30, 10)))
        self.ax = self.canvas.figure.subplots()
        Vbox.addStretch(1)
        Vbox.addWidget(self.canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        NavigationToolbar(self.canvas, self))



        
              
        #Define the widgets actions 
        

        self.open.clicked.connect(self.get_data)
        self.choseline.activated.connect(self.plot_data)
        self.fitMenu.activated.connect(self.fit_data)
        self.reset.clicked.connect(self.clean_plot)
        

    def get_data(self):
        fname,filters=QFileDialog.getOpenFileName(self,"Chose a data file","./","Data files (*.txt)")
        if fname!= "" :
            self.data=[]
            with open (fname,'r') as f :
                for textLine in f :
                    textLine=textLine.split() #Assumes tab/space as separator; else add the separator here
                    numLine=[]
                    for elem in textLine :
                        try : 
                            numLine+=[float(elem)] #Instructions to skip lines with text
                        except : 
                            break
                    if numLine != [] :
                        self.data+=[numLine]
            self.numLine=int(len(self.data[0])/2) #Data files must have an even number of columns, one for x and one for y
            self.choseline.clear()
            self.choseline.addItem('<none')
            for i in range(self.numLine) :
                self.choseline.addItem('Line %i'%(i+1))
            self.choseline.setEnabled(True)

        






    def plot_data(self):
        index=self.choseline.currentIndex()-1
        if index >= 0 :
            x=[]
            y=[]
            for line in self.data :
                x+=[line[index*2]]
                y+=[line[index*2+1]]
            self.currentLine=np.array([x,y])
            self.ax.plot(x,y)
            self.ax.autoscale()
            self.ax.figure.canvas.draw()


        self.fitMenu.clear()
        self.fitMenu.addItem('<none')

        self.cf=curveFitting(x,y)
        self.listFits=[func for func in dir(self.cf) if (callable(getattr(self.cf, func)) and func[0]!="_")]
        for func in self.listFits :
            self.fitMenu.addItem(func)
        self.fitMenu.setEnabled(True)

    def fit_data(self):
        fitName=self.fitMenu.currentText()
        getattr(self.cf,fitName)()
        self.ax.plot(self.cf.x,self.cf.fit,label=self.cf.label)
        self.ax.legend()
        self.ax.figure.canvas.draw()




    def clean_plot(self):
        self.ax.clear()
        self.ax.figure.canvas.draw()
        


        

        
        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
