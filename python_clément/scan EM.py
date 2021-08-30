from lab import *


## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	n=val(nPoints)
	xmin=val(vmin)
	xmax=val(vmax)
	xmed=xmin+xmax/2
	nstart=n//2
	nend=nstart+n
	voltageSignal=np.concatenate((np.linspace(xmed,xmin,nstart),np.linspace(xmin,xmax,n),np.linspace(xmax,xmed,nstart)))
	nTot=len(voltageSignal)

	ao.setupTimed(SampleFrequency=fsweep,ValuesList=voltageSignal)
	ai.setupTimed(SampleFrequency=fsweep,SamplesPerChan=nTot,nAvg=nAvg)
	ao.triggedOn(ai)
	x=voltageSignal[nstart:nend]
	return(nstart,nend,x)


## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(nstart,nend,x):
	y=ai.readTimed(waitForAcqui=False)
	if not ai.running :
		y1=y[0][nstart:nend]
		y2=y[1][nstart:nend]
		gra.updateLine(l1,x,y1)
		gra.updateLine(l2,x,y2)


def laserOnOff():
	if laserCb.state() :
		co.setChannels('ctr0')
		co.setupContinuous(laserFreq)
	else :
		co.close()


## Create the communication (I/O) instances ##
ai=AIChan('ai11','ai13')
ao=AOChan('ao0')
co=COChan()
co.toBeStopped=False

## Setup the Graphical interface ##

laserCb=checkBox('Laser On',action=laserOnOff)
laserFreq=field('Laser frequency',20E6,spaceAbove=0)
vmin=field('V min (V)',-5,spaceAbove=3)
vmax=field('V max (V)',5,spaceAbove=0)
nPoints=field('n points',151,spaceAbove=3)
nAvg=field('Average over :',10,spaceAbove=1)
fsweep=field('sweep frequency (Hz)',300,spaceAbove=0)

fields=[laserCb,laserFreq,vmin,vmax,nPoints,nAvg,fsweep]

gra=graphics()
l1=gra.addLine(typ='average',style='lm')
ax2=gra.addAx()
l2=gra.addLine(typ='average',style='lm',ax=ax2)

StartStop=startStopButton(setup=setup,update=update,debug=True,resetAO=True)
save=saveButton(gra,autoSave=10)
trace=keepTraceButton(gra,l1,l2)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
buttons=[norm,StartStop,trace,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='Scan EM')
GUI.run()