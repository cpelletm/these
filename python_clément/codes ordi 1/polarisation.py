import sys
sys.path.append("C:\\Users\\Tom\\Documents\\GitHub\\these\\python_clément")
from lab import *

physicalChannels=['ctr0','ctr3','ai8']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	if channels.text()[:3]=='ctr' :
		acqui=ci
		mode='ctr'
	elif channels.text()[:2]=='ai' :
		acqui=ai
		mode='ai'

	nRead=val(NRead)
	freq=nRead/val(tRead)
	nWait=int(freq*val(tWait))
	totalTime=val(tWait)+val(tRead)

	if fullView.state() :
		x=np.linspace(0,totalTime,(nWait+nRead))
		trigAcqui=[2]*(nWait+nRead)
	else :
		x=np.linspace(0,val(tRead),nRead)
		trigAcqui=[0]*nWait+[2]*nRead
		
	acqui.setChannels(channels.text())
	acqui.setupWithPb(freq=freq,signal=trigAcqui)

	
	trigMicrowave=[0]*nWait+[1]*nRead
	pb.setupPulsed(dt=1/freq,ch1=trigAcqui,ch2=trigMicrowave,ch3=trigMicrowave,ch4=trigMicrowave)#temporaire, il faut trouver le bon cable

	return x,acqui,mode

## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(x,acqui,mode):
	pb.start()
	y=acqui.read()
	if mode=='ctr' :
		gra.updateLine(l1,x[:-1],y)
	elif mode=='ai' :
		gra.updateLine(l1,x,y)
	


def mw_OnOff():
	mw.setupContinuous(Frequency=mwFreq,Power=mwLvl)

def switch_OnOff():
	if switchOn.state() :
		pb.setupContinuous(ch1=0,ch2=1,ch3=1,ch4=1)

	else :
		pb.setupContinuous(ch1=0,ch2=0,ch3=0,ch4=0)

## Create the communication (I/O) instances ##
ai=AIChan()
ci=CIChan()
pb=pulseBlaster()
mw=microwave('mw1')
## Setup the Graphical interface ##
channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)


fullView=checkBox('Full View')
fullView.setState(True)
NRead=field('n read',200)
tWait=field('dark time (s)',1e-3)
tRead=field('read time (s)',1e-3)
mwFreq=field('microwave frequency (MHz)',2880)
mwLvl=field('microwave power (dBm)',15)
mwOn=checkBox('Microwave on/off',action=mw_OnOff)
switchOn=checkBox('Switch on/off',action=switch_OnOff)

fields=[channels,fullView,NRead,tWait,tRead,mwFreq,mwLvl,mwOn,switchOn]

gra=graphics(theme='black')
l1=gra.addLine(typ='average',style='lm')

StartStop=startStopButton(setup=setup,update=update,debug=False,lineIter=l1,showMaxIter=True)
save=saveButton(gra,autoSave=10)
trace=keepTraceButton(l1)
it=iterationWidget(l1)
norm=gra.normalize()
norm.setState(False)
fit=fitButton(line=l1,fit='ESR',name='fit ESR')
buttons=[norm,StartStop,trace,fit,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='Polarisation',theme='dark')
GUI.run()