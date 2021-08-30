#To profile the code : @profile above the function tou want to profile, then run "kernprof -l script_to_profile.py" in terminal, then "python -m line_profiler script_to_profile.py.lprof" to visalize


import sys
import os
import traceback
import time
import random
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system
import pyvisa as visa

import numpy as np

# import PyQt6 #Ca a pas du tout l'air compatible
import pyqtgraph as pg 

from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer,QSize)
from PyQt5.QtWidgets import (QWidget, QPushButton, QComboBox,
	QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QErrorMessage, QMessageBox)

qapp = QApplication(sys.argv)

class Graphical_interface(QMainWindow) :
	def __init__(self,*itemLists,title='Unnamed'):
		super().__init__()
		self.setWindowTitle(title)
		main = QWidget()
		self.setCentralWidget(main)
		layout= QHBoxLayout()
		for itemList in itemLists :
			vBox=QVBoxLayout()
			layout.addLayout(vBox)
			if isinstance(itemList,list):
				for item in itemList :
					item.addToBox(vBox)
			else :
				itemList.addToBox(vBox)
		main.setLayout(layout)
		self.resize(1200,800)
		self.show()		
	def run(self):
		qapp.exec_()
	def closeEvent(self, event): #Semble éviter les bugs. Un peu. Si tu veux rajouter des actions à faire en fermant c'est ici
		startStopButton().stop_action(closeAnyway=True)
		self.close()

class label():
	def __init__(self,name,style='normal',spaceAbove=1,spaceBelow=0):
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
		self.label=QLabel(name)
		if style=='BIG' :
			self.label.setFont(QFont( "Consolas", 40, QFont.Bold))
	def setText(self,text):
		self.label.setText(text)
	def addToBox(self,box):
		box.addStretch(self.spaceAbove)
		box.addWidget(self.label)
		box.addStretch(self.spaceBelow)	

class field():
	def __init__(self,name,initial_value='noValue',spaceAbove=1,spaceBelow=0): 
		self.label=QLabel(name)
		self.lect=QLineEdit()
		if initial_value != 'noValue' :
			self.setValue(initial_value)
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
	def updateValue(self):
		try :
			self.v=int(self.lect.text())
		except :
			try :
				self.v=float(self.lect.text())
			except :
				self.v=self.lect.text()
	def setValue(self,new_value):
		self.v=new_value
		if self.v==0:
			self.lect.setText('0')
		elif abs(new_value)>1E4 or abs(new_value) <1E-3 :
			self.lect.setText('%e'%self.v)
		else :
			self.lect.setText(str(self.v))
	def setEnabled(self,b):
		self.label.setEnabled(b)
		self.lect.setEnabled(b)
	def addToBox(self,box):
		box.addStretch(self.spaceAbove)
		box.addWidget(self.label)
		box.addWidget(self.lect)
		self.lect.setFixedSize(QSize(100,20))
		box.addStretch(self.spaceBelow)

class button():
	def __init__(self,name,action=False,spaceAbove=1,spaceBelow=0): 
		self.button=QPushButton(name)
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
		if action :
			self.setAction(action)
	def setAction(self,action):		
			self.button.clicked.connect(action)
	def addToBox(self,box):
		box.addStretch(self.spaceAbove)
		box.addWidget(self.button)
		box.addStretch(self.spaceBelow)

class checkBox():
	def __init__(self,name,action=False,initialState=False,spaceAbove=1,spaceBelow=0): 
		self.cb=QCheckBox(name)
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
		self.setState(initialState)
		if action :
			self.setAction(action)		
	def setAction(self,action):		
			self.cb.stateChanged.connect(action)
	def setState(self,state):
		self.cb.setCheckState(state)
		self.cb.setTristate(False)
	def state(self):
		return(self.cb.isChecked())
	def addToBox(self,box):
		box.addStretch(self.spaceAbove)
		box.addWidget(self.cb)
		box.addStretch(self.spaceBelow)

class dropDownMenu():
	def __init__(self,name,*items,spaceAbove=1,spaceBelow=0):
		self.label=QLabel(name)
		self.cb=QComboBox()
		for item in items :
			self.cb.addItem(item)
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
	def index(self):
		return self.cb.currentIndex()
	def text(self):
		return self.cb.currentText()
	def addToBox(self,box):
		box.addStretch(self.spaceAbove)
		box.addWidget(self.label)
		box.addWidget(self.cb)
		box.addStretch(self.spaceBelow)

class saveButton(button):
	def __init__(self,graphicWidget,autoSave=False,spaceAbove=1,spaceBelow=0): 
		self.gra=graphicWidget
		self.qapp=qapp
		super().__init__("Save data",spaceAbove=spaceAbove,spaceBelow=spaceBelow)
		self.startpath="D:/DATA"
		self.setAction(self.save)
		if autoSave :
			self.gra.autoSave=autoSaveMethod(self,autoSave)

	def save(self,fname=False,saveData=True,saveFigure=True):
		#lines=get_objects(pg.graphicsItems.PlotDataItem.PlotDataItem) #C'est cradingue mais ça devrait fonctionner si besoin
		start = os.path.join(self.startpath, "data")
	
		if not fname :
			fname, filter = QFileDialog.getSaveFileName(self.button.parent(),
										 "Choose a filename to save to",
										 start, "Images (*.png)")
		self.startpath = os.path.dirname(fname)

		if saveData :
			fdataname=fname[:-4]+".csv"
			import csv
			with open(fdataname,'w',newline='') as csvfile :
				spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				for line in self.gra.lines :
					data=line.getData()
					spamwriter.writerow(data[0])
					spamwriter.writerow(data[1])


		if saveFigure :
			self.qapp.primaryScreen().grabWindow(self.gra.parentWidget().winId()).save(fname,'png')

class keepTraceButton():
	def __init__(self,graph,*lines,spaceAbove=1,spaceBelow=0):
		self.keepButton=button("Keep Trace",self.keepTrace,spaceAbove=spaceAbove,spaceBelow=0)
		self.clearButton=button("Clear Trace",self.clearTrace,spaceAbove=0,spaceBelow=spaceBelow)
		self.graph=graph
		self.lines=lines
		self.axes=[]
		for line in self.lines : 
			self.axes+=[line.ax]

	def keepTrace(self):
		for line in self.lines :
			data=line.getData()
			x=data[0]
			y=data[1]
			ax=line.ax
			trace=self.graph.addLine(x,y,ax=ax,typ='trace')


	def clearTrace(self):
		for ax in self.axes :
			curves=ax.curves
			if curves[-1].typ=='trace' :
				c=curves[-1]
				self.graph.lines.remove(c)
				ax.removeItem(c)
				ax.currentPenIndex-=1

	def addToBox(self,box):
		self.keepButton.addToBox(box)
		self.clearButton.addToBox(box)

class autoSaveMethod():
	def __init__(self,saveButton,delay=10,saveFigure=True,saveData=True): #delay in minutes
		self.time_last_save=time.time()
		self.delay_s=delay*60
		self.sb=saveButton
		self.saveFigure=saveFigure
		self.saveData=saveData
	def check(self):
		if time.time() > self.time_last_save + self.delay_s :
			from datetime import datetime
			now = datetime.now()
			date_str=now.strftime("%Y-%m-%d %H-%M-%S")
			filename='D:/DATA/AutoSave/'+date_str+'.png'
			self.sb.save(fname=filename,saveData=self.saveData,saveFigure=self.saveFigure)
			self.time_last_save=time.time()

class startStopButton():
	def __init__(self,setup=False,update=False,spaceAbove=1,spaceBelow=0,resetAO=False, debug=False, maxIter=np.infty, lineIter=False, showMaxIter=False):
		self.setup=setup
		self.updateFunc=update
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
		self.resetAO=resetAO
		self.debug=debug
		self.maxIter=maxIter
		self.lineIter=lineIter
		self.showMaxIter=showMaxIter
		self.startButton=button('Start',self.start_action, spaceAbove=spaceAbove, spaceBelow=0)
		if self.showMaxIter :
			self.stopButton=button('Stop',self.stop_action, spaceAbove=0, spaceBelow=0)
			self.maxIterWidget=field('Max number',self.maxIter,spaceAbove=0, spaceBelow=spaceBelow)
		else :
			self.stopButton=button('Stop',self.stop_action, spaceAbove=0, spaceBelow=spaceBelow)
		self.stopButton.button.setEnabled(False)
		self.timer=QTimer()


	def start_action(self):
		self.startButton.button.setEnabled(False)
		self.stopButton.button.setEnabled(True)
		if self.showMaxIter :
			self.maxIter=val(self.maxIterWidget)
		lines=get_objects(myLine)
		for line in lines :
			line.iteration=1
		if self.setup :
			self.updateArgs=failSafe(self.setup,debug=self.debug) #il va peut etre tej le failSafe
		if self.updateFunc :
			self.timer.timeout.connect(self.updateAction)
			self.timer.start()

	def updateAction(self):
		if self.lineIter :
			if self.lineIter.iteration > self.maxIter :
				self.stop_action()
				return	
		
		if isinstance(self.updateArgs,None.__class__) : #C'est déguelasse mais autrement numpy casse les couilles
			failSafe(self.updateFunc,debug=self.debug)
		elif isinstance(self.updateArgs,tuple) :
			failSafe(self.updateFunc,*self.updateArgs,debug=self.debug)
		else :
			failSafe(self.updateFunc,self.updateArgs,debug=self.debug)

	def stop_action(self,closeAnyway=False): #C'est un peu brut mais bon ça fonctionne
		self.timer.stop() #doublon mais bon
		tasks=get_subclass(NIChan)
		for task in tasks :
			if task.task._handle is not None  and (task.toBeStopped or closeAnyway): #sinon il essaie de fermer des taches qui n'existent plus et ça fout des warnings
				task.close()	
		if self.resetAO :
			for i in range(2):
				with nidaqmx.Task() as tension :
					tension.ao_channels.add_ao_voltage_chan('Dev1/ao%i'%i)
					tension.write(0)
					tension.start()
		mws=get_objects(microwave)
		for mw in mws :
			mw.close()
		timers=get_objects(QTimer)
		for timer in timers :
			timer.stop()
		self.startButton.button.setEnabled(True)
		self.stopButton.button.setEnabled(False)

	def addToBox(self,box):
		self.startButton.addToBox(box)
		self.stopButton.addToBox(box)
		if self.showMaxIter :
			self.maxIterWidget.addToBox(box)

class microwave():
	def __init__(self,ressourceName='mw_ludo',timeout=8000): #timeout in ms
		if ressourceName=='mw_ludo' :
			ressourceName='TCPIP0::micro-onde.phys.ens.fr::inst0::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"
		self.PG = visa.ResourceManager().open_resource( ressourceName )
		self.PG.write_termination = '\n'
		self.PG.timeout=timeout
		self.PG.clear()  # Clear instrument io buffers and status
		self.PG.write('*WAI')

	def create_list_freq(self,fmin,fmax,level,n_points) :
		#Frequecy given in MHz
			freq_list=np.linspace(fmin,fmax,n_points)
			instruction_f='SOUR:LIST:FREQ'
			for f in freq_list :
				if f==max(freq_list) :
					instruction_f+=' %f MHz'%f
				else :
					instruction_f+=' %f MHz,'%f
			instruction_pow='SOUR:LIST:POW'
			for f in freq_list :
				if f==max(freq_list) :
					instruction_pow+=' %f dBm'%level
				else :
					instruction_pow+=' %f dBm,'%level
			return instruction_f,instruction_pow

	def setupESR(self,F_min=2800,F_max=2950,Power=-10,N_points=201,mod=None,AM_Depth=100):

		fmin=val(F_min) #Note : ce serait possible d'automatiser tout ça avec du exec() mais après y'a moyen que ca casse tout, donc on va éviter
		fmax=val(F_max)
		n=val(N_points)
		depth=val(AM_Depth)
		lvl=val(Power)

		freq_list,pow_list=self.create_list_freq(fmin,fmax,lvl,n)

		self.PG.write(':LIST:DELete:ALL')
		self.PG.write('*WAI')

		if mod=='AM' :
			self.PG.write(':SOUR:AM:SOUR EXT')
			self.PG.write('*WAI')

			self.PG.write(':SOUR:AM:DEPT %f'%depth)
			self.PG.write('*WAI')

			self.PG.write(':SOUR:AM:STATe ON')
			self.PG.write('*WAI')


		self.PG.write('LIST:SEL "new_list"') #Il lui faut un nom, j'espere qu'il y a pas de blagues si je réécris dessus
		self.PG.write('*WAI')

		self.PG.write(freq_list)
		self.PG.write('*WAI')

		self.PG.write(pow_list)
		self.PG.write('*WAI')

		self.PG.write('LIST:LEAR') #Peut etre bien facultatif
		self.PG.write('*WAI')

		self.PG.write('LIST:MODE STEP')
		self.PG.write('*WAI')

		self.PG.write('LIST:TRIG:SOUR EXT')
		self.PG.write('*WAI')

		self.PG.write('OUTP ON') #OFF/ON pour allumer éteindre la uW
		self.PG.write('*WAI')

		self.PG.write('FREQ:MODE LIST') #on doit allumer la uW avant de passer en mode liste
		self.PG.write('*WAI')

		self.PG.write('LIST:RES') #Ca par contre ca a l'air de jouer curieusement
		self.PG.write('*WAI')

	def setupContinuous(self,Frequency=2800,Power=-10,mod=None,AC_Depth=100):
		f=val(Frequency)
		lvl=val(Power)
		depth=val(AC_Depth)

		if mod=='AC' :
			self.PG.write(':SOUR:AM:SOUR EXT')
			self.PG.write('*WAI')

			self.PG.write(':SOUR:AM:DEPT %f'%depth)
			self.PG.write('*WAI')

			self.PG.write(':SOUR:AM:STATe ON')
			self.PG.write('*WAI')

		self.PG.write('FREQ %f MHz'%f)
		self.PG.write('*WAI')

		self.PG.write('POW %f dBm'%lvl)
		self.PG.write('*WAI')

		self.PG.write('OUTP ON')
		self.PG.write('*WAI')

	def close(self):

		self.PG.write('*RST')
		self.PG.write('*WAI')

class useTheme():
	def __init__(self,theme):
		self.theme=theme
		if theme=='white' :
			pg.setConfigOption('background', 'w')
			pg.setConfigOption('foreground', 'k')			
			self.penColors=[(31, 119, 180),(255, 127, 14),(44, 160, 44),(214, 39, 40),(148, 103, 189),(140, 86, 75),(227, 119, 194),(127, 127, 127),(188, 189, 34),(23, 190, 207)] #j'ai volé les couleurs de matplotlib

		# pg.setConfigOptions(antialias=False)	
	def nextLine(self,ax,typ=False):
		if typ=='trace' :
			pen=pg.mkPen(self.penColors[ax.currentPenIndex%len(self.penColors)],width=2,style=Qt.DashDotLine) #ëvisiblement y'a moyen de faire ça avec iter() et next() mais c'est pas mal non plus ça
			symbol=None
			symbolPen=None
			symbolBrush=None
		else :
			pen=pg.mkPen(self.penColors[ax.currentPenIndex%len(self.penColors)],width=3,style=Qt.SolidLine)
			symbol='o'
			symbolPen=pen
			symbolBrush=pg.mkBrush(None)

		ax.currentPenIndex+=1
		return pen,symbol,symbolPen,symbolBrush

class NIChan():
	def __init__(self,*physicalChannels):
		self.trigged=False
		self.running=False
		self.nAvg=1
		self.toBeStopped=True
		self.setChannels(*physicalChannels)
	def setChannels(self,*physicalChannels):
		self.physicalChannels=physicalChannels
		self.nChannels=len(physicalChannels)
	def triggedOn(self,channels):
		self.task.triggers.start_trigger.cfg_dig_edge_start_trig(channels.triggerSignal)
		self.task.triggers.start_trigger.retriggerable=True
		self.trigged=True
		self.start()
	def timeAxis(self):
		n=int(self.sampsPerChan/self.nAvg)
		return(np.linspace(0,self.sampsPerChan/self.samplingRate,n))
	def start(self):
		self.task.start()
		self.running=True
	def close(self):
		self.task.close()

class AOChan(NIChan):
	def __init__(self,*physicalChannels): #Physical Channels = 'ao0' or 'ao1'	
		super().__init__(*physicalChannels)	
		self.triggerSignal='/Dev1/ao/StartTrigger'		
	def createTask(self):
		self.task=nidaqmx.Task()
		for pc in self.physicalChannels :
			cname='Dev1/'+pc
			self.task.ao_channels.add_ao_voltage_chan(cname)	
	def setupContinuous(self,Value): #Starts immediately
		self.createTask()
		self.value=val(Value)
		self.task.write(self.value)
		self.task.start()
	def updateContinuous(self,Value):
		self.value=val(Value)
		self.task.write(self.value)
	def setupTimed(self,SampleFrequency,ValuesList,SampleMode='finite'): #sampleMode = 'finite' or 'continuous' ; ValuesList example : [[1,0.5,0],[3,2.5,3]] for two AO channels
		self.createTask()
		self.samplingRate=val(SampleFrequency)
		self.signal=val(ValuesList)
		if self.nChannels==1:
			self.sampsPerChan=len(self.signal)
		else :
			self.sampsPerChan=len(self.signal[0]) #pas sur que ça marche ça, faudrait passer en numpy pour être clean
		if SampleMode=='finite':
			self.sampleMode=nidaqmx.constants.AcquisitionType.FINITE
		elif SampleMode=='continuous':
			self.sampleMode=nidaqmx.constants.AcquisitionType.CONTINUOUS
		self.task.timing.cfg_samp_clk_timing(self.samplingRate,sample_mode=self.sampleMode, samps_per_chan=self.sampsPerChan)
		self.task.write(self.signal)

class AIChan(NIChan):
	def __init__(self,*physicalChannels,extendedRange=[-10,10]): #Physical Channels = 'ai0' to 'ai15'; if extendedRange=False : Vmin=-5 V and Vmax=+5 V		
		super().__init__(*physicalChannels)	
		self.triggerSignal='/Dev1/ai/StartTrigger'
		self.extendedRange=extendedRange
	def createTask(self):
		self.task=nidaqmx.Task()
		for pc in self.physicalChannels :
			cname='Dev1/'+pc
			if self.extendedRange :
				self.task.ai_channels.add_ai_voltage_chan(cname,min_val=self.extendedRange[0],max_val=self.extendedRange[1])
			else :
				self.task.ai_channels.add_ai_voltage_chan(cname)
	def setupSingle(self):
		self.createTask()
	def setupTimed(self,SampleFrequency,SamplesPerChan,SampleMode='finite',nAvg=1): 
	#sampleMode = 'finite' or 'continuous' ; nAvg=average over n point for each sample
		self.createTask()
		self.nAvg=val(nAvg)
		self.samplingRate=val(SampleFrequency)*self.nAvg
		self.sampsPerChan=val(SamplesPerChan)*self.nAvg
		if SampleMode=='finite':
			self.sampleMode=nidaqmx.constants.AcquisitionType.FINITE
		elif SampleMode=='continuous':
			self.sampleMode=nidaqmx.constants.AcquisitionType.CONTINUOUS
		self.task.timing.cfg_samp_clk_timing(self.samplingRate,sample_mode=self.sampleMode, samps_per_chan=self.sampsPerChan)
	def readTimed(self,waitForAcqui=False):
		if self.sampleMode==nidaqmx.constants.AcquisitionType.CONTINUOUS:
			data=self.task.read(self.sampsPerChan)
			return average(data,self.nAvg) #je gère pas le multi channel en continuous. Faut pas utiliser continuous de toute facon

		if not self.running:
			self.start()

		if waitForAcqui :
			self.task.wait_until_done()

		if self.task.is_task_done() :
			data=self.readAndStop(self.sampsPerChan)
		else :
			return False

		data=np.array(data)
		if self.nChannels==1 :
			return average(data,self.nAvg)
		else :
			res=[]
			for k in range(self.nChannels):
				res+=[average(data[k,:],self.nAvg)]
			res=tuple(res)
			return(res)

	
	def readSingle(self):
		return self.task.read()
	def readAndStop(self,sampsPerChan):
		data=self.task.read(sampsPerChan)
		self.task.stop()
		self.running=False
		return data

class DOChan(NIChan):
	def __init__(self,*physicalChannels): #Physical Channels = 'p01' to 'p27' (p10 to p27 cannot be used in timed mode (I think, never understood what PFI were))		
		super().__init__(*physicalChannels)	
		self.triggerSignal='/Dev1/do/StartTrigger'	
	def createTask(self):
		self.task=nidaqmx.Task()
		for pc in self.physicalChannels :
			cname='Dev1/port'+pc[1]+'/line'+pc[2]
			self.task.do_channels.add_do_chan(cname)	
	def setupContinuous(self,Value): #Starts immediately. A noter que la c'est pour du continu constant, il faudrait éventuellement faire autre chose pour du continu avec un motif qui se répète
		self.createTask()
		self.value=val(Value)
		self.task.write(self.value)
		self.task.start()
	def updateContinuous(self,Value):
		self.value=val(Value)
		self.task.write(self.value)
	def setupTimed(self,SampleFrequency,ValuesList,SampleMode='finite'): #sampleMode = 'finite' or 'continuous' ; ValuesList example : [[True,False,True],[True,True,True]] for two DO channels
		self.createTask()
		self.samplingRate=val(SampleFrequency)
		self.signal=val(ValuesList) #je vois pas dans quelle situation c'est utile
		if self.nChannels==1:
			self.sampsPerChan=len(self.signal)
		else :
			self.sampsPerChan=len(self.signal[0]) #pas sur que ça marche ça, faudrait passer en numpy pour être clean
		if SampleMode=='finite':
			self.sampleMode=nidaqmx.constants.AcquisitionType.FINITE
		elif SampleMode=='continuous':
			self.sampleMode=nidaqmx.constants.AcquisitionType.CONTINUOUS
		self.task.timing.cfg_samp_clk_timing(self.samplingRate,sample_mode=self.sampleMode, samps_per_chan=self.sampsPerChan)
		self.task.write(self.signal)

class COChan(NIChan):
	def __init__(self,*physicalChannels): #Physical Channels = 'p01' to 'p27' (p10 to p27 cannot be used in timed mode (I think, never understood what PFI were))		
		super().__init__(*physicalChannels)	
		self.triggerSignal='/Dev1/co/StartTrigger'	#Pas sur avec le ArmStartTrigger, ce sera à vérifier. C'est la merde les trigg avec les compteurs
	def createTask(self,freq):
		self.task=nidaqmx.Task()
		for pc in self.physicalChannels :
			cname='Dev1/'+pc
			self.task.co_channels.add_co_pulse_chan_freq('Dev1/ctr0',freq=freq)
	def setupContinuous(self,Freq): #Starts immediately
		self.createTask((val(Freq)))		
		self.task.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,samps_per_chan=10)
		self.task.start()

class graphics(pg.GraphicsLayoutWidget) :
	def __init__(self,theme='white',debug=False):
		self.theme=useTheme(theme)
		super().__init__()		

		
		self.norm=False
		self.autoSave=False
		self.debug=debug
		self.lines=[]
		self.axes=[]
		self.mainAx=self.addAx(where=False)
	def addAx(self,where='bellow',title=None) :
		if where=='bellow' :
			self.nextRow()
		ax=self.addPlot(title=title)
		ax.currentPenIndex=0
		self.axes+=[ax]
		return ax
	def addLine(self,x=[],y=[],ax=False,typ='instant',style='lm',fast=False) : #style= :'l' =line, 'm' = marker, 'lm'=marker+line
		if not ax :
			ax=self.mainAx
		if len(x)==0 :
			x=np.linspace(0,10,100)
		if len(y)==0 :
			y=np.zeros(100)
		line=myLine(x,y,ax,theme=self.theme,typ=typ,style=style,fast=fast)
		self.lines+=[line]
		return line
	def normalize(self,initialState=False,spaceAbove=0,spaceBelow=0):
		self.normWidget=checkBox(name='Normalize',action=self.normalizeActualize,initialState=initialState,spaceAbove=spaceAbove,spaceBelow=spaceBelow)
		return(self.normWidget)
	def normalizeActualize(self):
		self.norm=self.normWidget.state()
		for line in self.lines :
			self.updateLine(line,line.xData,line.trueY)
	def updateLine(self,line,x,y) :		
		if not(isinstance(y,np.ndarray) or isinstance(y,list)) : #sécurité si jamais tu envoies rien, il ne se passe rien
			return
		if not(isinstance(x,np.ndarray) or isinstance(x,list)) :
			x=line.xData
		line.update(x,y,self.norm)

		if self.autoSave :
			self.autoSave.check()

	def addToBox(self,box):
		box.addWidget(self)

class myLine(pg.PlotDataItem) :
	def __init__(self,x,y,ax,theme,typ,style,fast): #typ=='instant','scroll', 'average' or 'trace'
		self.theme=theme
		self.ax=ax
		self.typ=typ
		self.trueY=y #Keep the real unnormalized value of y
		pen,symbol,symbolPen,symbolBrush=self.theme.nextLine(ax,typ=typ)
		if not 'l' in style :
			pen=None
		if not 'm' in style :
			symbolPen=None
		super().__init__(x,y,pen=pen,symbol=symbol,symbolPen=symbolPen,symbolBrush=symbolBrush,antialias=not fast)	#créé la ligne
		ax.addItem(self) #ajoute la ligne à l'axe

		self.iteration=1
		self.iterationWidget=False

	def update(self,x,y,norm):
		oldY=self.trueY
		if self.typ=='instant' :
			newY=y			
		elif self.typ=='average' :
			if np.any(oldY) : #Si il n'y a que des zéeros (donc première itération en pratique), il remplace directement. Mathématqiuement y'en a pas besoin mais sinon c'est galère avec les tailles
				newY=oldY*(1-1/self.iteration)+y/self.iteration
			else :
				newY=y
		elif self.typ=='scroll' :
			n=len(y)
			if n>len(x) :
				raise ValueError('Scroll data length greater than total data')
			elif len(y)==len(x) :
				newY=y
			else :
				newY=np.roll(oldY,-n)
				newY[-n:]=y
		elif self.typ=='trace' :
			newY=y	
		self.trueY=newY
		if norm :
			ytoplot=normalize(self.trueY)
		else :
			ytoplot=self.trueY
		self.setData(x,ytoplot)
		self.iteration+=1
		if self.iterationWidget :
			self.iterationWidget.update(self.iteration)

class iterationWidget():
	def __init__(self,line,spaceAbove=1,spaceBelow=0):
		self.label=QLabel('Iter #1')
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
		line.iterationWidget=self
	def update(self,value):
		self.label.setText('Iter #%i'%value)		
	def addToBox(self,box):
		box.addStretch(self.spaceAbove)
		box.addWidget(self.label)
		box.addStretch(self.spaceBelow)


def average(y,nAvg):
	if len(y)%nAvg!=0 :
		raise ValueError('nAvg does not divide the size of the array')
	yAvg=np.zeros(int(len(y)/nAvg))
	for k in range(len(yAvg)):
		yAvg[k]=sum(y[k*nAvg:(k+1)*nAvg])/nAvg
	return yAvg

def failSafe(func,*args,debug=False):
	try :
		res=func(*args)
		return res
	except Exception as error :		
		tb=traceback.extract_tb(error.__traceback__)
		if debug :
			print(error)
			print(''.join(tb.format()))
			startStopButton().stop_action()
			quit()
		else :
			GUI=get_objects(Graphical_interface)[0]
			startStopButton().stop_action() #
			mb = QMessageBox(GUI)
			mb.setStandardButtons(QMessageBox.Abort)
			mb.setText(error.__str__())
			mb.setInformativeText(''.join(tb.format())) #un peu barbare mais ça fonctionne
			mb.show()

def visualize(*chans): #args must be channels which have been timeSetuped
	offset=0
	graph=pg.plot()
	for chan in chans:
		f=chan.samplingRate
		n=chan.sampsPerChan
		tmax=n/f
		x=np.linspace(0,tmax,n)
		if isinstance(chan,AIChan) :
			x=np.linspace(0,tmax,2*n)
			y=np.array([1,0]*n)
		else :
			y=chan.signal
		y=normalize(y)+offset
		offset+=2
		graph.plot(x,y)


def normalize(y): #y must be an arraylike
	if isinstance(y,list):
		y=np.array(y,dtype=float)
	y=y/max(abs(y))
	return y

def val(x):
	if isinstance(x, field) :
		x.updateValue()
		return x.v
	else :
		return x


def get_objects(cls):
	import gc
	objs=[]
	for obj in gc.get_objects():
		if isinstance(obj, cls):
			objs+=[obj]
	return(objs)

def get_subclass(cls):
	import gc
	objs=[]
	for obj in gc.get_objects():
		if issubclass(obj.__class__, cls):
			objs+=[obj]
	return(objs)

def test_pg():
	def setup():
		return(np.linspace(0,10,100))
	def update(x):
		y=2*np.cos(x+time.time())
		gra.updateLine(l3,False,y)
		y0=np.cos(time.time())
		gra.updateLine(l1,False,[y0])
	def avertissement():
		mb = QMessageBox(GUI)
		mb.setText('Attention !')
		mb.show()
	x=np.linspace(0,10,100)
	y=np.cos(x)
	gra=graphics()
	l1=gra.addLine(x,y,typ='scroll')
	l2=gra.addLine(x,-y)
	ax2=gra.addAx()
	l3=gra.addLine(x,-y,ax=ax2,typ='instant')

	ftoto=field('toto',10,spaceBelow=1)
	attention=button('Warning',avertissement)



	StartStop=startStopButton(setup=setup,update=update,debug=True,lineIter=l3,showMaxIter=True)
	save=saveButton(gra,autoSave=10)
	trace=keepTraceButton(gra,l3)
	it=iterationWidget(l3)
	norm=gra.normalize()

	buttons=[norm,StartStop,trace,save,it]
	GUI=Graphical_interface([ftoto,attention],gra,buttons,title='Example GUI')

	GUI.run()




if __name__ == "__main__":
	test_pg()


