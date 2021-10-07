import sys
sys.path.append("C:\\Users\\Tom\\Documents\\GitHub\\these\\python_clément")
from lab import *

physicalChannels=['ctr0','ctr3']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	trigAcqui=[2,2]
	pb.setupPulsed(dt=dt,ch1=trigAcqui)
	ci.setChannels(channels.text()) #define the physical pin on the Ni USB device where the tension should be read
	ci.setupWithPb(freq=1/dt,signal=trigAcqui)
	# number of samples to be read each time ai.readTimed() is called, number of samples to be average over and sampling mode : 'continuous' or 'finite' (please always use 'finite')
	if len(l1.xData) != val(nPoints) : #condition to avoid being stuck at 0 PL the first time the program is launched, optional
		pb.start()
		while not pb.isDone():
			pass
		y0=ci.read()[0]
		x=np.linspace(0,val(dt)*val(nPoints),val(nPoints))
		y=np.ones(val(nPoints))*y0
		gra.updateLine(l1,x,y)

## update() is executed for each iteration of the loop (until stop is pressed) ##
def update():
	pb.start()
	y=ci.read()	
	gra.updateLine(l1,False,y) #syntax : gra.updateline(lineToUpdate,xUpdate,yUpdate) ; send False to xUpdate if you do not want to update x ; for 'scroll' type lines only send the new values in yUpdate
	PL.setText('%3.2E'%y[0]) #Modify the PL label with the last acquisition point


## Create the communication (I/O) instances ##
pb=pulseBlaster(chanOn=[])
ci=CIChan()
## Setup the Graphical interface ##

nPoints=field('n points',151,spaceAbove=3)
dt=field('dt (s)',0.03,spaceAbove=1,spaceBelow=3)
PL=label('Off',style='BIG',spaceAbove=0)
fields=[PL,nPoints,dt]

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
