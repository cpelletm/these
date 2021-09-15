from lab import *

physicalChannels=['ai13','ai11','ai9']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	ai.setChannels(channels.text()) 
	ai.setupTimed(SampleFrequency=freq,SamplesPerChan=nPoints,nAvg=nAvg,SampleMode='finite') 

## update() is executed for each iteration of the loop (until stop is pressed) ##
def update():
	try :
		y=ai.readTimed(waitForAcqui=False) #read the number of samples required in SamplesPerChan ; with waitForAcqui=True the program wil freeze until the acquisition is complete (more stable)
	except :
		return
	if not ai.running :
		gra.updateLine(l1,False,y) #syntax : gra.updateline(lineToUpdate,xUpdate,yUpdate) ; send False to xUpdate if you do not want to update x ; for 'scroll' type lines only send the new values in yUpdate
		mu.setText('mu=%3.2E'%l1.mu) 
		sigma.setText('sigma=%3.2E'%l1.sigma) 
		qapp.processEvents() #Ok ça et le try du dessus c'est ma conclusion après 4h pour avoir un truc qui marche vite tout le temps. En théorie faut pas utiliser processEvents mais c'est tout ce que j'ai pu trouver d'efficace
## Create the communication (I/O) instances ##
ai=AIChan()
## Setup the Graphical interface ##
laser=continuousLaserWidget(power=2E-4)
nPoints=field('n points',151,spaceAbove=3)
nAvg=field('Average over :','auto',spaceAbove=1)
freq=field('Acquisition frequency',1000)
mu=label('mu=',style='big',spaceAbove=0)
sigma=label('sigma=',style='big',spaceAbove=0)
fields=[mu,sigma,laser,nPoints,nAvg,freq]

gra=graphics()
l1=gra.addLine(typ='hist',style='m',fast=True)
l1.setNBins(50)
#typ='scroll' for scrolling data, 'average' for averaging data or 'instant' for immediate data
#style='l', 'm' or 'lm' for lines and/or marker
#fast=True/False (default False) : apply antialias or not on the lines. With anti-alias (fast=False), it takes ~0.1s to update a set with a lot of lines

channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)
StartStop=startStopButton(setup=setup,update=update,debug=True)
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(gra,l1)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
buttons=[channels,norm,StartStop,trace,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='Bruit Basique')
GUI.run()
