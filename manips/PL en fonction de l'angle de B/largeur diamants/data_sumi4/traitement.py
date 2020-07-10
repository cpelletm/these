import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from PyQt5.QtWidgets import QApplication,QFileDialog




def extract_data(filename,xcol=0,ycol=1):
	x=[]
	y=[]
	with open(filename,'r',encoding = "ISO-8859-1") as f:
		for line in f :
			line=line.split()
			try :
				x+=[float(line[xcol])]
				y+=[float(line[ycol])]
			except :
				pass
	return(np.array(x),np.array(y))

def lin_fit(x,y) :
	A=np.vstack([x,np.ones(len(x))]).T
	a,b = np.linalg.lstsq(A, y, rcond=None)[0]
	return(a,b)

def gauss_fit(x,y,Amp,x0,sigma) :
	def f(x,Amp,x0,sigma) :
		return Amp*np.exp(-((x-x0)/(2*sigma))**2)
	p0=[Amp,x0,sigma]
	popt, pcov = curve_fit(f, x, y, p0)
	return(x for x in popt)

def lor_fit(x,y,Amp,x0,sigma) :
	def f(x,Amp,x0,sigma) :
		return Amp*1/(1+((x-x0)/(2*sigma))**2)
	p0=[Amp,x0,sigma]
	popt, pcov = curve_fit(f, x, y, p0)
	return(x for x in popt)

def ask_name():
	qapp = QApplication(sys.argv)
	fname,filters=QFileDialog.getOpenFileName()	
	return fname


fname='ESR_sumi4_5-00V_80mA.txt'

x,y=extract_data(fname)
y=y/max(y)

plt.plot(x*1000,y,label='data')
x,y=extract_data('ESR_5V_simu.txt')
plt.plot(x,y,label='simu')


plt.legend()

plt.show()