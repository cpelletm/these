from lab import *

physicalChannels=['ai13','ai11','ai9']
nSide=30
xs=np.linspace(0,10,nSide)
ys=np.linspace(0,10,nSide)

# nLine=30
# ys=np.linspace(0,10,nLine)

def acquiStart(i):
	ix=i%nSide
	iy=i//nSide
	xV=xs[ix]
	yV=ys[iy]
	cube.move(xV,ax='x')	
	cube.move(yV,ax='y')

	# yV=ys[i]
	# cube.move(yV,ax='y')

def acquiEnd(i):
	ix=i%nSide
	iy=i//nSide
	xV=xs[ix]
	yV=ys[iy]
	fname=StartStop.defaultFolder+'x=%f,y=%f'%(xV,yV)

	# yV=ys[i]
	# fname=StartStop.defaultFolder+'x=0,y=%f'%(yV)
	if i==0 :
		save.save(fname=fname,saveFigure=True)
	else :
		save.save(fname=fname,saveFigure=False)
	

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	# fMaster=lcm(int(1/tWait),int(1/tLect)) #C'est rigolo mais je suis sur que c'est débile
	ai.setChannels(channel1.text())
	fMaster=ai.getMaxFreq()
	nWait=int(fMaster*tWait)
	nLect=int(fMaster*tLect)
	nCycle=nWait+nLect
	nPoints=val(nPointsWidg) 
	nTot=2*nPoints*nCycle #Attention : 2 fois plus de points pour faire le retour

	
	readSignal=([False]*nWait+[2]*nLect)*nPoints+[False]*nCycle*nPoints
	ai.setupPulsed(freq=fMaster,signal=readSignal,nRepeat=1,nAvg=1)
	gateLaser=([False]*nWait+[True]*nLect)*nPoints*2
	do.setupPulsed(ValuesList=[readSignal,gateLaser],freq=fMaster,nAvg=1,nRepeat=1)


	xmin=val(vmin)
	xmax=val(vmax)
	Vvalues=np.linspace(xmin,xmax,nPoints)
	voltageSignal=[]
	if fieldSlope.text()=='Decreasing' :
		for i in range(nPoints):
			voltageSignal+=[Vvalues[-(i+1)]]*nCycle
		for i in range(nPoints):
			voltageSignal+=[Vvalues[i]]*nCycle
	elif fieldSlope.text()=='Increasing' :
		for i in range(nPoints):
			voltageSignal+=[Vvalues[i]]*nCycle
		for i in range(nPoints):
			voltageSignal+=[Vvalues[-(i+1)]]*nCycle

	assert len(voltageSignal)==len(readSignal)
	ao.setupTimed(SampleFrequency=fMaster,ValuesList=voltageSignal)
	ao.triggedOn(do)
	if abscissChoice.text()=='Voltage (V)' :
		x=Vvalues
	elif abscissChoice.text()=='Time (s)' :
		x=np.linspace(0,n/fsweep,n)
	do.start()
	return(nLect,nPoints,x)


## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(nLect,nPoints,x):
	if do.done():
		data=ai.read(waitForAcqui=True)
		assert len(data)==nLect*nPoints
		y1=np.zeros(nPoints)
		y2=np.zeros(nPoints)
		for i in range(nPoints):
			y1[i]=sum(data[i*nLect:int((i+0.5)*nLect)])/sum(data[int((i+0.5)*nLect):(i+1)*nLect])
			y2[i]=sum(data[int((i+0.5)*nLect):(i+1)*nLect])/nLect
		gra.updateLine(l1,x,y1,noRefresh=True)
		gra.updateLine(l2,x,y2,noRefresh=False)
		do.restart()


## Create the communication (I/O) instances ##
ai=AIChan()
ao=AOChan('ao0')
do=DOChan('p06','p07')
cube=PiezoCube3axes()

## Setup the Graphical interface ##
channel1=dropDownMenu('Channel for ai :',*physicalChannels,spaceAbove=0)
channel1.setIndex('ai13')
laser=pulsedLaserWidget()
vmin=field('V min (V)',-5,spaceAbove=3)
vmax=field('V max (V)',5,spaceAbove=0)
fieldSlope=dropDownMenu('Field Slope','Increasing','Decreasing',spaceAbove=0)
tWait=field('t wait (s)',1e-3,spaceAbove=3)
tLect=field('t lect (s)',2e-3,spaceAbove=0)
nPointsWidg=field('n points',501,spaceAbove=3)
abscissChoice=dropDownMenu('Absciss','Voltage (V)','Time (s)',spaceAbove=0)
fields=[channel1,laser,vmin,vmax,fieldSlope,tWait,tLect,nPointsWidg,abscissChoice]

gra=graphics()
l1=gra.addLine(typ='average',style='lm')
ax2=gra.addAx()
l2=gra.addLine(typ='average',style='lm',ax=ax2)

StartStop=startStopButton(setup=setup,update=update,debug=True,serie=True,lineIter=l1,extraStop=lambda: ao.setTo(0))
StartStop.setupSerie(nAcqui=nSide**2,iterPerAcqui=10,acquiStart=acquiStart,acquiEnd=acquiEnd)
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(l1,l2)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
buttons=[norm,StartStop,trace,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='Scan EM Pulsed')
GUI.run()