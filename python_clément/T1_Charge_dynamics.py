from lab import *

physicalChannels=['ai13','ai11','ai9']

nLine=30
ys=np.linspace(0,10,nLine)

def acquiStart(i):
	yV=ys[i]
	cube.move(yV,ax='y')

def acquiEnd(i):
	yV=ys[i]
	fname=StartStop.defaultFolder+'x=0,y=%f'%(yV)

	if i==0 :
		save.save(fname=fname,saveFigure=True)
	else :
		save.save(fname=fname,saveFigure=False)

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	ai.setChannels(channels.text()) 
	freq=1e5 #rustine
	dt=tT1/nT1
	nWait=int(freq*dt)
	if nWait == 0 :
		raise ValueError('Check moi ce paquet de spaghettis')
	nPola=int(freq*tPola)
	nRead=int(freq*tRead)
	gateLaser=[True]*nPola
	readSignal=[False]*nPola
	x=[]
	for i in range(1,nT1+1):
		gateLaser+=[False]*i*nWait+[True]*nRead+[True]*nPola
		readSignal+=[False]*i*nWait+[2]*nRead+[False]*nPola
		x+=[i*dt]
	nAvg=ai.setupPulsed(freq=freq,signal=readSignal)
	do.setupPulsed(ValuesList=[readSignal,gateLaser],freq=freq,nAvg=nAvg)
	do.start()
	return x,nRead,val(nT1)
	
## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x,nRead,nT1):
	if do.done():
		data=ai.read()
		y=[]
		for i in range(nT1):
			segment=data[i*nRead:(i+1)*nRead]

			n=len(segment)
			n11=int(0.1*n)
			n12=int(0.3*n)
			n21=int(0.8*n)
			n22=n
			
			val=(sum(segment[n11:n12])-sum(segment[n21:n22]))
			y+=[val]

		gra.updateLine(l1,x,y) 

		nAvg=len(segment)//200
		segment=average(segment,nAvg=nAvg)
		xtRead=np.linspace(0,tRead.v,len(segment))
		gra.updateLine(l2,xtRead,segment)
		do.restart()

def extraStop() :
	do.setupContinuous([[False],[True]])

## Create the communication (I/O) instances ##
ai=AIChan()
ao=AOChan('ao0')
do=DOChan('p06','p07')
cube=PiezoCube3axes()

## Setup the Graphical interface ##
# laser=continuousLaserWidget(power=2E-4,spaceAbove=0)
laser=pulsedLaserWidget(gate=True,spaceAbove=0)
nT1=field('n points',100)
tT1=field('max time (s)',0.01)
tRead=field('read time (s)',0.01)
tPola=field('polarisation time (s)',0)
fields=[laser,nT1,tT1,tRead,tPola]

gra=graphics()
l1=gra.addLine(typ='average',style='m',fast=True)
ax2=gra.addAx()
l2=ax2.addLine(typ='average',style='m',fast=True)

channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)
StartStop=startStopButton(setup=setup,update=update,debug=True,serie=True,lineIter=l1,extraStop=extraStop)
StartStop.setupSerie(nAcqui=nLine,iterPerAcqui=100,acquiStart=acquiStart,acquiEnd=acquiEnd)
expfit=fitButton(line=l1,fit='exp',name='exp fit')
stretchfit=fitButton(line=l1,fit='stretch',name='stretch fit')
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(l1)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
buttons=[channels,norm,StartStop,trace,expfit,stretchfit,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='T1 CD')
# setup()
# visualize(ai,do)
GUI.run()

