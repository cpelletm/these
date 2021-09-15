import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from lab import *

physicalChannels=['ai13','ai11','ai9']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	apply_repeat(nRep,ai,do,l1)
	n=val(nPoints)
	ai.setChannels(channels.text()) 
	signal=[True]*(n//2)+[True]*(n-n//2)
	x=np.linspace(0,n/val(fAcq),n)
	ai.setupTimed(SampleFrequency=fAcq,SamplesPerChan=len(signal),nAvg=nAvg,SampleMode='finite',sourceClock='do') 	
	do.setupTimed(SampleFrequency=fAcq,ValuesList=signal,nAvg=ai.nAvg)
	do.triggedOn(ai)
	return x
## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x):
	y=ai.readTimed(waitForAcqui=False)
	if not ai.running :
		gra.updateLine(l1,x,y) 

## Create the communication (I/O) instances ##
ai=AIChan()
do=DOChan('p03,p07')

## Setup the Graphical interface ##
laser=continuousLaserWidget(power=2E-4,spaceAbove=0)
fAcq=field('Freq acq (Hz)',2E5)
nPoints=field('n points',400)
nAvg=field('n avg',1)
nRep=field('n repeat',1)
fields=[laser,fAcq,nPoints,nAvg,nRep]

gra=graphics(refreshRate=0.1)
l1=gra.addLine(typ='average',style='m',fast=True)

channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)
StartStop=startStopButton(setup=setup,update=update,debug=True)
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(gra,l1)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
buttons=[channels,norm,StartStop,trace,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='Polarisation')
# setup()
# visualize(ai,do)
GUI.run()

