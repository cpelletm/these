from lab import *

physicalChannels=['ai13','ai11','ai9']

nSerie=100

chanGreen='p07'
chanRed='p02' #'p03' typiquement utilisé par l'AOM; 'p02' par le switch
chanLect='p06'
invertedGate=False

def acquiStart(i):
	pass

def acquiEnd(i):
	if i==0 :
		save.save(fname=fname,saveFigure=True)
	else :
		save.save(fname=fname,saveFigure=False)

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	apply_repeat(nRep,ai,do,l1)
	nRead=val(NRead)
	freq=nRead/val(tRead)

	nWait=int(freq*val(tWait))
	nPola=int(freq*val(tPola))
	totalTime=val(tWait)+val(tRead)+val(tPola)
	if fullView.state() :
		x=np.linspace(0,totalTime,(nWait+nRead+nPola))
		lect=[2]*(nWait+nRead+nPola)
	else :
		x=np.linspace(0,val(tRead),+nRead)
		lect=[False]*(nWait+1)+[2]*(nRead-1)+[False]*(nPola)
		x=x[1:]

	ai.setChannels(channels.text()) 
	nAvg=ai.setupPulsed(signal=lect,freq=freq,nAvg='auto')


	redLaserGate=[]
	greenLaserGate=[]
	if waitMenu.text()=='green' :
		greenLaserGate+=[not invertedGate]*nWait
		redLaserGate+=[False]*nWait
	elif waitMenu.text()=='red' :
		greenLaserGate+=[invertedGate]*nWait
		redLaserGate+=[True]*nWait
	elif waitMenu.text()=='both' :
		greenLaserGate+=[not invertedGate]*nWait
		redLaserGate+=[True]*nWait
	elif waitMenu.text()=='none' :
		greenLaserGate+=[invertedGate]*nWait
		redLaserGate+=[False]*nWait

	if readMenu.text()=='green' :
		greenLaserGate+=[not invertedGate]*nRead
		redLaserGate+=[False]*nRead
	elif readMenu.text()=='red' :
		greenLaserGate+=[invertedGate]*nRead
		redLaserGate+=[True]*nRead
	elif readMenu.text()=='both' :
		greenLaserGate+=[not invertedGate]*nRead
		redLaserGate+=[True]*nRead
	elif readMenu.text()=='none' :
		greenLaserGate+=[invertedGate]*nRead
		redLaserGate+=[False]*nRead

	if polaMenu.text()=='green' :
		greenLaserGate+=[not invertedGate]*nPola
		redLaserGate+=[False]*nPola
	elif polaMenu.text()=='red' :
		greenLaserGate+=[invertedGate]*nPola
		redLaserGate+=[True]*nPola
	elif polaMenu.text()=='both' :
		greenLaserGate+=[not invertedGate]*nPola
		redLaserGate+=[True]*nPola
	elif polaMenu.text()=='none' :
		greenLaserGate+=[invertedGate]*nPola
		redLaserGate+=[False]*nPola



	# lect+=[False]*10
	# greenLaserGate+=[invertedGate]*10
	# redLaserGate+=[False]*10

	do.setChannels(chanLect,chanGreen,chanRed)
	do.setupPulsed(ValuesList=[lect,greenLaserGate,redLaserGate],freq=freq,nAvg=nAvg,nRepeat=nRep)
	do.start()
	return x
	
## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x):
	
	if do.done() :
		y=ai.read(timeout=5)
		do.restart()
		gra.updateLine(l1,x,y) 
	

def extraStop() :
	do.setupContinuous([[False],[not invertedGate],[AOM.state()]])

def avgWidgAction() :
	if avgWidg.state():
		l1.typ='average'
	else :
		l1.typ='instant'

def uwOnOff():
	s=uwCB.state()
	if s:
		mw.setupContinuous(Frequency=uwfreq,Power=uwlvl)
	else :
		mw.close()



## Create the communication (I/O) instances ##
ai=AIChan()
do=DOChan()
cube=PiezoCube3axes()
mw=microwave('mw3')
mw.toBeClosed=False

## Setup the Graphical interface ##
# laser=continuousLaserWidget(power=2E-4,spaceAbove=0)
laser=pulsedLaserWidget(gate=True,invertedGate=invertedGate)
AOM=AOMWidget(chan=chanRed)
fullView=checkBox('Full View',spaceAbove=0)
fullView.setState(True)
uwCB=checkBox('Microwave On/Off',action=uwOnOff)
uwfreq=field('Frequency (MHz)',2880,spaceAbove=0)
uwlvl=field('Power (dBm)',15,spaceAbove=0)
waitMenu=dropDownMenu('pulse menu','none','green','red','both',spaceAbove=0)
tWait=field('dark time (s)',10e-3)
readMenu=dropDownMenu('pulse menu','none','green','red','both',spaceAbove=0)
readMenu.setIndex('both')
tRead=field('read time (s)',20e-3)
polaMenu=dropDownMenu('pulse menu','none','green','red','both',spaceAbove=0)
tPola=field('pola time(s)',10e-3)
NRead=field('n read',200)
nRep=field('n repeat',1,spaceAbove=0)
fields=[laser,AOM,fullView,uwCB,uwfreq,uwlvl,tWait,waitMenu,tRead,readMenu,tPola,polaMenu,NRead,nRep]

gra=graphics(refreshRate=0.1)
l1=gra.addLine(typ='instant',style='m',fast=True)

avgWidg=checkBox('instant/avg',action=avgWidgAction) #Uncheck = instant, check = avg
avgWidg.setState(True)
channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)
StartStop=startStopButton(setup=setup,update=update,serie=True,lineIter=l1,debug=True,extraStop=extraStop)
StartStop.setupSerie(nAcqui=nSerie,iterPerAcqui=200,acquiStart=acquiStart,acquiEnd=acquiEnd)
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(l1)
expfit=fitButton(line=l1,fit='exp',name='exp fit')
stretchfit=fitButton(line=l1,fit='stretch',name='stretch fit')
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
buttons=[channels,avgWidg,norm,StartStop,trace,expfit,stretchfit,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='Polarisation')
# setup()
# visualize(ai,do)
GUI.run()

