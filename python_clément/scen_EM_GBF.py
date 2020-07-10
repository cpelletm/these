import sys
import os
import time
import random
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system
import nidaqmx.constants


import visa
import numpy as np


from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QComboBox)

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure



class Photon_Counter(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.f_cycle=1
        self.f_acq=300

        self.n_acq=int(self.f_acq/self.f_cycle)


       



        

        ##Creation of the graphical interface##

        self.setWindowTitle("Line Scan")

        self.main = QWidget()
        self.setCentralWidget(self.main)

        layout= QHBoxLayout()
        Vbox = QVBoxLayout()
        Vbox_droite=QVBoxLayout()


        layout.addLayout(Vbox)
        layout.addLayout(Vbox_droite)
        self.main.setLayout(layout)




        #Buttons on the right
        self.stop=QPushButton('Stop')
        self.start=QPushButton('Start')

        
        self.labelIter=QLabel("iter # 0")

        
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.start)
        Vbox_droite.addWidget(self.stop)
        Vbox_droite.addStretch(1)
        Vbox_droite.addWidget(self.labelIter)


        self.stop.setEnabled(False)
        
        
        #Plot in the middle
        dynamic_canvas = FigureCanvas(Figure(figsize=(30, 10)))
        Vbox.addStretch(1)
        Vbox.addWidget(dynamic_canvas)
        self.addToolBar(Qt.BottomToolBarArea,
                        MyToolbar(dynamic_canvas, self))
        self.dynamic_ax,self.tension_plot_ax = dynamic_canvas.figure.subplots(2)

        self.t=np.linspace(0,1/self.f_cycle,self.n_acq)
        self.y=np.zeros(self.n_acq)
        self.dynamic_line,=self.dynamic_ax.plot(self.t, self.y)
        self.tension_plot_line,=self.tension_plot_ax.plot(self.t, self.y)





              
        #Define the buttons' action 
        
        self.start.clicked.connect(self.start_measure)
        self.stop.clicked.connect(self.stop_measure)


        

       


    def start_measure(self):
        ## What happens when you click "start" ##


        self.start.setEnabled(False)
        self.stop.setEnabled(True)



        self.t=np.linspace(0,1/self.f_cycle,self.n_acq)
        y_PL=np.zeros(self.n_acq-1)
        y_tension= np.zeros(self.n_acq)


        self.dynamic_line.set_data(self.t[:-1],y_PL)
        self.tension_plot_line.set_data(self.t,y_tension)






        
        self.sample_clock=nidaqmx.Task()
        self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.f_acq)
        self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse


        self.apd=nidaqmx.Task()
        self.apd.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.apd.timing.cfg_samp_clk_timing(self.f_acq,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_acq)

        self.tension=nidaqmx.Task()
        self.tension.ai_channels.add_ai_voltage_chan("Dev1/ai11")
        self.tension.timing.cfg_samp_clk_timing(self.f_acq,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_acq)

        self.trig_gbf=nidaqmx.Task()
        self.trig_gbf.do_channels.add_do_chan('Dev1/port0/line0')
        self.trig_gbf.timing.cfg_samp_clk_timing(self.f_acq,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.n_acq)

        self.tension.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/do/StartTrigger')
        self.sample_clock.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/do/StartTrigger')
        

        signal=[True]+[False]*(self.n_acq-1)
        self.trig_gbf.write(signal)


        self.sample_clock.start()
        self.apd.start()
        self.tension.start()
        


        
        self.repeat=1.
        self.y=np.zeros(self.n_acq-1)
        

        #Start the timer     
        self.timer = QTimer(self,interval=0)        
        self.timer.timeout.connect(self.take_point)

        self.trig_gbf.start()
        self.timer.start() 
        

        

    def take_point(self):





        lecture=self.apd.read(self.n_acq)
        tensions=self.tension.read(self.n_acq) 


        PL=np.array([(lecture[i+1]-lecture[i])*self.f_acq for i in range(len(lecture)-1)])


        
        


        self.tension_plot_line.set_ydata(tensions) 
        ymin=min(tensions)
        ymax=max(tensions)
        self.tension_plot_ax.set_ylim([ymin,ymax]) 
        
        

        if min(PL) >= 0 :
            self.y=self.y*(1-1/self.repeat)+PL*(1/self.repeat)
            self.repeat+=1

        self.dynamic_line.set_ydata(self.y)
        ymin=min(self.y)
        ymax=max(self.y)
        self.dynamic_ax.set_ylim([ymin,ymax]) 

        # print(len(self.dynamic_line.get_xdata()))
        # print(len(self.dynamic_line.get_ydata()))
        # print(len(self.tension_plot_line.get_xdata()))
        # print(len(self.tension_plot_line.get_ydata()))
        self.dynamic_ax.figure.canvas.draw()

        self.labelIter.setText("iter # %i"%self.repeat)
     

    def stop_measure(self):
        #A ameliorer en recuperant dirrectement les tasks depuis system.truc
        try :
            self.timer.stop()
        except :
            pass
        try :
            self.apd.close()
        except :
            pass
        try :
            self.sample_clock.close()
        except :
            pass
        try :
            self.tension.close()
        except :
            pass
        try :
            self.trig_gbf.close()
        except :
            pass
        
        
        


        
        self.stop.setEnabled(False)
        self.start.setEnabled(True)     


class MyToolbar(NavigationToolbar): #Modification of the toolbar to save data with the plot
    
    def save_figure(self, *args): #Requires os and QFileDialog from PyQt5.QtWidgets

        try : #Test if there is a previous path saved
            if self.startpath :
                pass
        except :
            self.startpath="D:/DATA" #Default folder to save at
        
        start = os.path.join(self.startpath, self.canvas.get_default_filename())
        

        fname, filter = QFileDialog.getSaveFileName(self.canvas.parent(),
                                         "Choose a filename to save to",
                                         start, "Images (*.png)")

        data=[]
        for ax in self.canvas.figure.get_axes() :
            for line in ax.get_lines() :
                data+=[line._x]
                data+=[line._y]

        fdataname=fname[:-4]+".txt"
        with open(fdataname,'w') as f: #Needs an update if the lines have differents sizes
            for i in range(len(data[0])) :
                for ligne in data :
                    f.write("%5.4E \t"%ligne[i]) #Format = 5 significative numbers, scientific notation

                f.write("\n")


        if fname:
            # Save dir for next time, unless empty str (i.e., use cwd).
            self.startpath = os.path.dirname(fname)
            try:
                self.canvas.figure.savefig(fname)
            except :
                print('Could not save file !')

        

        






qapp = QApplication(sys.argv)
app = Photon_Counter()
app.show()
qapp.exec_()
app.stop_measure()
