from lab import *

physicalChannels=['ai11','ai13']

## setup() is executed once at the beginning of each loop (when start is pressed) ##

# nSide=30
# zs=np.linspace(-5,5,nSide)
# ys=np.linspace(0,10,nSide)

nLine=101
Voltages=np.linspace(-3,3,nLine)
# positions=np.linspace(4,8,nLine)

def acquiSetup():
	BaseFolder=str(QFileDialog.getExistingDirectory(GUI, "Choose Directory",defaultDataPath))
	global ESRFolder
	ESRFolder=BaseFolder+'\\ESR\\'	
	# platine.connect()


def acquiStart(i):
	v=Voltages[i]
	ao.setupContinuous(v)

	# pos=positions[i]
	# platine.setPos(pos,wait=True)

	# iz=i%nSide
	# iy=i//nSide
	# zV=zs[iz]
	# yV=ys[iy]
	# cube.move(zV,ax='z')	
	# cube.move(yV,ax='y')



def acquiEnd(i):
	# iz=i%nSide
	# iy=i//nSide
	# zV=zs[iz]
	# yV=ys[iy]
	# fname=StartStop.defaultFolder+'z=%f,y=%f'%(zV,yV)

	fname=ESRFolder+'V=%f'%(Voltages[i])
	if i==0 :
		save.save(fname=fname,saveFigure=True)
	else :
		save.save(fname=fname,saveFigure=False)

def setup(): 
	n=val(nPoints)
	f=val(fsweep)

	ai.setChannels(channels.text())
	ai.setupTimed(SampleFrequency=f,SamplesPerChan=n,nAvg='auto')

	doSequence=[True,False]*n
	do.setupTimed(SampleFrequency=2*f,ValuesList=doSequence)
	do.triggedOn(ai)

	x=np.linspace(val(fmin),val(fmax),n)
	return x

## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x):
	y=ai.read(waitForAcqui=True)
	if not ai.running :
		gra.updateLine(l1,x,y)

def AM_OnOff():
	AMDepth.setEnabled(AM.state())
	if AM.state():
		FM.setState(False)

def FM_OnOff():
	FMDev.setEnabled(FM.state())
	if FM.state():
		AM.setState(False)

def switchAction():
	switchState=switchButton.state()
	switchDo=DOChan('p02')
	switchDo.setupContinuous(switchState,close=True)

def setupuWAction():
	setupuWButton.setEnabled(False)
	if AM.state():
		mod='AM'
	elif FM.state():
		mod='FM'
	else :
		mod=False
	mw.setupESR(F_min=fmin,F_max=fmax,Power=level,N_points=nPoints,mod=mod,AM_Depth=AMDepth,FM_Dev=FMDev)
	mw.toBeClosed=False
	resetuWButton.setEnabled(True)

def resetuWAction():
	resetuWButton.setEnabled(False)
	mw.close()
	setupuWButton.setEnabled(True)
## Create the communication (I/O) instances ##
ai=AIChan()
do=DOChan('p01')
ao=AOChan('ao0')
mw=microwave('mw_ludo')
cube=PiezoCube3axes()
platine=platinePI()

## Setup the Graphical interface ##
channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)

fmin=field('min freq (MHz)',2850,spaceAbove=3)
fmax=field('max freq (MHz)',2890,spaceAbove=0)
level=field('power (dBm)',-5)

AM=checkBox('Amplitude Modulation',action=AM_OnOff)
AMDepth=field('AM depth (%)',100,spaceAbove=0)
FM=checkBox('Frequency Modulation',action=FM_OnOff)
FMDev=field('FM deviation (Hz)',1E6,spaceAbove=0)

setupuWButton=button('Setup µW',action=setupuWAction)
resetuWButton=button('Reset µW',action=resetuWAction,spaceAbove=0)
resetuWButton.setEnabled(False)

AM.setState(True)
AMDepth.setEnabled(AM.state())
FM.setState(False)
FMDev.setEnabled(FM.state())


switchButton=checkBox('Switch On',action=switchAction)

nPoints=field('n points',501,spaceAbove=3)
fsweep=field('sweep frequency (Hz)',100,spaceAbove=0)

fields=[channels,fmin,fmax,level,AM,AMDepth,FM,FMDev,setupuWButton,resetuWButton,switchButton,nPoints,fsweep]

gra=graphics()
l1=gra.addLine(typ='average',style='lm')

StartStop=startStopButton(setup=setup,update=update,debug=True,serie=True,lineIter=l1,showMaxIter=True)
StartStop.setupSerie(nAcqui=nLine,iterPerAcqui=2,acquiSetup=acquiSetup,acquiStart=acquiStart,acquiEnd=acquiEnd)
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(l1)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
fit=fitButton(line=l1,fit='ESR',name='fit ESR')
buttons=[norm,StartStop,trace,fit,save,it]

def ESRInLine(Fmin,Fmax,Power,NPoints,NRuns,Fsweep=300,AmpMod=True):
	if AmpMod :
		AM.setState(True)
	fmin.setValue(Fmin)
	fmax.setValue(Fmax)
	level.setValue(Power)
	nPoints.setValue(NPoints)
	fsweep.setValue(Fsweep)
	AM.setState(AmpMod)
	if AmpMod :
		channels.setIndex('ai11')
	else :
		channels.setIndex('ai13')
	switchDo=DOChan('p02')
	switchDo.setupContinuous(True,close=True)
	gateLaser=DOChan('p07')
	gateLaser.setupContinuous(True,close=True)
	l1.reset()
	x=setup()
	while l1.iteration < NRuns+1 :
		update(x)
	ai.close()
	do.close()
	mw.close()
	switchDo.setupContinuous(False,close=True)
	x=l1.x
	y=l1.trueY
	return (x,y)

## Create the graphical interface and launch the program ##
if __name__ == "__main__":
	GUI=Graphical_interface(fields,gra,buttons,title='ESR no-rst')
	GUI.run()