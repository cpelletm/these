from lab import *

physicalChannels=['ai13','ai11','ai9']

Voltages=np.linspace(-1,1,100)
def acquiStart(i):
	v=Voltages[i]
	ao.setupContinuous(v)

def acquiEnd(i):
	fname=StartStop.defaultFolder+'V=%f'%(Voltages[i])+' V'
	save.save(fname=fname)

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	apply_repeat(nRep,ai,do,l1)
	ai.setChannels(channels.text()) 
	freq=nT1/tT1
	dt=1/freq
	nPola=int(freq*tPola)
	nRead=int(freq*tRead)
	gateLaser=[True]*nPola
	readSignal=[False]*nPola
	x=[]
	for i in range(1,nT1+1):
		gateLaser+=[False]*i+[True]*nPola
		readSignal+=[False]*i+[True]*nRead+[False]*(nPola-nRead)
		x+=[i*dt]
	pulseRead=ai.setupPulsed(freq=freq,signal=readSignal)
	do.setupTimed(SampleFrequency=freq,ValuesList=[pulseRead,gateLaser])
	do.start()
	return x,nRead,val(nT1)
	
## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x,nRead,nT1):
	if True:
		data=ai.read()
		y=[]
		for i in range(nT1):
			segment=data[i*nRead:(i+1)*nRead]
			if maxwidg.state():
				y+=[sum(segment[nRead//2:])-sum(segment[:nRead//2])]
			else :
				y+=[sum(segment)/max(segment)]
		gra.updateLine(l1,x,y) 
		do.restart()

def extraStop() :
	do.setupContinuous([[False],[True]])

## Create the communication (I/O) instances ##
ai=AIChan()
ao=AOChan('ao0')
do=DOChan('p06','p07')

## Setup the Graphical interface ##
# laser=continuousLaserWidget(power=2E-4,spaceAbove=0)
laser=pulsedLaserWidget(gate=True,spaceAbove=0)
nT1=field('n points',200)
tT1=field('max time (s)',2e-3)
tRead=field('read time (s)',2e-4)
tPola=field('polarisation time (s)',1e-3)
nRep=field('n repeat',2)
fields=[laser,nT1,tT1,tRead,tPola,nRep]

gra=graphics(refreshRate=0.1)
l1=gra.addLine(typ='average',style='m',fast=True)

maxwidg=checkBox('max/last')
channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)
StartStop=startStopButton(setup=setup,update=update,debug=True,serie=True,lineIter=l1,extraStop=extraStop)
StartStop.setupSerie(nAcqui=len(Voltages),iterPerAcqui=30,acquiStart=acquiStart,acquiEnd=acquiEnd)
expfit=fitButton(line=l1,fit='exp',name='exp fit')
stretchfit=fitButton(line=l1,fit='stretch',name='stretch fit')
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(l1)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
buttons=[channels,maxwidg,norm,StartStop,trace,expfit,stretchfit,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='T1')
# setup()
# visualize(ai,do)
GUI.run()

