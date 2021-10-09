import sys
import time
import random
import os


import numpy as np


from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QComboBox)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


#This is a photon counter for the NI 6341 card when the TTL signal is plugged into ctr0/source which is on pin PFI8/P2.0/81



class Photon_Counter(QMainWindow):
    def __init__(self):
        super().__init__()
        
        

        

        

        ##Creation of the graphical interface##

        self.setWindowTitle("Photon Counter")

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
        self.reset=QPushButton('Clear File')
        
        Vbox_gauche.addWidget(self.open)
        Vbox_gauche.addWidget(self.choseline)
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

    def clean_plot(self):
        self.ax.clear()
        self.ax.figure.canvas.draw()
        


        

        
        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
