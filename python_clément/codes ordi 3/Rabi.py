import sys
sys.path.append("D:\\these\\python_clément")
sys.path.append('D:\\These Clément\\these\\python_clément')
from lab import *

physicalChannels=['ai10']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 

	pb.setType('finite')
	ai.setChannels(channels.text()) #define the physical pin on the Ni USB device where the tension should be read

	nAvg=ai.setupPulsed(signal=nPoints,freq=1e6/tpola)
	freq=ai.freq
	dtAcqui=1/freq
	tlist=np.linspace(val(tmin),val(tmax),val(nPoints))
	#ch1=laser, ch2= mw, ch3= ??, ch4=PL
	pb.addLine(ch1=1,dt=tpola+tread,unit='us')
	for t in tlist :
		pb.addLine(ch2=1,dt=t,unit='ns')
		pb.addPulses(ch1=1,ch4=2,dt=dtAcqui,unit='s')


	pb.start()

	return(tlist)

## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x):
	if ai.done() :
		y=ai.read()
		pb.restart()
		gra.updateLine(l1,x,y) 


## Create the communication (I/O) instances ##
pb=pulseBlasterInterpreter()
mw=microwave('mw_ludo')
ai=AIChan()
## Setup the Graphical interface ##

uwFreq=field('mw freq (MHz)',2880)
uwPower=field('mw power (dBm)',5,spaceAbove=0)

tmin=field('t pulse min (ns)',20)
tmax=field('t pulse max (ns)',1000,spaceAbove=0)
nPoints=field('n points pulse',151,spaceAbove=0)

tpola=field('t polarisation (µs)',500)
tread=field('t read (µs)',500,spaceAbove=0)
fields=[uwFreq,uwPower,tmin,tmax,nPoints,tpola,tread]

gra=graphics(theme='black')
l1=gra.addLine(typ='scroll',style='lm',fast=True)
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
GUI=Graphical_interface(fields,gra,buttons,title='PL+PB',theme='dark')
GUI.run()
