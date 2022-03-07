from lab import *


def connectAction():
	platine.connect()
	for x in [currentPos,velocity,targetPos,disconnect] :
		x.setEnabled(True)
	connect.setEnabled(False)
	actualizePos()

def disconnectAction():
	platine.close()
	for x in [currentPos,velocity,targetPos,disconnect] :
		x.setEnabled(False)
	connect.setEnabled(True)

def moveAction():
	platine.setPos(targetPos,wait=True)
	# while not platine.pidevice.qONT(axes=1)[1] :
	#Il n'arrive pas à actualiser la position quand il est en mouvement visiblement
	actualizePos()

def setVelAction():
	platine.setVelocity(velocity)

def actualizePos():
	pos=platine.getPos()
	# print(pos['1'])
	currentPos.setText("Current pos : %.4f"%pos['1'])

platine=platinePI()

connect=button("Connect",action=connectAction)
disconnect=button("Disconnect",action=disconnectAction,spaceAbove=0,spaceBelow=1)

currentPos=label("Current pos : ?",style='big')
velocity=field('Velocity',0.6,action=setVelAction)
targetPos=field('Target pos',0,action=moveAction)

for x in [currentPos,velocity,targetPos,disconnect] :
	x.setEnabled(False)

GUI=Graphical_interface([connect,disconnect],[currentPos,velocity,targetPos],size='auto',title='Platine PI control')
GUI.run()