from lab import *

physicalChannels=['ai13','ai11','ai9']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	ai.setChannels(channels.text()) #define the physical pin on the Ni USB device where the tension should be read
	facq=nPoints/DeltaT
	x=np.linspace(0,val(DeltaT),val(nPoints))
	ai.setupTimed(SampleFrequency=facq,SamplesPerChan=nPoints,nAvg=nAvg,SampleMode='finite') #define the timing at which the samples are recorded by the NI USB device : frequency of acquisition, 
	if trigCB.state():
		ai.task.triggers.start_trigger.cfg_anlg_edge_start_trig(trigger_level=val(trigLvl))
	return x

## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x):
	y=ai.readTimed(waitForAcqui=False) #read the number of samples required in SamplesPerChan ; with waitForAcqui=True the program wil freeze until the acquisition is complete (more stable)
	if not ai.running :
		gra.updateLine(l1,x,y) #syntax : gra.updateline(lineToUpdate,xUpdate,yUpdate) ; send False to xUpdate if you do not want to update x ; for 'scroll' type lines only send the new values in yUpdate
## Create the communication (I/O) instances ##
ai=AIChan()
## Setup the Graphical interface ##
laser=pulsedLaserWidget()
AOM=AOMWidget(spaceAbove=0)
# laser=continuousLaserWidget()
nPoints=field('n points',151,spaceAbove=3)
nAvg=field('Average over :','auto',spaceAbove=1)
DeltaT=field('Total time (s)',3e-3,spaceAbove=1,spaceBelow=3)
trigCB=checkBox('Trigged (Pas suporté sur ce modèle)')
trigLvl=field('Trig lvl (V)',0,spaceAbove=0)
fields=[laser,AOM,nPoints,nAvg,DeltaT,trigCB,trigLvl]

gra=graphics()
l1=gra.addLine(typ='instant',style='l',fast=True)
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
GUI=Graphical_interface(fields,gra,buttons,title='Oscillo')
GUI.run()
