import sys
sys.path.append("D:\\these\\python_clément")
sys.path.append('D:\\These Clément\\these\\python_clément')
from lab import *

physicalChannels=['ai10']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 

	pb.setType('finite')
	#ch1=laser, ch2= ??, ch3= mw, ch4=PL
	ai.setChannels(channels.text()) #define the physical pin on the Ni USB device where the tension should be read


	if fullView.state() :
		nPointsPola=int(nPoints*tpola/tread)
		nPointsRead=int(nPoints*tread/tread)
		nPointsDark=int(nPoints*tdark/tread)
		nPointsTotal=nPointsPola+nPointsRead+nPointsDark
		facq=1e6/tread*nPointsRead
		nAvg=ai.setupPulsed(signal=nPointsTotal,freq=facq)
		freqPB=ai.freq
		dtPB=1/freqPB
		nPBPola=nPointsPola*nAvg
		nPBRead=nPointsRead*nAvg
		nPBDark=nPointsDark*nAvg
		pb.addPulses(ch1=1,ch4=2,dt=dtPB,unit='s',nLoop=nPBPola)
		pb.addPulses(ch1=0,ch4=2,dt=dtPB,unit='s',nLoop=nPBDark)
		pb.addPulses(ch1=1,ch4=2,dt=dtPB,unit='s',nLoop=nPBRead)
		x=np.linspace(0,dtPB*(nPBPola+nPBRead+nPBDark),nPointsTotal)
	else :
		nPointsTotal=val(nPoints)
		facq=1e6/tread*nPoints
		nAvg=ai.setupPulsed(signal=nPointsTotal,freq=facq)
		freqPB=ai.freq
		dtPB=1/freqPB
		nPB=nPointsTotal*nAvg
		pb.addLine(ch1=1,dt=tpola,unit='us')
		pb.addLine(ch1=0,dt=tdark,unit='us')
		pb.addPulses(ch1=1,ch4=2,dt=dtPB,unit='s',nLoop=nPB)
		x=np.linspace(0,dtPB*nPB,nPointsTotal)
	


	pb.load()
	pb.start()

	return(x)

## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x):
	if ai.done() :
		y=ai.read()
		pb.restart()
		gra.updateLine(l1,x,y) 


## Create the communication (I/O) instances ##
pb=pulseBlasterInterpreter()
ai=AIChan()
## Setup the Graphical interface ##



fullView=checkBox('Full View')
fullView.setState(True)
tdark=field('t dark (µs)',500)
tpola=field('t polarisation (µs)',500,spaceAbove=0)
tread=field('t read (µs)',500,spaceAbove=0)
nPoints=field('n points pulse',151)
fields=[fullView,tdark,tread,tpola,nPoints]

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
GUI=Graphical_interface(fields,gra,buttons,title='Rabi',theme='dark')
GUI.run()
