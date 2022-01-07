from lab import *

physicalChannels=['ai13','ai11','ai9']

nSide=30
zs=np.linspace(-5,5,nSide)
ys=np.linspace(0,10,nSide)

# laser_freqs=np.linspace(2E6,2E7,10)

# nLine=30
# ys=np.linspace(0,10,nLine)

def acquiStart(i):
	iz=i%nSide
	iy=i//nSide
	zV=zs[iz]
	yV=ys[iy]
	cube.move(zV,ax='z')	
	cube.move(yV,ax='y')

	# laser.laserFreq.setValue(laser_freqs[i])
	# laser.lasOnOff()

	# yV=ys[i]
	# cube.move(yV,ax='y')

def acquiEnd(i):
	iz=i%nSide
	iy=i//nSide
	zV=zs[iz]
	yV=ys[iy]
	fname=StartStop.defaultFolder+'z=%f,y=%f'%(zV,yV)

	# laser.laser.stop()
	# fname='fLas=%f'%laser_freqs[i]

	# yV=ys[i]
	# fname=StartStop.defaultFolder+'x=0,y=%f'%(yV)
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
	nAvg=ai.setupPulsed(signal=lect,freq=freq,nAvg=nAvgWidg)


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



	lect+=[False]*10
	greenLaserGate+=[False]*10
	redLaserGate+=[False]*10

	do.setChannels('p06','p07','p03')
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
	do.setupContinuous([[False],[True],[AOM.state()]])

def avgWidgAction() :
	if avgWidg.state():
		l1.typ='average'
	else :
		l1.typ='instant'

## Create the communication (I/O) instances ##
ai=AIChan()
do=DOChan()
cube=PiezoCube3axes()

## Setup the Graphical interface ##
# laser=continuousLaserWidget(power=2E-4,spaceAbove=0)
laser=pulsedLaserWidget(gate=True)
AOM=AOMWidget()
fullView=checkBox('Full View')
fullView.setState(True)
NRead=field('n read',200)
waitMenu=dropDownMenu('pulse menu','none','green','red','both',spaceAbove=0)
tWait=field('dark time (s)',10e-3)
readMenu=dropDownMenu('pulse menu','none','green','red','both',spaceAbove=0)
readMenu.setIndex('both')
tRead=field('read time (s)',20e-3)
polaMenu=dropDownMenu('pulse menu','none','green','red','both',spaceAbove=0)
tPola=field('pola time(s)',10e-3)
nRep=field('n repeat',1)
nAvgWidg=field('n avg','auto')
fields=[laser,AOM,fullView,NRead,tWait,waitMenu,tRead,readMenu,tPola,polaMenu,nRep,nAvgWidg]

gra=graphics(refreshRate=0.1)
l1=gra.addLine(typ='instant',style='m',fast=True)

avgWidg=checkBox('instant/avg',action=avgWidgAction) #Uncheck = instant, check = avg
avgWidg.setState(False)
channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)
StartStop=startStopButton(setup=setup,update=update,serie=True,lineIter=l1,debug=True,extraStop=extraStop)
StartStop.setupSerie(nAcqui=nSide**2,iterPerAcqui=200,acquiStart=acquiStart,acquiEnd=acquiEnd)
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

