from lab import *

physicalChannels=['ai13','ai11','ai9']

## setup() is executed once at the beginning of each loop (when start is pressed) ##
def setup(): 
	ai.setChannels(channels.text()) 
	freq=10*fmax
	nPoints=int(freq/fmin)
	# ns=np.arange(1,int(fmax/fmin)+1)
	# freqs=[i*fmin for i in ns] #faudrait plutot que je fasse un truc en log. Mias c'est pas opti non plus
	freqs=np.geomspace(val(fmin),val(fmax),val(nFreqs))
	ns=[int(freq/f) for f in freqs]
	ts=np.linspace(0,nPoints/freq,nPoints)
	ai.setupTimed(SampleFrequency=freq,SamplesPerChan=nPoints,nAvg='auto',SampleMode='finite') 
	return freqs,ns,ts
## update() is executed for each iteration of the loop (until stop is pressed) ##
def update(freqs,ns,ts):
	y=ai.readTimed(waitForAcqui=False) #read the number of samples required in SamplesPerChan ; with waitForAcqui=True the program wil freeze until the acquisition is complete (more stable)
	if not ai.running :
		# gra.updateLine(l1,ts,y) #meme en fast c'est hyper lent, faut que je règle ca
		sigmas=[]
		for n in ns :
			nSeg=len(y)//n
			sigma=0
			for i in range(nSeg):
				s=analyse.sigma(y[i*n:(i+1)*n])
				sigma+=s
			sigma=sigma/nSeg
			sigmas+=[sigma]
		gra.updateLine(l2,freqs,sigmas)

## Create the communication (I/O) instances ##
ai=AIChan()
## Setup the Graphical interface ##
fmin=field('f min (Hz)',1)
fmax=field('f max (Hz)',1e3)
nFreqs=field('n freqs (Hz)',100)
fields=[fmin,fmax]

gra=graphics()
l1=gra.addLine(typ='instant',style='l',fast=True)
ax2=gra.addAx()
l2=ax2.addLine(typ='average',style='lm')

channels=dropDownMenu('Channel to read :',*physicalChannels,spaceAbove=0)
StartStop=startStopButton(setup=setup,update=update,debug=True)
save=saveButton(gra,autoSave=False)
trace=keepTraceButton(l2)
it=iterationWidget(l2)
norm=gra.normalize()
norm.setState(False)
buttons=[channels,norm,StartStop,trace,save,it]

## Create the graphical interface and launch the program ##
GUI=Graphical_interface(fields,gra,buttons,title='Noise LF')
GUI.run()
