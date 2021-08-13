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
from PyQt5.QtWidgets import (QWidget, QPushButton, 
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
		startStopButton().stop_action()
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
	def __init__(self,name,initial_value=False,spaceAbove=1,spaceBelow=0): 
		self.label=QLabel(name)
		self.lect=QLineEdit()
		if initial_value :
			self.setValue(initial_value)
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
	def updateValue(self):
		temp=np.float(self.lect.text())
		if temp==int(temp):
			temp=int(temp)
		self.v=temp
	def setValue(self,new_value):
		self.v=new_value
		if abs(new_value)>1E4 or abs(new_value) <1E-3 :
			self.lect.setText('%e'%self.v)
		else :
			self.lect.setText(str(self.v))
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
	def __init__(self,name,action=False,spaceAbove=1,spaceBelow=0): 
		self.cb=QCheckBox(name)
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
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
	def __init__(self,setup=False,update=False,spaceAbove=1,spaceBelow=0,zeroAoOut=False, debug=False):
		self.setup=setup
		self.update=update
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
		self.zeroAoOut=zeroAoOut
		self.debug=debug
		self.startButton=button('Start',self.start_action, spaceAbove=spaceAbove, spaceBelow=0)
		self.stopButton=button('Stop',self.stop_action, spaceAbove=0, spaceBelow=spaceBelow)
		self.stopButton.button.setEnabled(False)
		self.timer=QTimer()


	def start_action(self):
		self.startButton.button.setEnabled(False)
		self.stopButton.button.setEnabled(True)
		iters=get_objects(iterationWidget)
		for it in iters :
			it.reset()
		if self.setup :
			failSafe(self.setup,debug=self.debug)
		if self.update :
			self.timer.timeout.connect(self.update)
			self.timer.start()


	def stop_action(self): #C'est un peu brut mais bon ça fonctionne
		tasks=get_objects(nidaqmx.Task)
		for task in tasks :
			if task._handle is not None :
				task.close()	
		if self.zeroAoOut :
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

class microwave():
	def __init__(self,ressourceName='mw_ludo',timeout=8000): #timeout in ms
		if ressourceName=='mw_ludo' :
			ressourceName='TCPIP0::micro-onde.phys.ens.fr::inst0::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"
		self.PG = visa.ResourceManager().open_resource( ressourceName )
		self.PG.write_termination = '\n'
		self.PG.timeout=tiemout
		self.PG.clear()  # Clear instrument io buffers and status
		self.PG.write('*WAI')

	def setupESR(self,F_min=2800,F_max=2950,Power=-10,N_points=201,mod=None,AC_Depth=100):

		fmin=val(F_min) #Note : ce serait possible d'automatiser tout ça avec du exec() mais après y'a moyen que ca casse tout, donc on va éviter
		fmax=val(F_max)
		n=val(N_points)
		depth=val(AC_Depth)
		lvl=val(Power)

		freq_list=np.linspace(fmin,fmax,n)
		pow_list=np.ones(n)*lvl

		self.PG.write(':LIST:DELete:ALL')
		self.PG.write('*WAI')

		if mod=='AC' :
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

		pg.setConfigOptions(antialias=True)	
	def nextLine(self,ax,typ=False):
		if typ=='trace' :
			pen=pg.mkPen(self.penColors[ax.currentPenIndex%len(self.penColors)],width=2,style=Qt.DashDotLine)
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

class AOChan():
	def __init__(self,*physicalChannels): #Physical Channels = 'ao0' or 'ao1'		
		self.nChannels=len(physicalChannels)
		self.triggerSignal='/Dev1/ao/StartTrigger'
		self.physicalChannels=physicalChannels	
		self.trigged=False		
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
	def setupTimed(self,SampleFrequency,ValuesList,sampleMode='finite'): #sampleMode = 'finite' or 'continuous' ; ValuesList example : [[1,0.5,0],[3,2.5,3]] for two AO channels
		self.createTask()
		self.samplingRate=val(SampleFrequency)
		self.signal=val(ValuesList)
		if self.nChannels==1:
			self.sampsPerChan=len(self.signal)
		else :
			self.sampsPerChan=len(self.signal[0]) #pas sur que ça marche ça, faudrait passer en numpy pour être clean
		if sampleMode=='finite':
			self.sampleMode=nidaqmx.constants.AcquisitionType.FINITE
		elif sampleMode=='continuous':
			self.sampleMode=nidaqmx.constants.AcquisitionType.CONTINUOUS
		self.task.timing.cfg_samp_clk_timing(self.samplingRate,sample_mode=sampleMode, samps_per_chan=self.sampsPerChan)
	def triggedOn(self,channels):
		self.task.triggers.start_trigger.cfg_dig_edge_start_trig(channels.triggerSignal)
		self.task.triggers.start_trigger.retriggerable=True
		self.trigged=True
		self.task.start()
	def start(sef):
		self.task.start()
	def close(self):
		self.task.close()

class AIChan():
	def __init__(self,*physicalChannels,extendedRange=[-10,10]): #Physical Channels = 'ai0' to 'ai15'; if extendedRange=False : Vmin=-5 V and Vmax=+5 V		
		self.nChannels=len(physicalChannels)
		self.triggerSignal='/Dev1/ai/StartTrigger'
		self.physicalChannels=physicalChannels
		self.extendedRange=extendedRange
		self.trigged=False
		self.running=False
	def setChannels(self,*physicalChannels):
		self.physicalChannels=physicalChannels
		self.nChannels=len(physicalChannels)
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
	def setupTimed(self,SampleFrequency,SamplesPerChan,sampleMode='finite',nAvg=1): 
	#sampleMode = 'finite' or 'continuous' ; nAvg=average over n point for each sample
		self.createTask()
		self.nAvg=val(nAvg)
		self.samplingRate=val(SampleFrequency)*self.nAvg
		self.sampsPerChan=val(SamplesPerChan)*self.nAvg
		if sampleMode=='finite':
			self.sampleMode=nidaqmx.constants.AcquisitionType.FINITE
		elif sampleMode=='continuous':
			self.sampleMode=nidaqmx.constants.AcquisitionType.CONTINUOUS
		self.task.timing.cfg_samp_clk_timing(self.samplingRate,sample_mode=self.sampleMode, samps_per_chan=self.sampsPerChan)
	def triggedOn(self,channels):
		self.task.triggers.start_trigger.cfg_dig_edge_start_trig(channels.triggerSignal)
		self.task.triggers.start_trigger.retriggerable=True
		self.trigged=True
		self.start()
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
	def start(self):
		self.task.start()
		self.running=True
	def readAndStop(self,sampsPerChan):
		data=self.task.read(sampsPerChan)
		self.task.stop()
		self.running=False
		return data
	def close(self):
		self.task.close()

class graphics(pg.GraphicsLayoutWidget) :
	def __init__(self,theme='white',debug=False):
		self.theme=useTheme(theme)
		super().__init__()		

		
		self.it=False
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
	def addLine(self,x=[],y=[],ax=False,typ='instant',style='lm') : #style= :'l' =line, 'm' = marker, 'lm'=marker+line
		if not ax :
			ax=self.mainAx
		if len(x)==0 :
			x=np.linspace(0,10,100)
		if len(y)==0 :
			y=np.zeros(100)
		line=myLine(x,y,ax,theme=self.theme,typ=typ,style=style)
		self.lines+=[line]
		return line
	def iteration(self,spaceAbove=1,spaceBelow=0) :
		self.it=iterationWidget(spaceAbove=spaceAbove,spaceBelow=spaceBelow)
		return(self.it)
	def normalize(self,initialState=True,spaceAbove=0,spaceBelow=0):
		self.norm=normalizeWidget(initialState=initialState,spaceAbove=spaceAbove,spaceBelow=spaceBelow)
		return(self.norm)
	def updateLine(self,line,x,y) :		
		if self.norm :
			norm=self.norm.state()
		else :
			norm=False
		if not(isinstance(y,np.ndarray) or isinstance(y,list)) :
			return
		if not(isinstance(x,np.ndarray) or isinstance(x,list)) :
			x=line.xData
		line.update(x,y,self.it,norm)

		if self.autoSave :
			self.autoSave.check()

	def addToBox(self,box):
		box.addWidget(self)

class myLine(pg.PlotDataItem) :
	def __init__(self,x,y,ax,theme,typ,style): #typ=='instant','scroll', 'average' or 'trace'
		self.theme=theme
		self.ax=ax
		self.typ=typ
		self.trueY=y #Keep the real unnormalized value of y
		pen,symbol,symbolPen,symbolBrush=self.theme.nextLine(ax,typ=typ)
		if not 'l' in style :
			pen=None
		if not 'm' in style :
			symbolPen=None
		super().__init__(x,y,pen=pen,symbol=symbol,symbolPen=symbolPen,symbolBrush=symbolBrush)	#créé la ligne
		ax.addItem(self) #ajoute la ligne à l'axe

		self.toBeUpdated=False

	def update(self,x,y,iteration,norm):
		oldY=self.trueY
		if self.typ=='instant' :
			newY=y
		elif self.typ=='average' :
			if not self.iteration :
				raise ValueError('You need an iteration to average a measure')
			newY=oldY*(1-1/self.iteration.counter)+y/self.iteration.counter
		elif self.typ=='scroll' :
			n=len(y)
			if n>len(x) :
				raise ValueError('Scroll data length greater than total data')
			elif len(y)==len(x) :
				newY=y
			else :
				newY=np.roll(oldY,-n)
				newY[-n:]=y
		self.trueY=newY
		if norm :
			ytoplot=self.trueY/max(abs(self.trueY))
		else :
			ytoplot=self.trueY
		self.setData(x,ytoplot)

class normalizeWidget(checkBox):
	def __init__(self,initialState,spaceAbove,spaceBelow):
		super().__init__("Normalize",spaceAbove=spaceAbove,spaceBelow=spaceBelow)
		self.setState(initialState)

class iterationWidget():
	def __init__(self,spaceAbove,spaceBelow):
		self.label=QLabel('Iter #1')
		self.counter=1
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
	def increase(self):
		self.counter+=1
		self.label.setText('Iter #%i'%self.counter)
	def reset(self):
		self.counter=1
		self.label.setText('Iter #%i'%self.counter)
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
			startStopButton().stop_action()
			mb = QMessageBox(GUI)
			mb.setStandardButtons(QMessageBox.Abort)
			mb.setText(error.__str__())
			mb.setInformativeText(''.join(tb.format())) #un peu barbare mais ça fonctionne
			mb.show()
			

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


def test_pg():
	def setup():
		pass
	def update():
		x=np.linspace(0,10,100)
		y=2*np.cos(x+time.time())
		gra.updateLine(l3,False,y)
		y0=np.cos(time.time())
		gra.updateLine(l1,False,[y0])
		it.increase()
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



	StartStop=startStopButton(setup=setup,update=update,debug=True)
	save=saveButton(gra,autoSave=10)
	trace=keepTraceButton(gra,l3)
	it=gra.iteration()
	norm=gra.normalize()

	buttons=[norm,StartStop,trace,save,it]
	GUI=Graphical_interface([ftoto,attention],gra,buttons,title='Example GUI')

	GUI.run()




if __name__ == "__main__":
	test_pg()


