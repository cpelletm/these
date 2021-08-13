from lab import *

def setup():
	ai.setChannels('ai11')
	ai.setupTimed(SampleFrequency=1000/val(dt),SamplesPerChan=2,nAvg=nAvg,sampleMode='finite')
	if l1.yData[-1]==0 :
		y0=ai.readTimed(waitForAcqui=True)[0]
		x=np.linspace(0,val(dt)*val(nPoints),val(nPoints))
		y=np.ones(val(nPoints))*y0
		gra.updateLine(l1,x,y)

def update():
	y=failSafe(ai.readTimed,False,debug=False)
	gra.updateLine(l1,False,y)
	if np.any(y) :
		PL.setText('%3.2E'%y[0])
	it.increase() #à modifier ....

ai=AIChan()

nPoints=field('n points',151,spaceAbove=3)
nAvg=field('Average over :',10,spaceAbove=1)
dt=field('dt (ms)',30,spaceAbove=1,spaceBelow=3)
PL=label('Off',style='BIG',spaceAbove=0)
fields=[PL,nPoints,nAvg,dt]

gra=graphics()
l1=gra.addLine(typ='scroll',style='lm')

StartStop=startStopButton(setup=setup,update=update,debug=False)
save=saveButton(gra,autoSave=10)
trace=keepTraceButton(gra,l1)
it=gra.iteration()
norm=gra.normalize()
norm.setState(False)

buttons=[norm,StartStop,trace,save,it]
GUI=Graphical_interface(fields,gra,buttons,title='Oscillo')
GUI.run()
