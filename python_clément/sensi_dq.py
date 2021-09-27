from lab import *

physicalChannels=['ai11','ai13','ai9']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	ai.setChannels(channels.text()) 
	freq=nPoints/switchTime
	ai.setupTimed(SampleFrequency=freq,SamplesPerChan=nPoints,nAvg='auto',SampleMode='finite') 
	Vplus=V0+dV/2
	Vmoins=V0-dV/2
	ao.setupContinuous(Vmoins,close=False)
	time.sleep(val(deadTime))
	return(Vplus,Vmoins)


## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(Vplus,Vmoins):
	y=ai.readTimed(waitForAcqui=False)
	if not ai.running :
		gra.updateLine(l1,False,y) 
		ao.updateContinuous(Vplus)
		time.sleep(val(deadTime))
		y2=ai.readTimed(waitForAcqui=True)
		gra.updateLine(l2,False,y2) 
		diff=np.array(l1.histData) - np.array(l2.histData) 
		mean=abs(analyse.mean(diff))
		sigma=analyse.sigma(diff)
		s=sigma/mean*dV*conversion*np.sqrt(val(lowpass))
		sensi.setText('sensi=%3.2e T/sqrt(Hz)'%s)
		ao.updateContinuous(Vmoins)
		time.sleep(val(deadTime))


## Create the communication (I/O) instances ##
ai=AIChan()
ao=AOChan('ao0')
## Setup the Graphical interface ##

sensi=label('sensi=',style='big',spaceAbove=0)
conversion=field('Conversion U->B (T/V)',3.5e-3)
switchTime=field('switch time (s)',0.1)
deadTime=field('dead time (s)',0.025,spaceAbove=0)
nPoints=field('n points',1000,spaceAbove=0)
nBins=field('n bins',100)
V0=field('V0 (V)',0.05)
dV=field('dV (V)',1e-2,spaceAbove=0)
lowpass=field('lowpass filter (s)',3e-3)
fields=[sensi,V0,dV,conversion,switchTime,deadTime,nPoints,lowpass,nBins]

gra=graphics()
l1=gra.addLine(typ='hist',style='lm',fast=False)
l1.histSetup(typ='slow',nBins=nBins)
l2=gra.addLine(typ='hist',style='lm',fast=False)
l2.histSetup(typ='slow',nBins=nBins)
#typ='scroll' for scrolling data, 'average' for averaging data or 'instant' for immediate data
#style='l', 'm' or 'lm' for lines and/or marker
#fast=True/False (default False) : apply antialias or not on the lines. With anti-alias (fast=False), it takes ~0.1s to update a set with a lot of lines

channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)
StartStop=startStopButton(setup=setup,update=update,debug=True)
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(l1)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
buttons=[channels,norm,StartStop,trace,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='Sensi DQ')
GUI.run()
