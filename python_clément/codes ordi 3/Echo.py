import sys
sys.path.append("D:\\these\\python_clément")
sys.path.append('D:\\These Clément\\these\\python_clément')
from lab import *

physicalChannels=['ai10']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 

	pb.setType('finite')
	ai.setChannels(channels.text()) #define the physical pin on the Ni USB device where the tension should be read

	nAvg=ai.setupPulsed(signal=nPoints,freq=1e6/tread)
	freq=ai.freq
	dtAcqui=1/freq
	tlist=np.linspace(0,val(tscan),val(nPoints))
	tpi=val(tpulse)
	#ch1=laser, ch2= ??, ch3= mw, ch4=PL
	pb.addLine(ch1=1,dt=tpola+tread,unit='us')
	keepLasOn=laserOn.state()
	for t in tlist :
		pb.addLine(ch1=keepLasOn,ch3=1,dt=tpi/2,unit='ns')
		pb.addLine(ch1=keepLasOn,dt=t/2,unit='us')
		pb.addLine(ch1=keepLasOn,ch3=1,dt=tpi,unit='ns')
		pb.addLine(ch1=keepLasOn,dt=t/2,unit='us')
		pb.addLine(ch1=keepLasOn,ch3=1,dt=tpi/2,unit='ns')
		pb.addPulses(ch1=1,ch4=2,dt=dtAcqui,unit='s',nLoop=nAvg)
		pb.addLine(ch1=1,dt=tpola,unit='us')


	mw.setupContinuous(Frequency=uwFreq,Power=uwPower)

	pb.lastInst(ch1=1)
	pb.load()
	pb.start()

	return(tlist)

## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x):
	if ai.done() :
		y=ai.read()
		pb.start()
		gra.updateLine(l1,x,y) 


## Create the communication (I/O) instances ##
pb=pulseBlasterInterpreter()
mw=microwave('mw_ludo')
ai=AIChan()
## Setup the Graphical interface ##

laserOn=checkBox('Laser ON')
laserOn.setState(True)

uwFreq=field('mw freq (MHz)',2880)
uwPower=field('mw power (dBm)',5,spaceAbove=0)
tpulse=field('t pulse pi (ns)',500,spaceAbove=0)

tscan=field('t scan (us)',10)
nPoints=field('n points pulse',151,spaceAbove=0)

tpola=field('t polarisation (µs)',500)
tread=field('t read (µs)',500,spaceAbove=0)
fields=[laserOn,uwFreq,uwPower,tpulse,tscan,nPoints,tpola,tread]

gra=graphics(theme='black')
l1=gra.addLine(typ='average',style='lm',fast=True)
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
GUI=Graphical_interface(fields,gra,buttons,title='Echo',theme='dark')
GUI.run()
