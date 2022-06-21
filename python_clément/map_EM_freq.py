from lab import *

physicalChannels=['ai11','ai13']

def setup():
	ai.setChannels(channels.text())
	ai.setupTimed(SampleFrequency=1/dt,SamplesPerChan=1,nAvg='auto')
	v0=ai.read(waitForAcqui=True)[0]
	initialData=np.ones((val(nx),val(ny)))*v0
	m.setSize(initialData)
	m.setLim(xi,xf,yi,yf)
	cube.move(xi,'x')
	cube.move(yi,'y')
	xs=np.linspace(val(xi),val(xf),val(nx))
	ys=np.linspace(val(yi),val(yf),val(ny))
	# ai.setupTimed(SampleFrequency=10,SamplesPerChan=1)
	return(xs,ys)

def update(xs,ys):
	y=ai.read()
	if not ai.running :
		m.updateMap(y[0])
		i,j=m.xindex,m.yindex
		cube.move(xs[i],ax='x',close=False)
		cube.move(ys[j],ax='y',close=False)


## Create the communication (I/O) instances ##
cube=PiezoCube3axes()
ai=AIChan()

## Setup the Graphical interface ##
channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)

xi=field('x initial (V)',0,spaceAbove=3)
xf=field('x final (V)',10,spaceAbove=0)
nx=field('number of step x',11,spaceAbove=0)

yi=field('y initial (V)',0,spaceAbove=1)
yf=field('y final (V)',10,spaceAbove=0)
ny=field('number of step y',11,spaceAbove=0,spaceBelow=3)

dt=field('time per pixel (s)',0.2)
fields=[channels,xi,xf,nx,yi,yf,ny,dt]

gra=graphics()
m=gra.addMap(xsize=10,ysize=10,typ='average')

StartStop=startStopButton(setup=setup,update=update,debug=True,lineIter=m,showMaxIter=True)
save=saveButton(gra,autoSave=False)
it=iterationWidget(m)
buttons=[StartStop,save,it]

GUI=Graphical_interface(fields,gra,buttons,title='Piezo Map')
GUI.run()