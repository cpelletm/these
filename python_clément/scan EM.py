from lab import *


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
	n=val(nPoints)
	xmin=val(vmin)
	xmax=val(vmax)
	xmed=xmin+xmax/2
	nstart=n//2
	nend=nstart+n
	voltageSignal=np.concatenate((np.linspace(xmed,xmin,nstart),np.linspace(xmin,xmax,n),np.linspace(xmax,xmed,nstart)))
	nTot=len(voltageSignal)
	ao.setupTimed(SampleFrequency=fsweep,ValuesList=voltageSignal)
	ai.setupTimed(SampleFrequency=fsweep,SamplesPerChan=nTot,nAvg='auto')
	ao.triggedOn(ai)
	x=voltageSignal[nstart:nend]
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
ai=AIChan('ai11','ai13')
ao=AOChan('ao0')
cube=PiezoCube3axes()

## Setup the Graphical interface ##

laser=pulsedLaserWidget()
vmin=field('V min (V)',-5,spaceAbove=3)
vmax=field('V max (V)',5,spaceAbove=0)
nPoints=field('n points',501,spaceAbove=3)
fsweep=field('sweep frequency (Hz)',200,spaceAbove=0)

fields=[laser,vmin,vmax,nPoints,fsweep]

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