from lab import *


def moveX():
	cube.move(fieldX,ax='x',close=True)

def moveY():
	cube.move(fieldY,ax='y',close=True)

def moveZ():
	cube.move(fieldZ,ax='z',close=True)

cube=PiezoCube3axes()

fieldX=field('x=',0,action=moveX)
fieldY=field('y=',0,action=moveY)
fieldZ=field('z=',0,action=moveZ)

GUI=Graphical_interface(fieldX,fieldY,fieldZ,title='Piezo Control',size='auto')
GUI.run()