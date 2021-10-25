from lab import *
from ESR import ESRInLine
from analyse import find_ESR_peaks

physicalChannels=['ai13','ai11','ai9']

Voltages=np.linspace(-2,2,130)
def acquiStart(i):
	v=Voltages[i]
	ao.setupContinuous(v)
	x,y=ESRInLine(Fmin=2400,Fmax=3200,Power=10,NPoints=1001,NRuns=3,Fsweep=400,AmpMod=True)
	gra.updateLine(l4,x,y)
	cs=find_ESR_peaks(x,y)
	print(min(cs)) #ca fait planter en background mais ça assure qu'il fasse pas trop de conneries
	frequW.setValue(min(cs))


def acquiEnd(i):
	fname=StartStop.defaultFolder+'V=%f'%(Voltages[i])+' V'
	save.save(fname=fname)

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	mw.setupContinuous(Frequency=frequW,Power=poweruW)
	apply_repeat(nRep,ai,do,l1,l2,l3)
	ai.setChannels(channels.text()) 
	freq=nT1/tT1
	dt=1/freq
	nPola=int(freq*tPola)
	nRead=int(freq*tRead)
	gateLaser=[True]*nPola
	readSignal=[False]*nPola
	switchSignal=[False]*nPola
	x=[]
	for i in range(1,nT1+1):
		gateLaser+=([False]*i+[True]*nPola)*2
		readSignal+=([False]*i+[True]*nRead+[False]*(nPola-nRead))*2
		if debutfin.state() : #pulse au début du dark time
			switchSignal+=([False]*(nPola+i))+([True]+[False]*(nPola+i-1))
		else : #pulse à la fin du dark time 
			switchSignal+=([False]*i+[False]*nPola)+([False]*(i-1)+[True]+[False]*nPola)
		x+=[i*dt]
	pulseRead=ai.setupPulsed(freq=freq,signal=readSignal)
	do.setupTimed(SampleFrequency=freq,ValuesList=[pulseRead,gateLaser,switchSignal])
	do.start()
	return x,nRead,val(nT1)
	
## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x,nRead,nT1):
	if True:
		data=ai.read()
		y1=[]
		y2=[]
		for i in range(nT1):
			segment1=data[2*i*nRead:(2*i+1)*nRead]
			y1+=[sum(segment1)/len(segment1)]
			segment2=data[(2*i+1)*nRead:(2*i+2)*nRead]
			y2+=[sum(segment2)/len(segment2)]
		y1=np.array(y1)
		y2=np.array(y2)
		gra.updateLine(l1,x,y1,noRefresh=True) 
		gra.updateLine(l2,x,y2,noRefresh=True) 
		gra.updateLine(l3,x,y1-y2,noRefresh=False) 
		do.restart()

def extraStop() :
	do.setupContinuous([[False],[True],[True]])

## Create the communication (I/O) instances ##
ai=AIChan()
ao=AOChan('ao0')
do=DOChan('p06','p07','p02')
mw=microwave('mw_ludo')

## Setup the Graphical interface ##
# laser=continuousLaserWidget(power=2E-4,spaceAbove=0)
laser=pulsedLaserWidget(gate=True,spaceAbove=0)
frequW=field('uW frequency (MHz)',2866)
poweruW=field('uW power (dBm)',10,spaceAbove=0)
nT1=field('n points',200)
tT1=field('max time (s)',2e-3,spaceAbove=0)
tRead=field('read time (s)',2e-4,spaceAbove=0)
tPola=field('polarisation time (s)',1e-3,spaceAbove=0)
nRep=field('n repeat',1)
fields=[laser,frequW,poweruW,nT1,tT1,tRead,tPola,nRep]

gra=graphics(refreshRate=0.1)
l1=gra.addLine(typ='average',style='m',fast=True)
l2=gra.addLine(typ='average',style='m',fast=True)
ax2=gra.addAx()
l3=ax2.addLine(typ='average',style='m',fast=True)
# ax3=gra.addAx()
# l4=ax3.addLine(typ='instant',style='m',fast=True)

channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)
debutfin=checkBox('debut(check)\nfin(uncheck)')
StartStop=startStopButton(setup=setup,update=update,debug=True,serie=True,lineIter=l1,extraStop=extraStop)
StartStop.setupSerie(nAcqui=len(Voltages),iterPerAcqui=200,acquiStart=acquiStart,acquiEnd=acquiEnd)
expfit=fitButton(line=l3,fit='expZero',name='exp fit')
stretchfit=fitButton(line=l3,fit='stretchZero',name='stretch fit')
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(l1,l2,l3)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
buttons=[channels,debutfin,norm,StartStop,trace,expfit,stretchfit,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='T1 soustraction')
# setup()
# visualize(ai,do)
GUI.run()

