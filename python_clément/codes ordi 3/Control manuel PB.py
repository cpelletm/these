import sys
sys.path.append("D:\\these\\python_clément")
sys.path.append('D:\\These Clément\\these\\python_clément')
from lab import *


def ch1OnAction():
	ch1OnButton.setEnabled(False)
	ch1OffButton.setEnabled(True)
	pbState[0]=1
	loadPb()

def ch1OffAction():
	ch1OnButton.setEnabled(True)
	ch1OffButton.setEnabled(False)
	pbState[0]=0
	loadPb()

def ch2OnAction():
	ch2OnButton.setEnabled(False)
	ch2OffButton.setEnabled(True)
	pbState[1]=1
	loadPb()
def ch2OffAction():
	ch2OnButton.setEnabled(True)
	ch2OffButton.setEnabled(False)
	pbState[1]=0
	loadPb()

def ch3OnAction():
	ch3OnButton.setEnabled(False)
	ch3OffButton.setEnabled(True)
	pbState[2]=1
	loadPb()
def ch3OffAction():
	ch3OnButton.setEnabled(True)
	ch3OffButton.setEnabled(False)
	pbState[2]=0
	loadPb()

def ch4OnAction():
	ch4OnButton.setEnabled(False)
	ch4OffButton.setEnabled(True)
	pbState[3]=1
	loadPb()
def ch4OffAction():
	ch4OnButton.setEnabled(True)
	ch4OffButton.setEnabled(False)
	pbState[3]=0
	loadPb()


def loadPb():
	pb.contInst(*pbState)
	pb.load()
	pb.start()

pb=pulseBlasterInterpreter()

pbState=[0,0,0,0]

ch1OnButton=button('Ch1 ON',ch1OnAction)
ch1OffButton=button('Ch1 OFF',ch1OffAction)
ch1OffButton.setEnabled(False)

ch2OnButton=button('Ch2 ON',ch2OnAction)
ch2OffButton=button('Ch2 OFF',ch2OffAction)
ch2OffButton.setEnabled(False)

ch3OnButton=button('Ch3 ON',ch3OnAction)
ch3OffButton=button('Ch3 OFF',ch3OffAction)
ch3OffButton.setEnabled(False)

ch4OnButton=button('Ch4 ON',ch4OnAction)
ch4OffButton=button('Ch4 OFF',ch4OffAction)
ch4OffButton.setEnabled(False)

GUI=Graphical_interface([ch1OnButton,ch1OffButton],[ch2OnButton,ch2OffButton],[ch3OnButton,ch3OffButton],[ch4OnButton,ch4OffButton],size='auto',title='PB manual')
GUI.run()