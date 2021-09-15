from lab import *

physicalChannels=['ai13','ai11','ai9']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	apply_repeat(nRep,ai,do,l1)
	nRead=val(NRead)
	freq=nRead/val(tRead)
	nWait=int(freq*val(tWait))
	totalTime=val(tWait)+val(tRead)
	if fullView.state() :
		x=np.linspace(0,totalTime,(nWait+nRead))
		lect=[True]*(nWait+nRead)
	else :
		x=np.linspace(0,val(tRead),+nRead)
		lect=([False]*(nWait+1)+[True]*(nRead-1))
		x=x[1:]
	ai.setChannels(channels.text()) 
	pulseLect=ai.setupPulsed(freq=freq,signal=lect)
	gateLaser=[False]*nWait+[True]*nRead
	do.setupTimed(SampleFrequency=freq,ValuesList=[pulseLect,gateLaser])
	do.start()
	return x
	
## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x):
	if do.done():
		y=ai.read()
		gra.updateLine(l1,x,y) 
		do.restart()

def extraStop() :
	do.setupContinuous([[True],[True]])

## Create the communication (I/O) instances ##
ai=AIChan()
do=DOChan('p06','p07')

## Setup the Graphical interface ##
# laser=continuousLaserWidget(power=2E-4,spaceAbove=0)
laser=pulsedLaserWidget(gate=True)
fullView=checkBox('Full View')
NRead=field('n read',200)
tWait=field('dark time (s)',1e-3)
tRead=field('read time (s)',1e-3)
nRep=field('n repeat',2)
fields=[laser,fullView,NRead,tWait,tRead,nRep]

gra=graphics(refreshRate=0.1)
l1=gra.addLine(typ='average',style='m',fast=True)

channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)
StartStop=startStopButton(setup=setup,update=update,debug=True,extraStop=extraStop)
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(l1)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
buttons=[channels,norm,StartStop,trace,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='Polarisation')
# setup()
# visualize(ai,do)
GUI.run()

