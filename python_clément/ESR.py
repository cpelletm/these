from lab import *

physicalChannels=['ai11','ai13']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
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
	y=ai.readTimed(waitForAcqui=False)
	if not ai.running :
		gra.updateLine(l1,x,y)

def AM_OnOff():
	AMDepth.setEnabled(AM.state())

## Create the communication (I/O) instances ##
ai=AIChan()
do=DOChan('p01')
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

nPoints=field('n points',151,spaceAbove=3)
fsweep=field('sweep frequency (Hz)',300,spaceAbove=0)

fields=[channels,fmin,fmax,level,AM,AMDepth,nPoints,fsweep]

gra=graphics()
l1=gra.addLine(typ='average',style='lm')

StartStop=startStopButton(setup=setup,update=update,debug=True,lineIter=l1,showMaxIter=True)
save=saveButton(gra,autoSave=10)
trace=keepTraceButton(l1)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
buttons=[norm,StartStop,trace,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='ESR')
GUI.run()