#To profile the code : @profile above the function tou want to profile, then run "kernprof -l script_to_profile.py" in terminal, then "python -m line_profiler script_to_profile.py.lprof" to visalize

import sys
import os
import traceback
import time
from datetime import datetime
import nidaqmx
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
		resetSetup(closeAnyway=True,stopTimers=True)
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
		if callable(action) :
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
		from pathlib import Path
		#lines=get_objects(pg.graphicsItems.PlotDataItem.PlotDataItem) #C'est cradingue mais ça devrait fonctionner si besoin
		start = os.path.join(self.startpath, "data")
	
		if not fname :
			fname, filter = QFileDialog.getSaveFileName(self.button.parent(),
										 "Choose a filename to save to",
										 start, "Images (*.png)")
		dname=os.path.dirname(fname)
		Path(dname).mkdir(parents=True, exist_ok=True)
		self.startpath = os.path.dirname(dname)
		if len(fname) < 5 or fname[-4]!='.' :
			fname=fname+'.png'
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
			now = datetime.now()
			date_str=now.strftime("%Y-%m-%d %H-%M-%S")
			filename='D:/DATA/AutoSave/'+date_str+'.png'
			self.sb.save(fname=filename,saveData=self.saveData,saveFigure=self.saveFigure)
			self.time_last_save=time.time()

class startStopButton():
	def __init__(self,setup=False,update=False,spaceAbove=1,spaceBelow=0, extraStop=False, debug=False, maxIter=np.infty, lineIter=False, showMaxIter=False,serie=False):
		self.setup=setup
		self.updateFunc=update
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
		self.debug=debug
		self.maxIter=maxIter
		self.lineIter=lineIter
		self.showMaxIter=showMaxIter
		self.serie=serie
		self.extraStop=extraStop
		if self.serie :
			self.serieButton=button('Begin Serie', self.startSerie, spaceAbove=spaceAbove, spaceBelow=0)
			self.serieLabel=label('Acquisition 0/?',spaceAbove=0, spaceBelow=0)
			self.startButton=button('Start',self.startAction, spaceAbove=0, spaceBelow=0)
		else :
			self.startButton=button('Start',self.startAction, spaceAbove=spaceAbove, spaceBelow=0)
		if self.showMaxIter :
			self.stopButton=button('Stop',self.stopAction, spaceAbove=0, spaceBelow=0)
			self.maxIterWidget=field('Max number',self.maxIter,spaceAbove=0, spaceBelow=spaceBelow)
		else :
			self.stopButton=button('Stop',self.stopAction, spaceAbove=0, spaceBelow=spaceBelow)
		self.stopButton.button.setEnabled(False)
		self.timer=QTimer()

	def setupSerie(self,nAcqui,iterPerAcqui,iterToCheck='default',acquiStart=False,acquiEnd=False): 
	#nAcqui=number of acquisition for the serie ; iterPerAcqui= number of iteration for one acqui
	#iterToCheck = function which is called and compared to  iterPerAcqui to check when the deed is done (typically some line.getIteration)
		
		self.nAcqui=nAcqui
		self.serieLabel.setText('Acquisition 0/%i'%(self.nAcqui))
		self.acquiStart=acquiStart
		self.acquiEnd=acquiEnd
		if isinstance(iterPerAcqui, (list, tuple, np.ndarray)) :			
			self.iterPerAcqui=iterPerAcqui	
		else :
			self.iterPerAcqui=np.ones(self.nAcqui)*iterPerAcqui	
		if iterToCheck=='default' :
			try :
				self.iterToCheck=self.lineIter.getIteration
			except :
				raise(ValueError('You need to setup a line in startStopButton(lineIter=) to begin a serie'))
		else :
			self.iterToCheck=iterToCheck

	def startSerie(self):

		self.serieButton.button.setEnabled(False)
		self.startButton.button.setEnabled(False)
		self.stopButton.button.setEnabled(True)

		#~~Setup defaultFolder
		i=1
		folderName='D:/DATA/'+datetime.now().strftime("%Y%m%d")+'/Serie 1/'
		while os.path.exists(folderName) :
			i+=1
			folderName='D:/DATA/'+datetime.now().strftime("%Y%m%d")+'/Serie %i/'%i
		self.defaultFolder=folderName
		#~~Fin de setup default Folder

		self.iAcqui=0 #Counter of the current acquisition
		self.maxIter=np.infty #j'utilise un autre système de compteur finalement,ça devrait éviter les embrouilles
		self.nextAcqui()
		self.timer.timeout.connect(self.updateSerie)
		self.timer.start()

	def nextAcqui(self):
		self.acquiStart(self.iAcqui)
		self.updateArgs=self.setup()
		resetLines()
		self.serieLabel.setText('Acquisition %i/%i'%(self.iAcqui+1,self.nAcqui))


	def updateSerie(self):
		if self.iterToCheck() <= self.iterPerAcqui[self.iAcqui] :
			self.updateAction()
		elif self.iAcqui+1 < self. nAcqui :
			resetSetup(closeAnyway=False,stopTimers=False)
			self.acquiEnd(self.iAcqui)
			self.iAcqui+=1
			self.nextAcqui()		
		else :
			self.acquiEnd(self.iAcqui)
			self.stopAction()


	def startAction(self):
		if self.serie :
			self.serieButton.button.setEnabled(False)
		self.startButton.button.setEnabled(False)
		self.stopButton.button.setEnabled(True)
		if self.showMaxIter :
			self.maxIter=val(self.maxIterWidget)
		resetLines()
		if self.setup :
			self.updateArgs=failSafe(self.setup,debug=self.debug) #il va peut etre tej le failSafe
		if self.updateFunc :
			self.timer.timeout.connect(self.updateAction)
			self.timer.start(10)

	def updateAction(self):
		if self.lineIter :
			if self.lineIter.iteration > self.maxIter :
				self.stopAction()
				return	
		
		if isinstance(self.updateArgs,None.__class__) : #C'est déguelasse mais autrement numpy casse les couilles
			failSafe(self.updateFunc,debug=self.debug)
		elif isinstance(self.updateArgs,tuple) :
			failSafe(self.updateFunc,*self.updateArgs,debug=self.debug)
		else :
			failSafe(self.updateFunc,self.updateArgs,debug=self.debug)

	def stopAction(self): 
		self.timer.stop()
		resetSetup(closeAnyway=False,stopTimers=False,extraStop=extraStop)
		self.startButton.button.setEnabled(True)
		self.stopButton.button.setEnabled(False)
		if self.serie :
			self.serieButton.button.setEnabled(True)

	def addToBox(self,box):
		if self.serie :
			self.serieButton.addToBox(box)
			self.serieLabel.addToBox(box)
		self.startButton.addToBox(box)
		self.stopButton.addToBox(box)
		if self.showMaxIter :
			self.maxIterWidget.addToBox(box)

class device(): #Pour l'instant ça sert juste à les regrouper pour les fermer
	def __init__(self):
		self.toBeClosed=True

class microwave(device):
	def __init__(self,ressourceName='mw_ludo',timeout=8000): #timeout in ms
		super().__init__()
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
		self.toBeClosed=True
		self.taskOpened=False
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
		self.taskOpened=True
	def close(self,closeAnyway=False):
		if self.taskOpened :
			if self.toBeClosed or closeAnyway :
				self.task.close()
				self.taskOpened=False
				self.running=False

class AOChan(NIChan):
	def __init__(self,*physicalChannels): #Physical Channels = 'ao0' or 'ao1'	
		super().__init__(*physicalChannels)	
		self.triggerSignal='/Dev1/ao/StartTrigger'		
	def createTask(self):
		self.task=nidaqmx.Task()
		for pc in self.physicalChannels :
			cname='Dev1/'+pc
			self.task.ao_channels.add_ao_voltage_chan(cname)	
		self.taskOpened=True
	def setupContinuous(self,Value): #Starts immediately
		self.createTask()
		self.value=val(Value)
		self.task.write(self.value)
		self.start()
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
	def setTo(self,value=0):
		if self.running :
			self.close()
		self.setupContinuous(value)
		self.close()

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
		self.taskOpened=True
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
		self.taskOpened=True
	def setupContinuous(self,Value): #Starts immediately. A noter que la c'est pour du continu constant, il faudrait éventuellement faire autre chose pour du continu avec un motif qui se répète
		self.createTask()
		self.value=val(Value)
		self.task.write(self.value)
		self.start()
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
			self.task.co_channels.add_co_pulse_chan_freq(cname,freq=freq)
		self.taskOpened=True
	def setupContinuous(self,Freq): #Starts immediately
		self.createTask((val(Freq)))		
		self.task.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,samps_per_chan=10)
		self.start()

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
			return False
		if not(isinstance(x,np.ndarray) or isinstance(x,list)) :
			x=line.xData
		line.update(x,y,self.norm)
		if self.autoSave :
			self.autoSave.check()
		return True

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
	def getIteration(self):
		return self.iteration

	def update(self,x,y,norm):
		oldY=self.trueY
		if self.typ=='instant' :
			newY=y			
		elif self.typ=='average' :
			if self.iteration == 1 : #Mathématqiuement y'en a pas besoin mais sinon c'est galère avec les tailles
				newY=y
			else :			
				newY=oldY*(1-1/self.iteration)+y/self.iteration
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

class pulsedLaserWidget():
	def __init__(self,spaceAbove=1,spaceBelow=0,chan='ctr0',freq=20E6,ignoreWarning=False):
		self.laserCb=checkBox('Laser On',action=self.lasOnOff,spaceAbove=spaceAbove)
		self.laserFreq=field('Laser frequency',freq,spaceAbove=0)
		self.laser=pulsedLaserControl(channel=chan,ignoreWarning=ignoreWarning)
	def lasOnOff(self):
		if self.laserCb.state() :
			self.laser.start(self.laserFreq)
		else :
			self.laser.stop()
	def addToBox(self,box):
		self.laserCb.addToBox(box)
		self.laserFreq.addToBox(box)

class pulsedLaserControl():
	def __init__(self,channel='ctr0',ignoreWarning=False):
		self.co=COChan(channel)
		self.state='Off'
		self.freq=0
		self.co.toBeClosed=False
		self.ignoreWarning=ignoreWarning
	def start(self,freq):
		freq=val(freq)
		if self.state=='Off':
			self.freq=freq
			try :
				self.co.setupContinuous(self.freq)	
			except :
				if not self.ignoreWarning :
					warning('Could not start pulsed laser \n Probably used in another program')
			self.state='On'
		elif freq != self.freq : 
			self.freq=freq
			self.stop()
			self.start(self.freq)
		else :
			pass
	def stop(self):
		if self.state=='On':
			self.co.close(closeAnyway=True)
			self.state='Off'

class continuousLaserWidget():
	def __init__(self,spaceAbove=1,spaceBelow=0,chanAOM='ao1',chanPM='ai9',power=200,caliber=1000): #Power in uW ; caliber=power in uW for U=1V
		self.laserCb=checkBox('Laser On',action=self.lasOnOff,spaceAbove=spaceAbove)
		self.laserPow=field('Laser power (uW)',power,spaceAbove=0)
		self.AOM=AOChan(chanAOM)
		self.PM=powerMeterAnalog(chan=chanPM,caliber=caliber)
	def lasOnOff(self):
		if self.laserCb.state() :			
			self.AOM.setupContinuous(0)
			self.setTo(val(self.laserPow))
			self.AOM.close()
		else :
			self.AOM.setupContinuous(0)
			self.AOM.close()


	def setTo(self,target,precision=0.001):
		mini=0
		maxi=0.45
		self.PM.setup()
		while maxi-mini > precision :
			val=(maxi+mini)/2
			self.AOM.updateContinuous(val)
			lect=self.PM.read()
			if lect > target :
				maxi=val
			else :
				mini=val
		self.PM.close()
	def addToBox(self,box):
		self.laserCb.addToBox(box)
		self.laserPow.addToBox(box)

class powerMeterAnalog():
	def __init__(self,chan,caliber):
		self.Ai=AIChan(chan,extendedRange=[-0.5,2.5])
		self.caliber=caliber
	def setup(self,nAvg=100,facq=1E4):
		self.Ai.setupTimed(SampleFrequency=facq,SamplesPerChan=nAvg)
	def close(self):
		self.Ai.close()
	def read(self):
		res=self.Ai.readTimed(waitForAcqui=True)
		return(sum(res)/len(res)*self.caliber)



def resetSetup(closeAnyway=False,stopTimers=True,extraStop=False): #C'est un peu brut mais bon ça fonctionne
	if stopTimers :
		timers=get_objects(QTimer)
		for timer in timers :
			timer.stop()
	tasks=get_subclass(NIChan)
	for task in tasks :
		task.close(closeAnyway=closeAnyway)	
	devices=get_subclass(device)
	for d in devices :
		if d.toBeClosed :
			d.close()
	if callable(extraStop):
		extraStop()
	
def resetLines():
	lines=get_objects(myLine)
	for line in lines :
		line.iteration=1

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
			resetSetup(closeAnyway=True,stopTimers=True)
			quit()
		else :
			GUI=get_objects(Graphical_interface)[0]
			resetSetup(closeAnyway=True,stopTimers=True)
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

def warning(message):
	try :
		GUI=get_objects(Graphical_interface)[0]
	except :
		print(message)
		raise(ValueError('Could not find graphical interface to print error message'))
	mb = QMessageBox(GUI)
	mb.setText(message)
	mb.show()

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
		warning('Attention !')
	def acquiStart(i):
		ftoto.setValue(3*i)
	def acquiEnd(i):
		fname=StartStop.defaultFolder+'acqui #%i'%i
		save.save(fname=fname)
	def dummyf(e):
		pos=e[0]
		# print(pos.pos())
		mousePoint = gra.mainAx.vb.mapSceneToView(pos.pos())
		print(mousePoint.x(),mousePoint.y())
	x=np.linspace(0,10,100)
	y=np.cos(x)
	gra=graphics()
	l1=gra.addLine(x,y,typ='scroll')
	l2=gra.addLine(x,-y)
	ax2=gra.addAx()
	l3=gra.addLine(x,-y,ax=ax2,typ='instant')

	las=continuousLaserWidget()
	ftoto=field('toto',10,spaceBelow=1)
	attention=button('Warning',avertissement)
	fields=[las,ftoto,attention]


	StartStop=startStopButton(setup=setup,update=update,debug=True,lineIter=l3,showMaxIter=True,serie=True)
	StartStop.setupSerie(nAcqui=3,iterPerAcqui=[100,150,50],acquiStart=acquiStart,acquiEnd=acquiEnd)
	save=saveButton(gra,autoSave=10)
	trace=keepTraceButton(gra,l3)
	it=iterationWidget(l3)
	norm=gra.normalize()
	# print(dir(gra.scene()))
	proxy = pg.SignalProxy(gra.scene().sigMouseClicked, rateLimit=60, slot=dummyf)

	buttons=[norm,StartStop,trace,save,it]
	GUI=Graphical_interface(fields,gra,buttons,title='Example GUI')

	GUI.run()

def test_multiple_tasks():
	ao1=AOChan('ao0')
	ao2=AOChan('ao1')
	ao3=AOChan('ao0')
	ao2.setupContinuous(0.5)
	values=np.linspace(-1,1,100)
	ao1.setupTimed(100,values)
	ao1.start()
	time.sleep(1)
	resetSetup(extraStop=lambda: ao2.setTo(0.45))


if __name__ == "__main__":
	test_pg()


