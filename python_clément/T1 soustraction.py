from lab import *
from ESR import ESRInLine
from analyse import find_ESR_peaks,find_elem

physicalChannels=['ai13','ai11','ai9']

nLine=121
# vs=np.linspace(0.8,5,nLine)
positions=np.linspace(4,8,nLine)

def acquiSetup():
	BaseFolder=str(QFileDialog.getExistingDirectory(GUI, "Choose Directory",defaultDataPath))
	global T1Folder,ESRFolder
	ESRFolder=BaseFolder+'\\ESR\\'	
	T1Folder=BaseFolder+'\\T1\\'
	platine.connect()

def acquiStart(i):
	
	# v=vs[i]
	# ao.setupContinuous(v)
	pos=positions[i]
	platine.setPos(pos,wait=True)

	x,y=ESRInLine(Fmin=2680,Fmax=2850,Power=0,NPoints=501,NRuns=3,Fsweep=100,AmpMod=True)
	save_data(x,y,dirname=ESRFolder,fname="x=%f"%pos)
	i=find_elem(max(y),y)
	freq=x[i]
	frequW.setValue(freq)
	# print(freq) #ca fait planter en background mais ça assure qu'il fasse pas trop de conneries


def acquiEnd(i):
	# fname=T1Folder+'V=%f'%(vs[i])
	fname=T1Folder+'x=%f'%(positions[i])


	if i==0 :
		save.save(fname=fname,saveFigure=True)
	else :
		save.save(fname=fname,saveFigure=False)

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
	for i in range(1,nT1+1): #Je fais 4 sequences : sans pulse, avec pulse; avec pulse, sans pulse. La différence avec 2 séquences c'est que ça devrait limiter l'effet des drifts (si ils sont linéaires)
		gateLaser+=([True]*nPola+[False]*i+[True]*nRead)*4
		readSignal+=([False]*(i+nPola)+[2]*nRead)*4
		if zeromoinsunCB.state() : #mesure du T1 du -1 (ou+1) : pulse au début du dark time puis soustraction
			switchSignal+=([False]*(nPola-1)+[True]+[False]*(i+nRead))   +   ([False]*(nPola-1)+[True]+[False]*(i-1)+[True]+[False]*(nRead)) \
			+([False]*(nPola-1)+[True]+[False]*(i-1)+[True]+[False]*(nRead))   +   ([False]*(nPola-1)+[True]+[False]*(i+nRead))
		else : #mesure du T1 du zero
			switchSignal+=([False]*(nPola+i+nRead))   +   ([False]*(nPola+i-1)+[True]+[False]*nRead) \
			+([False]*(nPola+i-1)+[True]+[False]*nRead)   +   ([False]*(nPola+i+nRead))
		x+=[i*dt]
	nAvg=ai.setupPulsed(freq=freq,signal=readSignal,nRepeat=nRep)
	do.setupPulsed(ValuesList=[readSignal,gateLaser,switchSignal],freq=freq,nAvg=nAvg,nRepeat=nRep)
	do.start()
	return x,nRead,val(nT1)
	
## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x,nRead,nT1):
	if do.done():
		data=ai.read(waitForAcqui=True)
		y1=[]
		y2=[]
		for i in range(nT1):
			segment1=data[4*i*nRead:(4*i+1)*nRead]
			segment2=data[(4*i+1)*nRead:(4*i+2)*nRead]
			segment3=data[(4*i+2)*nRead:(4*i+3)*nRead]
			segment4=data[(4*i+3)*nRead:(4*i+4)*nRead]
			y1+=[sum(segment1)/len(segment1)+sum(segment4)/len(segment4)]		
			y2+=[sum(segment2)/len(segment2)+sum(segment3)/len(segment3)]
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
cube=PiezoCube3axes()
platine=platinePI()


## Setup the Graphical interface ##
# laser=continuousLaserWidget(power=2E-4,spaceAbove=0)
laser=pulsedLaserWidget(gate=True,spaceAbove=0)
frequW=field('uW frequency (MHz)',2866)
poweruW=field('uW power (dBm)',15,spaceAbove=0)
nT1=field('n points',200)
tT1=field('max time (s)',4e-3,spaceAbove=0)
tRead=field('read time (s)',1e-3,spaceAbove=0)
tPola=field('polarisation time (s)',0,spaceAbove=0)
nRep=field('n repeat',1)
fields=[laser,frequW,poweruW,nT1,tT1,tRead,tPola,nRep]

gra=graphics(refreshRate=0.1)
l1=gra.addLine(typ='average',style='m',fast=True)
l2=gra.addLine(typ='average',style='m',fast=True)
ax2=gra.addAx()
l3=gra.addLine(typ='average',style='m',fast=True,ax=ax2)
# ax3=gra.addAx()
# l4=ax3.addLine(typ='instant',style='m',fast=True)

channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)
zeromoinsunCB=checkBox('ms=-1(check)\nms=0(uncheck)')
StartStop=startStopButton(setup=setup,update=update,debug=True,serie=True,lineIter=l1,extraStop=extraStop)
StartStop.setupSerie(nAcqui=nLine,iterPerAcqui=75,startingIter=0,acquiSetup=acquiSetup,acquiStart=acquiStart,acquiEnd=acquiEnd)
expfit=fitButton(line=l3,fit='expZero',name='exp fit')
stretchfit=fitButton(line=l3,fit='stretchZero',name='stretch fit')
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(l1,l2,l3)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
buttons=[channels,norm,zeromoinsunCB,StartStop,trace,expfit,stretchfit,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='T1 soustraction')
# setup()
# visualize(ai,do)
GUI.run()

