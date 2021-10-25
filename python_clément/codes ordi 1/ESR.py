import sys
sys.path.append("C:\\Users\\Tom\\Documents\\GitHub\\these\\python_clément")
from lab import *

physicalChannels=['ctr0','ctr3','ai8']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	if AM.state():
		mod='AM'
	else :
		mod=False
	n=val(nPoints)
	f=val(fsweep)
	if channels.text()[:3]=='ctr' :
		acqui=ci
		mode='ctr'
	elif channels.text()[:2]=='ai' :
		acqui=ai
		mode='ai'
	mw.setupESR(F_min=fmin,F_max=fmax,Power=level,N_points=n,mod=mod,AM_Depth=AMDepth)

	trigAcqui=[2]*n
	acqui.setChannels(channels.text())
	acqui.setupWithPb(freq=f,signal=trigAcqui)
	
	trigMicrowave=[2]*n
	pb.setupPulsed(dt=1/f,ch1=trigAcqui,ch2=trigMicrowave,ch3=trigMicrowave,ch4=trigMicrowave)#temporaire, il faut trouver le bon cable

	x=np.linspace(val(fmin),val(fmax),n)
	return x,acqui,mode,n

## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x,acqui,mode,n):
	pb.start()
	y=acqui.read()
	print(acqui.sampsPerChan,acqui.nAvg,acqui.nRepeat)
	if mode=='ctr' :
		gra.updateLine(l1,x[:-1],y)
	elif mode=='ai' :
		gra.updateLine(l1,x,y)
	


def AM_OnOff():
	AMDepth.setEnabled(AM.state())

## Create the communication (I/O) instances ##
ai=AIChan()
ci=CIChan()
pb=pulseBlaster()
mw=microwave('mw1')
## Setup the Graphical interface ##
channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)

fmin=field('min freq (MHz)',2800,spaceAbove=3)
fmax=field('max freq (MHz)',2950,spaceAbove=0)
level=field('power (dBm)',0.)

AM=checkBox('Amplitude Modulation',action=AM_OnOff)
AMDepth=field('AM depth (%)',100,spaceAbove=0)
AM.setState(False)
AMDepth.setEnabled(AM.state())

nPoints=field('n points',150,spaceAbove=3)
fsweep=field('sweep frequency (Hz)',500,spaceAbove=0)

fields=[channels,fmin,fmax,level,AM,AMDepth,nPoints,fsweep]

gra=graphics(theme='black')
l1=gra.addLine(typ='average',style='lm')

StartStop=startStopButton(setup=setup,update=update,debug=True,lineIter=l1,showMaxIter=True)
save=saveButton(gra,autoSave=10)
trace=keepTraceButton(l1)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
fit=fitButton(line=l1,fit='ESR',name='fit ESR')
buttons=[norm,StartStop,trace,fit,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='ESR',theme='dark')
GUI.run()