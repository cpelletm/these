from lab import *

physicalChannels=['ai13','ai11','ai9']

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
		lect=[True]*(nWait+nRead+nPola)
	else :
		x=np.linspace(0,val(tRead),+nRead)
		lect=([False]*(nWait+1)+[True]*(nRead-1)+[False]*(nPola))
		x=x[1:]
	ai.setChannels(channels.text()) 
	pulseLect=ai.setupPulsed(freq=freq,signal=lect)

	redLaserGate=[]
	greenLaserGate=[]
	if waitMenu.text()=='green' :
		greenLaserGate+=[True]*nWait
		redLaserGate+=[False]*nWait
	elif waitMenu.text()=='red' :
		greenLaserGate+=[False]*nWait
		redLaserGate+=[True]*nWait
	elif waitMenu.text()=='both' :
		greenLaserGate+=[True]*nWait
		redLaserGate+=[True]*nWait
	elif waitMenu.text()=='none' :
		greenLaserGate+=[False]*nWait
		redLaserGate+=[False]*nWait

	if readMenu.text()=='green' :
		greenLaserGate+=[True]*nRead
		redLaserGate+=[False]*nRead
	elif readMenu.text()=='red' :
		greenLaserGate+=[False]*nRead
		redLaserGate+=[True]*nRead
	elif readMenu.text()=='both' :
		greenLaserGate+=[True]*nRead
		redLaserGate+=[True]*nRead
	elif readMenu.text()=='none' :
		greenLaserGate+=[False]*nRead
		redLaserGate+=[False]*nRead

	if polaMenu.text()=='green' :
		greenLaserGate+=[True]*nPola
		redLaserGate+=[False]*nPola
	elif polaMenu.text()=='red' :
		greenLaserGate+=[False]*nPola
		redLaserGate+=[True]*nPola
	elif polaMenu.text()=='both' :
		greenLaserGate+=[True]*nPola
		redLaserGate+=[True]*nPola
	elif polaMenu.text()=='none' :
		greenLaserGate+=[False]*nPola
		redLaserGate+=[False]*nPola



	do.setChannels('p06','p07','p03')
	do.setupTimed(SampleFrequency=freq,ValuesList=[pulseLect,greenLaserGate,redLaserGate])
	do.start()
	return x
	
## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x):
	
	y=ai.read(timeout=30)
	gra.updateLine(l1,x,y) 
	do.restart()

def extraStop() :
	do.setupContinuous([[False],[False],[AOM.state()]])

def avgWidgAction() :
	if avgWidg.state():
		l1.typ='average'
	else :
		l1.typ='instant'

## Create the communication (I/O) instances ##
ai=AIChan()
do=DOChan()

## Setup the Graphical interface ##
# laser=continuousLaserWidget(power=2E-4,spaceAbove=0)
laser=pulsedLaserWidget(gate=True)
AOM=AOMWidget()
fullView=checkBox('Full View')
NRead=field('n read',200)
waitMenu=dropDownMenu('pulse menu','none','green','red','both',spaceAbove=0)
tWait=field('dark time (s)',1e-3)
readMenu=dropDownMenu('pulse menu','none','green','red','both',spaceAbove=0)
tRead=field('read time (s)',1e-3)
polaMenu=dropDownMenu('pulse menu','none','green','red','both',spaceAbove=0)
tPola=field('pola time(s)',1e-3)
nRep=field('n repeat',2)
fields=[laser,AOM,fullView,NRead,tWait,waitMenu,tRead,readMenu,tPola,polaMenu,nRep]

gra=graphics(refreshRate=0.1)
l1=gra.addLine(typ='instant',style='m',fast=True)

avgWidg=checkBox('instant/avg',action=avgWidgAction) #Uncheck = instant, check = avg
channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)
StartStop=startStopButton(setup=setup,update=update,debug=True,extraStop=extraStop)
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

