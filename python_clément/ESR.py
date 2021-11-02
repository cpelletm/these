from lab import *

physicalChannels=['ai11','ai13']

## setup() is executed once at the beginning of each loop (when start is pressed) ##

Voltages=np.linspace(1,3,300)
def acquiStart(i):
	v=Voltages[i]
	ao.setupContinuous(v)

def acquiEnd(i):
	fname=StartStop.defaultFolder+'V=%f'%(Voltages[i])+' V'
	save.save(fname=fname)

def setup(): 
	if AM.state():
		mod='AM'
	else :
		mod=False
	n=val(nPoints)
	f=val(fsweep)

	mw.setupESR(F_min=fmin,F_max=fmax,Power=level,N_points=n,mod=mod,AM_Depth=AMDepth)
	ai.setChannels(channels.text())
	ai.setupTimed(SampleFrequency=f,SamplesPerChan=n,nAvg='auto')

	doSequence=[True,False]*n
	do.setupTimed(SampleFrequency=2*f,ValuesList=doSequence)
	do.triggedOn(ai)

	x=np.linspace(val(fmin),val(fmax),n)
	return x

## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x):
	y=ai.read(waitForAcqui=False)
	if not ai.running :
		gra.updateLine(l1,x,y)

def AM_OnOff():
	AMDepth.setEnabled(AM.state())

def switchAction():
	switchState=switchButton.state()
	switchDo=DOChan('p02')
	switchDo.setupContinuous(switchState,close=True)
## Create the communication (I/O) instances ##
ai=AIChan()
do=DOChan('p01')
ao=AOChan('ao0')
mw=microwave('mw_ludo')
## Setup the Graphical interface ##
channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)

fmin=field('min freq (MHz)',2800,spaceAbove=3)
fmax=field('max freq (MHz)',2950,spaceAbove=0)
level=field('power (dBm)',0.)

AM=checkBox('Amplitude Modulation',action=AM_OnOff)
AMDepth=field('AM depth (%)',100,spaceAbove=0)
AM.setState(True)
AMDepth.setEnabled(AM.state())

switchButton=checkBox('Switch On',action=switchAction)

nPoints=field('n points',151,spaceAbove=3)
fsweep=field('sweep frequency (Hz)',300,spaceAbove=0)

fields=[channels,fmin,fmax,level,AM,AMDepth,switchButton,nPoints,fsweep]

gra=graphics()
l1=gra.addLine(typ='average',style='lm')

StartStop=startStopButton(setup=setup,update=update,debug=True,serie=True,lineIter=l1,showMaxIter=True)
StartStop.setupSerie(nAcqui=len(Voltages),iterPerAcqui=20,acquiStart=acquiStart,acquiEnd=acquiEnd)
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(l1)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
fit=fitButton(line=l1,fit='ESR',name='fit ESR')
buttons=[norm,StartStop,trace,fit,save,it]

def ESRInLine(Fmin,Fmax,Power,NPoints,NRuns,Fsweep=300,AmpMod=True):
	if AmpMod :
		AM.setState(True)
	fmin.setValue(Fmin)
	fmax.setValue(Fmax)
	level.setValue(Power)
	nPoints.setValue(NPoints)
	fsweep.setValue(Fsweep)
	AM.setState(AmpMod)
	if AmpMod :
		channels.setIndex('ai11')
	else :
		channels.setIndex('ai13')
	switchDo=DOChan('p02')
	switchDo.setupContinuous(True,close=True)
	gateLaser=DOChan('p07')
	gateLaser.setupContinuous(True,close=True)
	l1.reset()
	x=setup()
	while l1.iteration < NRuns+1 :
		update(x)
	ai.close()
	do.close()
	mw.close()
	switchDo.setupContinuous(False,close=True)
	x=l1.x
	y=l1.trueY
	return (x,y)

## Create the graphical interface and launch the program ##
if __name__ == "__main__":
	GUI=Graphical_interface(fields,gra,buttons,title='ESR')
	GUI.run()