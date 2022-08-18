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
	fMaster=10/tWait
	nWait=int(fMaster*tWait)
	nLect=int(fMaster*tLect)
	nCycle=nWait+nLect
	nPoints=val(nPoints) 
	nTot=2*nPoints*nCycle #Attention : 2 fois plus de points pour faire le retour

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


	ai.setChannels(channel1.text(),channel2.text())

	
	
	nTot=len(voltageSignal)
	ao.setupTimed(SampleFrequency=fsweep,ValuesList=voltageSignal)
	ai.setupTimed(SampleFrequency=fsweep,SamplesPerChan=nTot,nAvg='auto')
	ao.triggedOn(ai)
	if abscissChoice.text()=='Voltage (V)' :
		x=voltageSignal[nstart:nend]
	elif abscissChoice.text()=='Time (s)' :
		x=np.linspace(0,n/fsweep,n)
	return(nstart,nend,x)


## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(nstart,nend,x):
	y=ai.readTimed(waitForAcqui=False)
	if not ai.running :
		y1=y[0][nstart:nend]
		y2=y[1][nstart:nend]
		gra.updateLine(l1,x,y1)
		gra.updateLine(l2,x,y2)


## Create the communication (I/O) instances ##
ai=AIChan()
ao=AOChan('ao0')
cube=PiezoCube3axes()

## Setup the Graphical interface ##
channel1=dropDownMenu('Channel for Fig.1 :',*physicalChannels,spaceAbove=0)
channel1.setIndex('ai11')
channel2=dropDownMenu('Channel for Fig.2 :',*physicalChannels,spaceAbove=0)
channel2.setIndex('ai13')
laser=pulsedLaserWidget()
vmin=field('V min (V)',-5,spaceAbove=3)
vmax=field('V max (V)',5,spaceAbove=0)
fieldSlope=dropDownMenu('Field Slope','Increasing','Decreasing',spaceAbove=0)
tWait=field('t wait (s)',1e-3,spaceAbove=3)
tLect=field('t lect (s)',1e-3,spaceAbove=0)
nPoints=field('n points',501,spaceAbove=3)
abscissChoice=dropDownMenu('Absciss','Voltage (V)','Time (s)',spaceAbove=0)
fields=[channel1,channel2,laser,vmin,vmax,fieldSlope,tWait,tLect,nPoints,abscissChoice]

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
GUI=Graphical_interface(fields,gra,buttons,title='Scan EM')
GUI.run()