#To profile the code : @profile above the function tou want to profile, then run "kernprof -l script_to_profile.py" in terminal, then "python -m line_profiler script_to_profile.py.lprof" to visalize

import sys
import os
from getmac import get_mac_address as gma
from contextlib import contextmanager
import warnings
import traceback
import time
from datetime import datetime
import nidaqmx
import nidaqmx.task
import nidaqmx.system
import pyvisa as visa

import numpy as np
import statistics
import analyse

# import PyQt6 #Ca a pas du tout l'air compatible
import pyqtgraph as pg 

from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QTimer,QSize)
from PyQt5.QtWidgets import (QWidget, QPushButton, QComboBox,
	QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QCheckBox, QFileDialog, QErrorMessage, QMessageBox)
import qdarkstyle

qapp = QApplication(sys.argv)

macAdressOfCurrentPC=gma()
if macAdressOfCurrentPC=='64:00:6a:5f:1e:5b' : #Ordi 2 (le mien)
	computerUsed='Ordi2'
	defaultDataPath="D:/DATA/"
	defaultTheme='light'

elif macAdressOfCurrentPC=='d8:9e:f3:23:bb:26' : #Ordi 1 (de l'entrée)
	computerUsed='Ordi1'
	defaultDataPath="C:/DATA/"
	defaultTheme='dark'

elif macAdressOfCurrentPC=='f0:79:59:2f:4b:78' : #Ordi perso
	computerUsed='OrdiPerso'
	defaultDataPath="../data/"
	defaultTheme='light'
else :
	print('current mac adress : ',gma())
	raise(ValueError('Your computer was not detected in the list, please add its mac adress at the beginning of lab.py'))

class Graphical_interface(QMainWindow) :
	def __init__(self,*itemLists,title='Unnamed',theme=defaultTheme):
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
		if theme=='dark' :
			qapp.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
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
		if style=='big' :
			self.label.setFont(QFont( "Consolas", 20, QFont.Bold))
		if style=='BIG' :
			self.label.setFont(QFont( "Consolas", 40, QFont.Bold))
	def setText(self,text):
		self.label.setText(text)
	def addToBox(self,box):
		box.addStretch(self.spaceAbove)
		box.addWidget(self.label)
		box.addStretch(self.spaceBelow)	

class field():
	def __init__(self,name,initial_value='noValue',action=False,spaceAbove=1,spaceBelow=0): 
		self.label=QLabel(name)
		self.lect=QLineEdit()
		if initial_value != 'noValue' :
			self.setValue(initial_value)
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
		if action :
			self.lect.returnPressed.connect(action)
	def updateValue(self):
		try : 
			self.v=float(self.lect.text())
			if self.v.is_integer():
				self.v=int(self.v)
		except :
			self.v=self.lect.text()
	def setValue(self,new_value,precision='exact'):
		self.v=new_value
		label=repr_numbers(self.v,precision)
		self.lect.setText(label)
	def setEnabled(self,b):
		self.label.setEnabled(b)
		self.lect.setEnabled(b)
	def __mul__(self,b):
		self.updateValue()
		return self.v*b
	def __rmul__(self,b):
		self.updateValue()
		return b*self.v
	def __add__(self,b):
		self.updateValue()
		return b+self.v
	def __radd__(self,b):
		self.updateValue()
		return self.v+b
	def __sub__(self,b):
		self.updateValue()
		return self.v-b
	def __rsub__(self,b):
		self.updateValue()
		return b-self.v
	def __truediv__(self,b):
		self.updateValue()
		return self.v/b
	def __rtruediv__(self,b):
		self.updateValue()
		return b/self.v
	def __float__(self):
		return float(self.v)
	def __int__(self):
		return int(self.v)
	def __repr__(self):
		return("Field of value %f"%self.v)
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
	def setEnabled(self,b):
		self.button.setEnabled(b)
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
	def __init__(self,name,*items,action=False,spaceAbove=1,spaceBelow=0):
		self.label=QLabel(name)
		self.cb=QComboBox()
		self.dic={}
		for item in items :
			self.addItem(item)
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
		if action :
			self.cb.currentIndexChanged.connect(action)
	def index(self):
		return self.cb.currentIndex()
	def setIndex(self,index):
		if isinstance(index,str) :
			i=self.dic[index]
		else :
			i=index
		return self.cb.setCurrentIndex(i)
	def text(self):
		return self.cb.currentText()
	def addItem(self,item):
		self.dic[item]=self.cb.count() #je le fait avant pour qu'il commence à 0
		self.cb.addItem(item)
	def removeItem(self,item):
		if isinstance(item,str) :
			i=self.dic[item]
		else :
			i=item
		return self.cb.removeItem(i)
	def removeAll(self):
		# for item in self.dic.keys():
		# 	self.removeItem(item)
		self.cb.clear()
	def setEnabled(self,b):
		self.label.setEnabled(b)
		self.cb.setEnabled(b)
	def addToBox(self,box):
		box.addStretch(self.spaceAbove)
		box.addWidget(self.label)
		box.addWidget(self.cb)
		box.addStretch(self.spaceBelow)

class box():
	def __init__(self,*items,typ='H',spaceAbove=1,spaceBelow=0): #typ='H' or 'V', pour les Hbox, spaceAbove/below devient gauche/droite
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
		if typ=='H':
			self.box=QHBoxLayout()
		elif typ=='V':
			self.box=QVBoxLayout()
		for item in items :
			item.addToBox(self.box)
	def addToBox(self,box):
		box.addStretch(self.spaceAbove)
		box.addLayout(self.box)
		box.addStretch(self.spaceBelow)

class saveButton(button):
	def __init__(self,graphicWidget,autoSave=False,spaceAbove=1,spaceBelow=0): 
		self.gra=graphicWidget
		self.qapp=qapp
		super().__init__("Save data",spaceAbove=spaceAbove,spaceBelow=spaceBelow)
		try :
			self.startpath=defaultDataPath
		except :
			self.startpath=''
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
			if fname=='' :
				return
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
					spamwriter.writerow(line.x)
					spamwriter.writerow(line.trueY)


		if saveFigure :
			self.qapp.primaryScreen().grabWindow(self.gra.parentWidget().winId()).save(fname,'png')

class keepTraceButton():
	def __init__(self,*lines,graph='auto',spaceAbove=1,spaceBelow=0):
		self.keepButton=button("Keep Trace",self.keepTrace,spaceAbove=spaceAbove,spaceBelow=0)
		self.clearButton=button("Clear Trace",self.clearTrace,spaceAbove=0,spaceBelow=spaceBelow)
		if graph=='auto' :
			self.graph=lines[0].graphicsWidget
		else :
			self.graph=graph
		self.lines=lines
		self.axes=[]
		for line in self.lines : 
			self.axes+=[line.ax]

	def keepTrace(self):
		for line in self.lines :
			x=line.xData
			y=line.trueY
			ax=line.ax
			trace=self.graph.addLine(x,y,ax=ax,typ='trace')


	def clearTrace(self):
		for ax in self.axes :
			curves=ax.curves
			for i in range(1,len(curves)+1):
				if curves[-i].typ=='trace' :
					curves[-i].remove()
					break

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
			filename=defaultDataPath+'/AutoSave/'+date_str+'.png'
			self.sb.save(fname=filename,saveData=self.saveData,saveFigure=self.saveFigure)
			self.time_last_save=time.time()

class startStopButton():
	def __init__(self,setup=False,update=False,spaceAbove=1,spaceBelow=0, extraStop=False, debug=False, maxIter=np.infty, lineIter=False, showMaxIter=False,serie=False, timeDelay=0): #§timeDelay in ms
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
		self.timeDelay=timeDelay
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
		folderName=defaultDataPath+datetime.now().strftime("%Y%m%d")+'/Serie 1/'
		while os.path.exists(folderName) :
			i+=1
			folderName=defaultDataPath+datetime.now().strftime("%Y%m%d")+'/Serie %i/'%i
		self.defaultFolder=folderName
		#~~Fin de setup default Folder

		self.iAcqui=0 #Counter of the current acquisition
		self.maxIter=np.infty #j'utilise un autre système de compteur finalement,ça devrait éviter les embrouilles
		self.nextAcqui()
		self.timer.timeout.connect(self.updateSerie)
		self.timer.start(self.timeDelay)
		self.running=True

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
			self.timer.start(self.timeDelay)
		self.running=True

	def updateAction(self):
		if self.running==False :
			# print("tried to update while closed")
			return
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
		qapp.processEvents() #Danger, mais je pense que c'est la bonne direction. Ca et/ou gérer le buffer. 
		#En gros ça force l'image à s'actualiser, mais ça fout le bordel dans les timers (je pense que ça joue sur les threads), et en gros tu peux te retrouver à call update (plusieurs fois meme) alors que le timer est sensé être stoppé.

	def stopAction(self): 
		self.timer.stop()
		self.running=False
		resetSetup(closeAnyway=False,stopTimers=False,extraStop=self.extraStop)
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

class fitButton():
	def __init__(self,line,fit='lin',name='fit',menu=False,spaceAbove=1,spaceBelow=0): 

		self.fitLibrary=['lin','exp','stretch','arb stretch','ESR']

		if menu :
			self.menu=dropDownMenu('Chose fit','--No fit chosen--',*self.fitLibrary,action=self.itemChosenMenu,spaceAbove=spaceAbove,spaceBelow=0)
		else :
			self.menu=False
		if menu :
			self.addFitButton=button(name=name,action=self.addFit,spaceAbove=0,spaceBelow=0)
			self.addFitButton.setEnabled(False)
		else :
			self.addFitButton=button(name=name,action=self.addFit,spaceAbove=spaceAbove,spaceBelow=0)
		self.removeFitButton=button(name='clear fit',action=self.removeFit,spaceAbove=0,spaceBelow=spaceBelow)
		self.line=line
		self.labelNames=False
		
		
		self.setFitFunction(fit)
	def setFitFunction(self,fit):
		if fit=='lin' :
			from analyse import lin_fit as f
			self.func=f
			self.paramsToShow=[0,1]
			self.labelNames=['slope','y0']
		if fit=='exp' :
			from analyse import exp_fit as f
			self.func=f
			self.paramsToShow=[2]
			self.labelNames=['tau']
		elif fit=='stretch' :
			from analyse import stretch_exp_fit as f
			self.func=f
			self.paramsToShow=[2]
			self.labelNames=['tau']
		elif fit=='arb stretch' :
			from analyse import stretch_arb_exp_fit as f
			self.func=f
			self.paramsToShow=[2,3]
			self.labelNames=['tau','alpha']
		if fit=='expZero' :
			from analyse import exp_fit_zero as f
			self.func=f
			self.paramsToShow=[1]
			self.labelNames=['tau']
		elif fit=='stretchZero' :
			from analyse import stretch_exp_fit_zero as f
			self.func=f
			self.paramsToShow=[1]
			self.labelNames=['tau']
		elif fit=='ESR' :
			from analyse import ESR_n_pics,find_ESR_peaks
			def f(x,y):
				if len(self.line.ax.infiniteLines) <= 1 :
					cs=find_ESR_peaks(x,y)
				else :
					cs=[]
					for l in self.line.ax.infiniteLines :
						cs+=[l.pos()[0]]
				return ESR_n_pics(x,y,cs)
			self.func=f
			self.paramsToShow=[]
			self.labelNames=[]
		elif fit=='ESR and B' :
			from analyse import find_nearest_ESR
			def f(x,y):
				cs=[]
				for l in self.line.ax.infiniteLines :
					cs+=[l.pos()[0]]
				return find_nearest_ESR(x,y,cs)		
			self.func=f
			self.paramsToShow=[0,1,2,3]
			self.labelNames=['B amp (G)','Angle from 100 (°)', 'Angle from 111 (°)', 'Width (Mhz)']
	def itemChosenMenu(self):
		self.setFitFunction(fit=self.menu.text())
		self.addFitButton.setEnabled(True)
	def addFit(self):
		x=self.line.xData
		y=self.line.trueY
		with warnings.catch_warnings() :
			warnings.simplefilter('error')
			try :
				popt,yfit=self.func(x,y)
			except Exception as error :		
				tb=traceback.extract_tb(error.__traceback__)
				warningGUI(str(error)) #.join(tb.format()) Pour l'erreur complète
				return
		label=''
		for i in range(len(self.paramsToShow)) :
			if self.labelNames :
				label+=self.labelNames[i]+'='+repr_numbers(popt[self.paramsToShow[i]],precision=3)+'; '
			else :
				label+='p%i : '%i+repr_numbers(popt[self.paramsToShow[i]])+'; '
		self.line.graphicsWidget.addLine(x,yfit,ax=self.line.ax,typ='fit',label=label)
	def removeFit(self):
		curves=self.line.ax.curves
		for i in range(1,len(curves)+1):
			if curves[-i].typ=='fit' :
				curves[-i].remove()
				break
	def addToBox(self,box):
		if self.menu :
			self.menu.addToBox(box)
		self.addFitButton.addToBox(box)
		self.removeFitButton.addToBox(box)

class device(): #Pour l'instant ça sert juste à les regrouper pour les fermer
	def __init__(self):
		self.toBeClosed=True

class microwave(device):
	def __init__(self,ressourceName='mw_ludo',timeout=8000): #timeout in ms
		super().__init__()
		if ressourceName=='mw_ludo' :
			ressourceName='TCPIP0::micro-onde.phys.ens.fr::inst0::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"
		if ressourceName=='mw1' :
			ressourceName= 'USB0::0x0AAD::0x0054::182239::INSTR'
		self.PG = visa.ResourceManager().open_resource( ressourceName )
		self.PG.write_termination = '\n'
		self.PG.timeout=timeout
		# self.PG.clear()  # Clear instrument io buffers and status. Fait planter la microonde de l'entrée
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

		self.PG.write('OUTP ON') #OFF/ON pour allumer éteindre la uW
		self.PG.write('*WAI')

		self.PG.write('FREQ:MODE LIST') #on doit allumer la uW avant de passer en mode liste
		self.PG.write('*WAI')

		self.PG.write('LIST:LEAR') #Peut etre bien facultatif
		self.PG.write('*WAI')

		self.PG.write('LIST:MODE STEP')
		self.PG.write('*WAI')

		self.PG.write('LIST:TRIG:SOUR EXT')
		self.PG.write('*WAI')

		self.PG.write('LIST:RES') #Ca par contre ca a l'air de jouer curieusement
		self.PG.write('*WAI')

		time.sleep(1)
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

class pulseBlaster(device):
	def __init__(self,clockFrequency=300,chanOn=(),verbose=False): #frequency in MHz, frequency of the pb in the entrance computer is 300 MHz, frequency of the pb in the back computer is 500 MHz
		#chanOn : channels (1,2,3, or 4) to leave on True when the pulseblaster is closed
		#le verbose ne sert présentement à rien
		super().__init__()
		import spinapi as sp
		self.verbose=verbose
		self.sp=sp
		self.sp.pb_set_debug(1)
		self.clockFrequency=clockFrequency
		self.chanOn=chanOn
	def initPb(self):
		self.sp.pb_select_board(0)
		if self.sp.pb_init() != 0:
			raise ValueError("Error initializing board: %s" % self.sp.pb_get_error())
		self.sp.pb_core_clock(self.clockFrequency)

	def setupContinuous(self,ch1=0,ch2=0,ch3=0,ch4=0):
		with stdout_redirected() :
			self.initPb()
			self.sp.pb_start_programming(self.sp.PULSE_PROGRAM)
			self.writeInst([ch1,ch2,ch3,ch4],1e-3,inst=self.sp.Inst.BRANCH,inst_data=0)
			self.sp.pb_stop_programming()
			self.start()
			self.sp.pb_close()
	def setupPulsed(self,dt=1e-6,ch1='unused',ch2='unused',ch3='unused',ch4='unused',finite=True, toBeClosed=True): #timeUnit in s (default 1 us)
		with stdout_redirected() :
			self.initPb()
			self.toBeClosed=toBeClosed
			dt=1*dt
			channels=[ch1,ch2,ch3,ch4]

			for ch in channels :
				if ch !='unused' :
					n=len(ch)

			a=np.zeros((n,4),np.dtype(int))
			for i in range(4):
				ch=channels[i]
				if ch =='unused' :
					pass
				else :
					a[:,i]=ch

			self.sp.pb_start_programming(self.sp.PULSE_PROGRAM)

			for i in range(0,n-1) :
				self.writeInst(a[i,:],dt)
			if finite :
				self.writeInst(a[n-1,:],dt,inst=self.sp.Inst.STOP,inst_data=0)
			else :
				self.writeInst(a[n-1,:],dt,inst=self.sp.Inst.BRANCH,inst_data=0)
			self.sp.pb_stop_programming()

	def writeInst(self,flags,length,inst=0,inst_data=0): #flags : array of length 4 for the four channels with either 0(Down), 1(Up) or 2(Pulse); inst=InstType (see spinapi.py); inst_data= input for the instruction; length= length in s.
		length=length*1e9 #the base unit of the pb is the ns
		Pulse=False
		for k in flags : 
			if k==2 :
				Pulse=True
		if Pulse :
			#Il faudra p-e modifier pour mettre la pulse la plus courte possible (une dizaine de ns je crois), mais j'ai un peu peur qu'elles ne soit pas toujours détectée (la micro-onde m'a deja fait des blagues)
			flagBis=[min(1,i) for i in flags] #ca transforme les 2 en 1
			cmd=self.convertLineToBin(flagBis)
			self.sp.pb_inst_pbonly(cmd, self.sp.Inst.CONTINUE, 0, length//2) #les pulses font 20 ns up.
			flagBis=[i%2 for i in flags] #c'est un peu ridicule mais en vrai je suis fier de moi. Ca transforme les 2 en 0 et pas les 1
			cmd=self.convertLineToBin(flagBis)
			if inst_data==self.sp.Inst.STOP :
				self.sp.pb_inst_pbonly(cmd, inst, self.sp.Inst.CONTINUE, length//2) #Il y a une instruction en plus parce que la pulseblaster considère qu'elle a fini des qu'elle lance la dernière instruction, et pas quand la dernière instrucion est terminée
				self.sp.pb_inst_pbonly(cmd, inst, self.sp.Inst.STOP, 20)
			else :
				self.sp.pb_inst_pbonly(cmd, inst, inst_data, length-length//2)
		else :
			cmd=self.convertLineToBin(flags)
			if inst_data==self.sp.Inst.STOP :
				self.sp.pb_inst_pbonly(cmd, inst, self.sp.Inst.CONTINUE, length)
				self.sp.pb_inst_pbonly(cmd, inst, self.sp.Inst.STOP, 20)
			else :
				self.sp.pb_inst_pbonly(cmd, inst, inst_data, length)


	def convertLineToBin(self,line):
		#En gros la pb prend en entrée une série de 6*4 bits sous la forme d'un entier 32 bits (c'est pareil sur l'interpreter), mais nous on a que
		#4 sorties qui correspondent aux 4 derniers bits. Donc je part d'un cas ou tout est à 0, et j'ajoute la channel i en modifiant l'avant dernier i-eme bit (aka 2^i)
		cmd=0XFFFFF0 #Je fout des 1 sur tous les bits non utilisés. Je crois que techiquement il n'y a que le premier qui est indispensable mais bon
		for i in range(len(line)):
			if line[i]!=0 and line[i]!=1 :
				raise ValueError('Invalid command sent to the pulseblaster (not 0 or 1) :',line[i])
			cmd+=2**i*line[i]
		return(int(cmd))


	def isDone(self):
		ret=self.sp.pb_read_status()
		if ret<=3 :
			return True
		else :
			return False
	def start(self):
		with stdout_redirected() :
			self.sp.pb_reset() #pas bien compris à quoi il sert le reset
			self.sp.pb_start()
	def stop(self):
		self.sp.pb_stop()
	def close(self):
		with stdout_redirected() :
			line=[0,0,0,0]
			for i in self.chanOn :
				line[i-1]=1
			self.sp.pb_close()
			self.setupContinuous(ch1=line[0],ch2=line[1],ch3=line[2],ch4=line[3])

class hiddenPrints:
	def __enter__(self):
		self._original_stdout = sys.stdout
		sys.stdout = open(os.devnull, 'w')

	def __exit__(self, exc_type, exc_val, exc_tb):
		sys.stdout.close()
		sys.stdout = self._original_stdout

class useTheme():
	def __init__(self,theme='white'):
		self.theme=theme
		if theme=='light' or theme=='white' :
			pg.setConfigOption('background', 'w')
			pg.setConfigOption('foreground', 'k')			
			self.penColors=[(31, 119, 180),(255, 127, 14),(44, 160, 44),(214, 39, 40),(148, 103, 189),(140, 86, 75),(227, 119, 194),(127, 127, 127),(188, 189, 34),(23, 190, 207)] #j'ai volé les couleurs de matplotlib
		if theme=='dark' or theme=='black' :
			self.penColors=[(255, 127, 14),(31, 119, 180),(44, 160, 44),(214, 39, 40),(148, 103, 189),(140, 86, 75),(227, 119, 194),(127, 127, 127),(188, 189, 34),(23, 190, 207)] #j'ai volé les couleurs de matplotlib


		# pg.setConfigOptions(antialias=False)	
	def nextLine(self,ax,typ=False,big=True):
		try : ax.penIndices #je fais plus trop ça maintenant normalement, mais bon
		except :
			ax.penIndices=[True]*len(self.penColors)
		for i in range(len(self.penColors)) : #Si jamais toutes les couleurs sont prises, il reste sur la dernière
			if ax.penIndices[i] :
				break
		penIndex=i
		ax.penIndices[penIndex]=False
		if big :
			widths=[2,2,3]
		else :
			widths=[1,2,1]
		if typ=='trace' :
			pen=pg.mkPen(self.penColors[penIndex],width=widths[0],style=Qt.DashDotLine) 
			symbol=None
			symbolPen=None
			symbolBrush=None
		elif typ=='fit' :
			pen=pg.mkPen(self.penColors[penIndex],width=widths[1],style=Qt.DashDotLine) 
			symbol=None
			symbolPen=None
			symbolBrush=None
		else :
			pen=pg.mkPen(self.penColors[penIndex],width=widths[2],style=Qt.SolidLine)
			symbol='o'
			symbolPen=pen
			symbolBrush=pg.mkBrush(None)

		ax.currentPenIndex+=1
		return pen,symbol,symbolPen,symbolBrush,penIndex
	def penSizeChange(self,line):
		n=len(line.x)
		big = n<=300
		penIndex=line.penIndex
		ax=line.ax
		typ=line.typ
		if big :
			widths=[2,2,3]
		else :
			widths=[1,2,1]
		if typ=='trace' :
			pen=pg.mkPen(self.penColors[penIndex],width=widths[0],style=Qt.DashDotLine) 
			symbol=None
			symbolPen=None
			symbolBrush=None
		elif typ=='fit' :
			pen=pg.mkPen(self.penColors[penIndex],width=widths[1],style=Qt.DashDotLine) 
			symbol=None
			symbolPen=None
			symbolBrush=None
		else :
			pen=pg.mkPen(self.penColors[penIndex],width=widths[2],style=Qt.SolidLine)
			symbol='o'
			symbolPen=pen
			symbolBrush=pg.mkBrush(None)
		return pen,symbol,symbolPen,symbolBrush

class NIChan():
	def __init__(self,*physicalChannels):
		self.trigged=False
		self.running=False
		self.nAvg=1 #nAvg : (mainly for AI) : increase the acquisition frequency by a factor of nAvg in order to get more measurement per sequence (~low pass filter)
		self.nRepeat=1 #nRepeat : Do the sequence nRepeat times each times the task is called. Starting and stopping the task takes ~10 ms, so you should aime to have a total acquistion time > 10 ms
		self.toBeClosed=True
		self.taskOpened=False
		self.setChannels(*physicalChannels)
	def setChannels(self,*physicalChannels):
		self.physicalChannels=physicalChannels
		self.nChannels=len(physicalChannels)
	def triggedOn(self,chan):
		if isinstance(chan,str) :
			self.task.triggers.start_trigger.cfg_dig_edge_start_trig(chan)
		else :
			self.task.triggers.start_trigger.cfg_dig_edge_start_trig(chan.triggerSignal)
		self.task.triggers.start_trigger.retriggerable=True
		self.trigged=True
		self.start()
	def timeAxis(self):
		n=int(self.sampsPerChan/self.nAvg)
		return(np.linspace(0,self.sampsPerChan/self.samplingRate,n))
	def done(self):
		return(self.task.is_task_done())
	def start(self):
		self.task.start()
		self.running=True
		self.taskOpened=True
	def restart(self,wait=True):
		if wait :
			while not self.done():
				pass
		self.task.stop()
		self.start()
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
	def setupContinuous(self,Value,close=True): #Starts immediately
		if self.running :
			self.updateContinuous(Value)
		else :
			self.createTask()
			self.value=val(Value)
			self.task.write(self.value)
			self.start()
			if close :
				self.close()
	def updateContinuous(self,Value):
		self.value=val(Value)
		self.task.write(self.value)
	def setupTimed(self,SampleFrequency,ValuesList,SampleMode='finite'): #sampleMode = 'finite' or 'continuous' ; ValuesList example : [[1,0.5,0],[3,2.5,3]] for two AO channels
		self.createTask()
		self.samplingRate=val(SampleFrequency)
		self.signal=np.array(list(ValuesList)*self.nRepeat)
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
		self.mode='single'
	def getMaxFreq(self):
		return (nidaqmx.system.device.Device('Dev1').ai_max_single_chan_rate/self.nChannels)
	def setupTimed(self,SampleFrequency,SamplesPerChan,SampleMode='finite',nAvg='auto',sourceClock='auto'): 
	#sampleMode = 'finite' or 'continuous' ; nAvg=average over n point for each sample
	#cf def testSynchro(): in test, there is up to a ~2/1000 difference between the AI clock and th DO clock depending on frequency
	#but if you want to use the DO sample Clock, you have to make sure its frequency matches the real samplingRate (pourquoi je m'inflige ça...)
		self.createTask()
		self.mode='timed'
		self.nAvg=val(nAvg)
		if self.nAvg=='auto' :
			fmax=self.getMaxFreq()
			self.nAvg=(fmax/val(SampleFrequency)).__trunc__()
		self.samplingRate=val(SampleFrequency)*self.nAvg
		self.sampsPerChan=val(SamplesPerChan)*self.nAvg*self.nRepeat
		if SampleMode=='finite':
			self.sampleMode=nidaqmx.constants.AcquisitionType.FINITE
		elif SampleMode=='continuous':
			self.sampleMode=nidaqmx.constants.AcquisitionType.CONTINUOUS
		if sourceClock=='auto' :
			self.task.timing.cfg_samp_clk_timing(self.samplingRate,sample_mode=self.sampleMode, samps_per_chan=self.sampsPerChan)
		elif sourceClock=='do' :
			self.task.timing.cfg_samp_clk_timing(self.samplingRate,source='/Dev1/do/SampleClock',sample_mode=self.sampleMode, samps_per_chan=self.sampsPerChan)
		else :
			self.task.timing.cfg_samp_clk_timing(self.samplingRate,source=sourceClock,sample_mode=self.sampleMode, samps_per_chan=self.sampsPerChan)

	def setupPulsed(self,signal,freq,chan='/Dev1/PFI11'): #j'ai décidé qu'il n'y aurait plus de continuous. Ni de multiChannels (pour l'instant)
		#signal : True=1 sample; False = no sample
		#freq is the frequency of the signal
		#chan is the physical channel of the pulsed signal input
		self.createTask()
		self.mode='pulsed'
		fmax=self.getMaxFreq()
		self.nAvg=(fmax/val(freq)).__trunc__() 
		pulsedSignal=doubleSignal(signal)
		self.sampsPerChan=sum(signal)*self.nAvg*self.nRepeat
		self.task.timing.cfg_samp_clk_timing(fmax,sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=self.nAvg) #Rajouter source='/Dev1/do/SampleClock' si ça merde
		self.triggedOn(chan)
		return pulsedSignal

	def setupWithPb(self,signal,freq,chan='/Dev1/PFI9'):
		self.createTask()
		self.mode='withPB'
		fmax=self.getMaxFreq()
		self.nAvg=(fmax/(freq*1.05)).__trunc__() #j'augmente la freq d'acquisition de 5% pour être sur qu'il a le temps de finir l'acquisition entre chaque pulse
		# self.nAvg=2
		mask=[el==2 for el in signal]
		self.sampsPerChan=sum(mask)*self.nAvg*self.nRepeat #note : si tu veux custom la lecture avec des 0 et des 1, n'utilise pas le read(nSample='auto'), ca devrait marcher.
		self.task.timing.cfg_samp_clk_timing(fmax,sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=self.nAvg)
		self.triggedOn(chan)

		
	def read(self,nRead='auto',waitForAcqui=False,timeout=60) :
		if self.mode=='single' :
			return(self.readSingle(timeout=timeout))
		elif self.mode=='timed' :
			return(self.readTimed(waitForAcqui=waitForAcqui,timeout=timeout))
		elif self.mode=='pulsed' :
			return(self.readPulsed(nRead=nRead,timeout=timeout))
		elif self.mode=='withPB' :
			return(self.readPulsed(nRead=nRead,timeout=timeout))



	def readPulsed(self,nRead='auto',timeout=10) :
		if nRead=='auto':
			nRead=self.sampsPerChan
		else :
			nRead=nRead*self.nAvg*self.nRepeat
		data=self.task.read(nRead,timeout=timeout)
		return average(data,self.nAvg,self.nRepeat)

		

	def readTimed(self,waitForAcqui=False,timeout=10):
		if self.sampleMode==nidaqmx.constants.AcquisitionType.CONTINUOUS:
			data=self.task.read(self.sampsPerChan)
			return average(data,self.nAvg) #je gère pas le multi channel en continuous. Faut pas utiliser continuous de toute facon

		if not self.running:
			self.start()

		if waitForAcqui :
			self.task.wait_until_done()

		if self.task.is_task_done() :
			data=self.readAndStop(self.sampsPerChan,timeout=timeout)
		else :
			return False

		data=np.array(data)
		if self.nChannels==1 :
			return average(data,self.nAvg,self.nRepeat)
		else :
			res=[]
			for k in range(self.nChannels):
				res+=[average(data[k,:],self.nAvg,self.nRepeat)]
			res=tuple(res)
			return(res)

	
	def readSingle(self,timeout=10):
		return self.task.read(timeout=timeout)

	def readAndStop(self,sampsPerChan,timeout=10):
		data=self.task.read(sampsPerChan,timeout=timeout)
		self.task.stop()
		self.running=False
		return data

class DOChan(NIChan):
	def __init__(self,*physicalChannels): #Physical Channels = 'p00' to 'p27' (p10 to p27 cannot be used in timed mode (I think, never understood what PFI were))		
		super().__init__(*physicalChannels)	
		self.triggerSignal='/Dev1/do/StartTrigger'	
	def createTask(self):
		self.task=nidaqmx.Task()
		for pc in self.physicalChannels :
			cname='Dev1/port'+pc[1]+'/line'+pc[2]
			self.task.do_channels.add_do_chan(cname)	
		self.taskOpened=True
	def setupContinuous(self,Value,close=True): #Starts immediately. A noter que la c'est pour du continu constant, il faudrait éventuellement faire autre chose pour du continu avec un motif qui se répète
		if self.running :
			self.updateContinuous(Value)
		else :
			self.createTask()
			self.value=val(Value)
			self.task.write(self.value)
			self.start()
			if close :
				self.close()
	def updateContinuous(self,Value):
		self.value=val(Value)
		self.task.write(self.value)
	def setupTimed(self,ValuesList,SampleFrequency,SampleMode='finite'): #sampleMode = 'finite' or 'continuous' ; ValuesList example : [[True,False,True],[True,True,True]] for two DO channels
		self.createTask()
		self.samplingRate=val(SampleFrequency)
		if self.nChannels==1:
			if isinstance(ValuesList,doubleSignal) :
				self.samplingRate=2*val(SampleFrequency)
				self.signal=ValuesList.l*self.nRepeat
			else :
				self.signal=list(ValuesList)*self.nRepeat

			self.sampsPerChan=len(self.signal)
		else :		
			doubleTheRest=False #Tout ce joyeux bordel c'est pour pouvoir passer des signaux doublés (pour trig AI) et des signaux normaux en même temps. Si il y a un signal doublé, il va doubler les autres signaux et la fréquence
			for l in ValuesList :
				if isinstance(l,doubleSignal) :
					self.samplingRate=2*val(SampleFrequency)
					doubleTheRest=True
			if doubleTheRest :
				self.signal=[]
				for l in ValuesList :
					if isinstance(l,doubleSignal) :
						l=l.l*self.nRepeat
					else :
						l=extend_signal(l,2)*self.nRepeat
					self.signal+=[l]
			else :
				self.signal=[list(l)*self.nRepeat for l in ValuesList]
			self.sampsPerChan=len(self.signal[0]) #pas sur que ça marche ça, faudrait passer en numpy pour être clean
		if SampleMode=='finite':
			self.sampleMode=nidaqmx.constants.AcquisitionType.FINITE
		elif SampleMode=='continuous':
			self.sampleMode=nidaqmx.constants.AcquisitionType.CONTINUOUS
		self.task.timing.cfg_samp_clk_timing(self.samplingRate,sample_mode=self.sampleMode, samps_per_chan=self.sampsPerChan)
		self.task.write(self.signal)

class COChan(NIChan):
	def __init__(self,*physicalChannels): #Physical Channel = 'ctr0' to 'ctr3' . Counters can only contain one channel (i believe)		
		super().__init__(*physicalChannels)	
		self.triggerSignal='/Dev1/co/StartTrigger'	#Pas sur avec le ArmStartTrigger, ce sera à vérifier. C'est la merde les trigg avec les compteurs
	def createTask(self,freq):
		self.task=nidaqmx.Task()
		for pc in self.physicalChannels :
			cname='Dev1/'+pc
			self.task.co_channels.add_co_pulse_chan_freq(cname,freq=freq)
		self.taskOpened=True
	def setupContinuous(self,Freq,gate=False,gateChan='/Dev1/PFI9'): #Starts immediately
		freq=val(Freq)
		self.createTask(freq)		
		self.task.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,samps_per_chan=10)
		if gate :
			self.task.triggers.pause_trigger.trig_type=nidaqmx.constants.TriggerType.DIGITAL_LEVEL
			self.task.triggers.pause_trigger.dig_lvl_src=gateChan
			self.task.triggers.pause_trigger.dig_lvl_when=nidaqmx.constants.Level.LOW
		self.start()

class CIChan(NIChan):
	def __init__(self,*physicalChannels): #Physical Channel = 'ctr0' to 'ctr3' . Counters can only contain one channel (i believe)
		super().__init__(*physicalChannels)	
		self.triggerSignal='NOT IMPLEMENTED YET' #ça devrait passer par un sampling via la pb sur le pc de l'entrée
		self.nBitsCounter=nidaqmx.system.device.Device('Dev1').ci_max_size
	def createTask(self):
		self.task=nidaqmx.Task()
		for pc in self.physicalChannels :
			cname='Dev1/'+pc
			self.task.ci_channels.add_ci_count_edges_chan(cname)
		self.taskOpened=True
	def setupContinuous(self,frequency,nSample=1000): #prévu pour fonctionner en autonome (sans trig externe). En gros juste pour l'appli "PL"
		self.createTask()
		self.mode='continuous'
		self.freq=val(frequency)
		n=val(nSample)
		if self.physicalChannels[0] == 'ctr0' :
			SCChan='ctr1'
		if self.physicalChannels[0] == 'ctr1' :
			SCChan='ctr0'
		if self.physicalChannels[0] == 'ctr2' :
			SCChan='ctr3'
		if self.physicalChannels[0] == 'ctr3' :
			SCChan='ctr2'
		self.sampleClock=COChan(SCChan)
		self.task.timing.cfg_samp_clk_timing(self.freq,source='/Dev1/Ctr'+SCChan[-1]+'InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=n)
		self.sampleClock.setupContinuous(Freq=self.freq,gate=False)
		self.start()

	def readContinuous(self,nRead=2): #pas de waitForAcqui en continuous. Pas de waitForAcqui avec les compteurs en faite, ce sera plus simple
		if nRead=='auto':
			nRead=2
		data=np.array(self.task.read(val(nRead)))
		PL=((data[1:]-data[:-1])%(1<<self.nBitsCounter))*self.freq #C'est pour prendre en compte les reset de compteurs : je prends le modulo 2^32 de la différence du nombre de coup pour être tjr positif
		return PL

	def setupWithPb(self,signal,freq,chan='auto'):
		if chan=='auto' : #ce sont les gate terminals des différents compteurs. Je pensais que le problème de ctr3 venait de la, mais visiblement c'est plus compliqué (la gate est court-circuité ? j'en sais rien)
			if self.physicalChannels[0] == 'ctr0' :
				chan='/Dev1/PFI9'
			if self.physicalChannels[0] == 'ctr1' :
				chan='/Dev1/PFI4'
			if self.physicalChannels[0] == 'ctr2' :
				chan='/Dev1/PFI1'
			if self.physicalChannels[0] == 'ctr3' :
				chan='/Dev1/PFI6'
		self.createTask()
		self.mode='withPB'
		self.freq=val(freq)
		mask=[el==2 for el in signal]
		self.sampsPerChan=sum(mask)*self.nRepeat
		self.task.timing.cfg_samp_clk_timing(self.freq,source=chan,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.sampsPerChan)
		self.start()

	def readPulsed(self,nRead='auto',counts=False) :
		if nRead=='auto':
			nRead=self.sampsPerChan
		else :
			nRead=nRead*self.nRepeat
		data=np.array(self.task.read(val(nRead),timeout=60))
		if counts :
			return data
		else :
			# PL=((data[1:]-data[:-1]))*self.freq
			PL=((data[1:]-data[:-1])%(1<<self.nBitsCounter))*self.freq #C'est pour prendre en compte les reset de compteurs : je prends le modulo 2^32 de la différence du nombre de coup pour être tjr positif
			return PL

	def read(self,nRead='auto') :
		if self.mode=='continuous' :
			return(self.readContinuous(nRead=nRead))
		if self.mode=='withPB' :
			return(self.readPulsed(nRead=nRead))	

class graphics(pg.GraphicsLayoutWidget) :
	def __init__(self,theme=defaultTheme,debug=False,refreshRate=False):
		self.theme=useTheme(theme)
		super().__init__()			
		self.norm=False
		self.autoSave=False
		self.refreshRate=refreshRate
		self.timeLastUpdate=time.time()
		self.debug=debug
		self.lines=[]
		self.infiniteLines=[]
		self.axes=[]
		self.mainAx=self.addAx(where=False)
	def addAx(self,where='bellow',title=None,verticalLines=True) :
		if where=='bellow' :
			self.nextRow()
		class myAx(pg.PlotItem): #And myAx !
			def __init__(self,title):
				super().__init__(title=title)
				self.currentPenIndex=0
				self.legend=self.addLegend(labelTextSize='15pt')
				self.infiniteLines=[]
			def clicked(self,e):
				pos=e[0]
				mousePoint = self.vb.mapSceneToView(pos.scenePos())
				if mousePoint.x() > ax.viewRange()[0][0] and mousePoint.x() < ax.viewRange()[0][1] and mousePoint.y() > ax.viewRange()[1][0] and mousePoint.y() < ax.viewRange()[1][1] :
					if pos.double() :
						if pos.button()==1 :
							l=self.addInfiniteLine(mousePoint.x())
						elif pos.button()==4 :
							self.clearInfiniteLines()
			def addLine(self,*args,**kwargs):
				return self.graphicsWidget.addLine(*args,ax=self,**kwargs)
			def addInfiniteLine(self,*args,**kwargs):
				return self.graphicsWidget.addInfiniteLine(*args,ax=self,**kwargs)
			def clearInfiniteLines(self):
				while self.infiniteLines != [] : #C'est un peu chelou, mais comme je supprime les élléments de la liste au fur et à mesure il comprend pas sinon
					line=self.infiniteLines[0]
					line.remove()
		ax=myAx(title=title)
		self.addItem(ax)
		ax.graphicsWidget=self
		self.axes+=[ax]
		if verticalLines :
			ax.proxy = pg.SignalProxy(ax.scene().sigMouseClicked, rateLimit=60, slot=ax.clicked)
		return ax
	def addLine(self,x=[],y=[],ax=False,typ='instant',style='lm',fast=False,label=False) : #style= :'l' =line, 'm' = marker, 'lm'=marker+line
		if not ax :
			ax=self.mainAx
		if len(x)==0 :
			x=np.linspace(0,10,100)
		if len(y)==0 :
			y=np.zeros(100)
		line=myLine(x,y,ax,theme=self.theme,typ=typ,style=style,fast=fast,label=label)
		line.update(x,y,norm=self.norm)
		line.reset()
		self.lines+=[line]
		line.graphicsWidget=self
		return line
	def addInfiniteLine(self,pos,angle=90,movable=True,ax=False):
		if not ax :
			ax=self.mainAx
		class myInfiniteLine(pg.InfiniteLine) :
			def __init__(self,pos,angle,movable):
				self.color=(100,100,100)
				super().__init__(pos=pos,angle=angle,movable=movable,pen=pg.mkPen(color=self.color,width=2))
				self.sigClicked.connect(self.clicked)
				self.sigPositionChanged.connect(self.moved) #Change to sigPositionChangeFinished if lagging
			def clicked(self,line,e):
				if e.button()==4 :
					self.remove()
			def remove(self):
				self.ax.removeItem(self)
				self.ax.removeItem(self.label)
				self.ax.infiniteLines.remove(self)
				self.graphicsWidget.infiniteLines.remove(self)
			def moved(self):
				line.label.moveToLine()
		line=myInfiniteLine(pos=pos,angle=angle,movable=movable)
		ax.addItem(line)
		self.infiniteLines+=[line]
		ax.infiniteLines+=[line]
		line.ax=ax
		line.graphicsWidget=self
		class infiniteLineLabel(pg.TextItem) :
			def __init__(self,line):
				self.line=line			
				super().__init__(color=line.color)
				self.setFont(QFont( "Consolas", 20, QFont.Bold))
				self.moveToLine()
				line.ax.addItem(self)
			def moveToLine(self):
				xAnch=self.line.pos()[0]
				yAnch=(self.line.ax.viewRange()[1][0]+self.line.ax.viewRange()[1][1])/2
				self.setPos(xAnch,yAnch)
				self.setText(repr_numbers(xAnch,precision=3))
		line.label=infiniteLineLabel(line)
		return line
	def clearInfinteLines(self):
		while self.infiniteLines != [] : #C'est un peu chelou, mais comme je supprime les élléments de la liste au fur et à mesure il comprend pas sinon
			line=self.infiniteLines[0]
			line.remove()
	def normalize(self,initialState=False,spaceAbove=0,spaceBelow=0):
		self.normWidget=checkBox(name='Normalize',action=self.normalizeActualize,initialState=initialState,spaceAbove=spaceAbove,spaceBelow=spaceBelow)
		return(self.normWidget)
	def normalizeActualize(self):
		self.norm=self.normWidget.state()
		for line in self.lines :
			self.updateLine(line,line.xData,line.trueY)
	def updateLine(self,line,x,y,noRefresh=False) :		
		if not(isinstance(y,np.ndarray) or isinstance(y,list)) : #sécurité si jamais tu envoies rien, il ne se passe rien
			return False
		if not(isinstance(x,np.ndarray) or isinstance(x,list)) :
			x=line.xData
		if isinstance(y,list):
			y=np.array(y)
		if isinstance(x,list):
			x=np.array(x)
		if self.refreshRate :
			t=time.time()
			if t > self.timeLastUpdate +self.refreshRate :
				line.update(x,y,self.norm,show=True)
				if not noRefresh :
					self.timeLastUpdate=t
			else :
				line.update(x,y,self.norm,show=False)
		else :
			line.update(x,y,self.norm,show=True)
		if self.autoSave :
			self.autoSave.check()
		return True

	def addToBox(self,box):
		box.addWidget(self)

class myLine(pg.PlotDataItem) :
	def __init__(self,x,y,ax,theme,typ='instant',style='lm',fast=False,label=False,**kwargs): #typ=='instant','scroll', 'average', 'hist', 'trace' or 'fit'
		self.theme=theme
		self.ax=ax
		self.typ=typ
		self.label=label
		self.trueY=y #Keep the real unnormalized value of y
		if self.typ=='hist':
			self.histSetup()
			#makes sure that histSetup is called at least once. You can call it again and overwrite the default parameters
		pen,symbol,symbolPen,symbolBrush,penIndex=self.theme.nextLine(ax,typ=typ)
		self.penIndex=penIndex
		if not 'l' in style :
			pen=None
		if not 'm' in style :
			symbolPen=None
		super().__init__(x,y,pen=pen,symbol=symbol,symbolPen=symbolPen,symbolBrush=symbolBrush,antialias=not fast,**kwargs)	#créé la ligne
		ax.addItem(self) #ajoute la ligne à l'axe
		if label :
			ax.legend.addItem(self,label)
		self.iteration=1
		self.nRepeat=1
		self.iterationWidget=False
	def histSetup(self,typ='fast',nBins=100,bounds='auto'):
		self.histType=typ #fast : the data is overwritten each time, you only keep the average of all the histograms. slow : you keep all the data and make a new histogram of it each time
		if typ=='slow' :
			self.histData=[] 
		self.histNbins=nBins
		if bounds=='auto' :
			self.histBoundsType='auto'
		else :
			self.histBoundsType='manual'
			self.histBounds=bounds
	def remove(self):
		self.ax.removeItem(self)
		self.ax.penIndices[self.penIndex]=True
		if self.label :
			self.ax.legend.removeItem(self)
		self.graphicsWidget.lines.remove(self)
	def clicked(self,ev): #self et line sont équivalents ici
		if self.typ=='trace' or self.typ=='fit' :
			if ev.double() :
				pass
				#Malheuresement y'a une erreur cheloue quand on supprimer la ligne ici qui vient du fait que la ligne n'existe plus pour la deusième phase de sigClicked
				
	def getIteration(self):
		return self.iteration

	def update(self,x,y,norm,show=True):
		oldY=self.trueY
		if self.typ=='instant' or self.typ=='trace' or self.typ=='fit':
			newY=y			
		elif self.typ=='average' :
			if self.iteration == 1 : #Mathématqiuement y'en a pas besoin mais sinon c'est galère avec les tailles
				newY=y
			else :			
				newY=oldY*(1-self.nRepeat/self.iteration)+y*self.nRepeat/self.iteration
		elif self.typ=='scroll' :
			n=len(y)
			if n>len(x) :
				raise ValueError('Scroll data length greater than total data')
			elif len(y)==len(x) :
				newY=y
			else :
				newY=np.roll(oldY,-n)
				newY[-n:]=y
		elif self.typ=='hist' :
			if self.histType=='fast' :
				if self.iteration==1 :
					oldY=np.zeros(self.histNbins)
					if self.histBoundsType=='auto':
						mu=analyse.mean(y)
						sigma=analyse.sigma(y)
						self.histBounds=[mu-5*sigma,mu+5*sigma]
				hist,bins=np.histogram(y,density=False,bins=val(self.histNbins),range=self.histBounds)
				x=(bins[1:]+bins[:-1])/2
				newY=oldY+hist
			elif self.histType=='slow' :
				self.histData+=list(y)
				if self.histBoundsType=='auto':
					mu=self.mu()
					sigma=self.sigma()
					self.histBounds=[mu-5*sigma,mu+5*sigma]
				hist,bins=np.histogram(self.histData,density=False,bins=val(self.histNbins),range=self.histBounds)
				x=(bins[1:]+bins[:-1])/2
				newY=hist
			elif self.histType=='instant' :
				if self.iteration==1 :
					oldY=np.zeros(self.histNbins)
					if self.histBoundsType=='auto':
						mu=analyse.mean(y)
						sigma=analyse.sigma(y)
						self.histBounds=[mu-5*sigma,mu+5*sigma]
				hist,bins=np.histogram(y,density=False,bins=val(self.histNbins),range=self.histBounds)
				x=(bins[1:]+bins[:-1])/2
				newY=hist
				self.histData=y

		self.trueY=newY
		self.x=x
		if norm :
			if self.typ=='hist' :
				ytoplot=self.trueY/sum(self.trueY)
			else :
				ytoplot=normalize(self.trueY)
		else :
			ytoplot=self.trueY
		if len(ytoplot) != len(x) :
			raise ValueError('len(x)=%i does not match len(y)=%i'%(len(x),len(ytoplot)))
		if show :
			pen,symbol,symbolPen,symbolBrush=self.theme.penSizeChange(self)
			self.setData(x,ytoplot,pen=pen,symbol=symbol,symbolPen=symbolPen,symbolBrush=symbolBrush)
		self.iteration+=self.nRepeat
		if self.iterationWidget :
			self.iterationWidget.update(self.iteration)

	def mu(self):
		if self.typ=='hist' :
			if self.histType=='fast':
				return analyse.hist_mean(self.x,self.trueY)
			elif self.histType=='slow' or self.histType=='instant':
				return analyse.mean(self.histData)
		else :
			return analyse.mean(self.trueY)
	def sigma(self):
		if self.typ=='hist' :
			if self.histType=='fast' :
				return analyse.hist_sigma(self.x,self.trueY)
			elif self.histType=='slow' or self.histType=='instant':
				return analyse.sigma(self.histData)
		else :
			return analyse.sigma(self.trueY)

	def setHistBounds(self,bmin,bmax):
		self.histBounds=[bmin,bmax]
	def setNBins(self,n):
		self.histNbins=n
	def reset(self):
		self.iteration=1
		if self.typ=='hist' and self.histType=='slow' :
			self.histData=[]

class iterationWidget():
	def __init__(self,line,spaceAbove=1,spaceBelow=0):
		self.label=QLabel('Iter #1')
		self.spaceAbove=spaceAbove
		self.spaceBelow=spaceBelow
		line.iterationWidget=self
		self.value=1
	def update(self,value):
		self.label.setText('Iter #%i'%value)
		self.value=value	
	def addToBox(self,box):
		box.addStretch(self.spaceAbove)
		box.addWidget(self.label)
		box.addStretch(self.spaceBelow)

class pulsedLaserWidget():
	def __init__(self,spaceAbove=1,spaceBelow=0,chan='ctr0',freq=20E6,ignoreWarning=False,gate=False,gateChan='/Dev1/PFI9'):
		self.laserCb=checkBox('Laser On',action=self.lasOnOff,spaceAbove=spaceAbove)
		self.laserFreq=field('Laser frequency',freq,spaceAbove=0)
		self.laser=pulsedLaserControl(channel=chan,ignoreWarning=ignoreWarning,gate=gate,gateChan=gateChan)
	def lasOnOff(self):
		if self.laserCb.state() :
			self.laser.start(self.laserFreq)
		else :
			self.laser.stop()
	def addToBox(self,box):
		self.laserCb.addToBox(box)
		self.laserFreq.addToBox(box)

class pulsedLaserControl():
	def __init__(self,channel='ctr0',gate=False,gateChan='/Dev1/PFI9',ignoreWarning=False):
		self.co=COChan(channel)
		self.state='Off'
		self.freq=0
		self.co.toBeClosed=False
		self.ignoreWarning=ignoreWarning
		self.gate=gate
		self.gateChan='/Dev1/PFI9'
	def start(self,freq):
		freq=val(freq)
		if self.state=='Off':
			self.freq=freq
			try :
				self.co.setupContinuous(self.freq,gate=self.gate,gateChan=self.gateChan)	
			except :
				if not self.ignoreWarning :
					warningGUI('Could not start pulsed laser \n Probably used in another program')
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
	def __init__(self,spaceAbove=1,spaceBelow=0,chanAOM='ao1',power=200E-6,PMType='USB',chanPM='ai9',caliber=1E-3,DCChan='p03'): #Power in W ; PMType='USB' or 'Analog'; caliber=power in W for U=1V
		self.laserCb=checkBox('Laser On',action=self.lasOnOff,spaceAbove=spaceAbove)
		self.laserPow=field('Laser power (W)',power,spaceAbove=0)
		self.AOM=AOChan(chanAOM)
		self.PMType=PMType
		self.DCChan=DCChan
		if self.PMType=='Analog' :
			self.PM=powerMeterAnalog(chan=chanPM,caliber=caliber)
		elif self.PMType=='USB' :
			self.PM=powerMeterUSB()

	def lasOnOff(self):
		if self.laserCb.state() :						
			self.setPower(val(self.laserPow))
		else :
			self.AOM.setupContinuous(0)
			self.AOM.close()

	def setPower(self,target,precision=0.001): #Precision in V on the AOM input
		self.AOM.setupContinuous(0)
		if self.DCChan :
			switch_do(self.DCChan,True)
		mini=0
		maxi=0.45
		if self.PMType=='Analog' :
			self.PM.setup()
		elif self.PMType=='USB' :
			self.PM.setup(powerRange=target*1.5)
		while maxi-mini > precision :
			val=(maxi+mini)/2
			self.AOM.updateContinuous(val)
			time.sleep(0.1)
			lect=self.PM.read()
			# print(lect,target)
			if lect > target :
				maxi=val
				# print(mini,maxi)
			else :
				mini=val
				# print(mini,maxi)
		realP=self.PM.read()
		self.laserPow.setValue(realP,precision=3)
		self.PM.close()
		self.AOM.close()
	def getPower(self):
		return(val(self.laserPow))
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

class powerMeterUSB(device):
	def __init__(self,ressourceName='tl_rouge'):
		super().__init__()
		if ressourceName=='tl_rouge':
			ressourceName='USB0::0x1313::0x8079::P1002303::INSTR'
		self.ressourceName=ressourceName
		#A noter que ça marche aussi avec du visa et self.PG.query('MEAS?'), j'ai juste pas accès au calibre vu que je connais pas la commande visa
		sys.path.append('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\TLPM\\Example\\Python')
		global TLPM,byref,c_double,c_bool,c_int16
		import TLPM
		from ctypes import byref,c_double,c_bool,c_int16
	def setup(self,powerRange=2E-3,wavelength=532): #range in [W], wl in [nm]
		self.tlPM = TLPM.TLPM()
		self.tlPM.open(b'USB0::0x1313::0x8079::P1002303::INSTR', c_bool(True), c_bool(True))
		self.tlPM.setPowerRange(c_double(powerRange))
		self.tlPM.setWavelength(c_double(wavelength))
		time.sleep(1.5) #The powermeter needs some time to adjust to the new caliber
	def read(self):	
		power=c_double()
		self.tlPM.measPower(byref(power))
		return(power.value)
	def close(self):
		try :
			self.tlPM.close()
		except :
			pass

class doubleSignal():
	def __init__(self,signal):
		pulsedSignal=[]
		for b in signal :
			if b :
				pulsedSignal+=[True,False]
			else :
				pulsedSignal+=[False,False]
		self.l=pulsedSignal

class AOMWidget(checkBox):
	def __init__(self,chan='p03',**kwargs) :
		super().__init__(name='AOM',**kwargs)
		self.setAction(self.action)
		self.do=DOChan(chan)
	def action(self):		
		self.do.setupContinuous(self.state(),close=True)



def failSafe(func,*args,debug=True):
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
		line.reset()

def average(y,nAvg=1,nRepeat=1): #see def of nAvg and nRepeat in NIChan
	if len(y)%nRepeat!=0 :
		raise ValueError('nRepeat does not divide the size of the array')
	nSeg=len(y)//nRepeat
	yRep=np.zeros(len(y)//(nRepeat*nAvg))
	for i in range(nRepeat) :
		ySeg=y[i*nSeg:(i+1)*nSeg]
		if len(ySeg)%nAvg!=0 :
			raise ValueError('nAvg does not divide the size of the array')
		yAvg=np.zeros(int(len(ySeg)/nAvg))
		for k in range(len(yAvg)):
			yAvg[k]=sum(ySeg[k*nAvg:(k+1)*nAvg])/nAvg
		yRep+=yAvg
	return yRep/nRepeat

def visualize(*chans): #args must be channels which have been timeSetuped
	offset=0
	theme=useTheme()
	graph=pg.plot()
	for i in range(len(chans)):
		chan=chans[i]
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
		offset+=1.5
		# myLine(x,y,graph,theme=theme,fast=True,style='l')
		pen,symbol,symbolPen,symbolBrush=theme.nextLine(graph)
		graph.plot(x,y,pen=(i,len(chans)),stepMode='left')

def warningGUI(message):
	try :
		GUI=get_objects(Graphical_interface)[0]
	except :
		print(message)
		raise(ValueError('Could not find graphical interface to print error message'))
	mb = QMessageBox(GUI)
	mb.setText(message)
	mb.show()

def ignoreWarnings(f,*args):
	with warnings.catch_warnings() :
		warnings.simplefilter('ignore')
		return f(*args)

def normalize(y): #y must be an arraylike
	if isinstance(y,list):
		y=np.array(y,dtype=float)
	if max(abs(y)) > 0 :
		y=y/max(abs(y))
	return y

def val(x):
	if isinstance(x, field) :
		x.updateValue()
		return x.v
	else :
		return x

def switch_do(chan,state):
	DO=DOChan(chan)
	DO.setupContinuous(state)
	DO.close()

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

def apply_repeat(nRepeat,*Objs):
	for obj in Objs :
		obj.nRepeat=val(nRepeat)

def extend_signal(signal,n):
	l=[]
	for elem in signal :
		l+=[elem]*n
	return l

def scale_signal(signal,baseFreq,newFreq=1e6):
	factor=newFreq/baseFreq
	if factor.is_integer() :
		factor=int(factor)
	else :
		raise ValueError("Can't scale up the signal to the new frequency")
	return extend_signal(signal,factor)

def repr_numbers(value,precision='exact'):
	value=value
	if isinstance(value,str):
		label=(value)
	elif value==0:
		label=('0')
	elif abs(value)>1E4 or abs(value) <1E-1 :
		if precision=='exact' :
			label=('%e'%value)
		else :
			label=('{:.{}e}'.format(value,precision))
	elif isinstance(value,int) :
		label=('%i'%value)
	else :
		if precision=='exact' :
			label=('%f'%value)
		else :
			label=('{:.{}f}'.format(value,precision))
	return label

def fhp(f,verbose,*args,**kwargs): ##fhp = function hidden print
	if verbose :
		return(f(*args,**kwargs))
	else :
		with hiddenPrints() :
			return(f(*args,**kwargs))

@contextmanager
def stdout_redirected(to=os.devnull):
	'''
	import os

	with stdout_redirected(to=filename):
		print("from Python")
		os.system("echo non-Python applications are also supported")
	'''
	fd = sys.stdout.fileno()

	##### assert that Python and C stdio write using the same file descriptor
	####assert libc.fileno(ctypes.c_void_p.in_dll(libc, "stdout")) == fd == 1

	def _redirect_stdout(to):
		sys.stdout.close() # + implicit flush()
		os.dup2(to.fileno(), fd) # fd writes to 'to' file
		sys.stdout = os.fdopen(fd, 'w') # Python writes to fd

	with os.fdopen(os.dup(fd), 'w') as old_stdout:
		with open(to, 'w') as file:
			_redirect_stdout(to=file)
		try:
			yield # allow code to be run with the redirected stdout
		finally:
			_redirect_stdout(to=old_stdout) # restore stdout.

def test_pg():
	def setup():
		return(x)
	def update(x):
		y=2*np.cos(x+time.time())
		gra.updateLine(l3,False,y)
		y0=np.cos(time.time())
		gra.updateLine(l1,False,[y0])
	def avertissement():
		warningGUI('Attention !')
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
	x=np.linspace(0,10,500)
	y=np.cos(x)
	gra=graphics()
	l1=gra.addLine(x,y,typ='scroll',label='L1')
	l2=gra.addLine(x,-y)
	ax2=gra.addAx()
	l3=ax2.addLine(x,-y,typ='instant',label='L3')


	ftoto=field('toto',10,spaceBelow=1)
	attention=button('Warning',avertissement)
	fields=[ftoto,attention]


	StartStop=startStopButton(setup=setup,update=update,debug=True,lineIter=l3,showMaxIter=True,serie=True)
	StartStop.setupSerie(nAcqui=3,iterPerAcqui=[100,150,50],acquiStart=acquiStart,acquiEnd=acquiEnd)
	save=saveButton(gra,autoSave=False)
	trace=keepTraceButton(l1,l3)
	it=iterationWidget(l3)
	norm=gra.normalize()
	# print(dir(gra.scene()))

	buttons=[norm,StartStop,trace,save,it]

	GUI=Graphical_interface(fields,gra,buttons,title='Example GUI')

	GUI.run()

def test_fitESR():
	from analyse import extract_data
	# x,y=extract_data('ESR 100 2V')
	# x=x*1000



	x,y=extract_data('ESR 1x1x1x1 2V')
	# x0s=[2626,2702,2805,2867,2989,3042,3115,3160]
	gra=graphics()
	l1=gra.addLine(x,y)
	fitESR=fitButton(line=l1,fit='ESR',name='fit ESR')
	GUI=Graphical_interface(fitESR,gra,title='test')
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

def test_laser():
	ao=AOChan('ao1')
	ao.setupContinuous(0.45)
	do=DOChan('p03')
	do.setupContinuous(False)

if __name__ == "__main__":
	test_pg()


