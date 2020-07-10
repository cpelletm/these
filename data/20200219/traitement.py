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

def gauss_fit(x,y,Amp=None,x0=None,sigma=None) :
	if not Amp :
		Amp=max(y)
	if not x0 :
		x0=x[int(len(x)/2)]
	if not sigma :
		sigma=x[int(len(x)/10)]-x[0]

	def f(x,Amp,x0,sigma) :
		return Amp*np.exp(-((x-x0)/(2*sigma))**2)
	p0=[Amp,x0,sigma]
	popt, pcov = curve_fit(f, x, y, p0)
	return(x for x in popt)

def lor_fit(x,y,Amp=None,x0=None,sigma=None) :
	if not Amp :
		Amp=max(y)
	if not x0 :
		x0=x[int(len(x)/2)]
	if not sigma :
		sigma=x[int(len(x)/10)]-x[0]
	print(Amp,x0,sigma)
	def f(x,Amp,x0,sigma) :
		return Amp*1/(1+((x-x0)/(2*sigma))**2)
	p0=[Amp,x0,sigma]
	popt, pcov = curve_fit(f, x, y, p0)
	return(x for x in popt)

def ask_name():
	qapp = QApplication(sys.argv)
	fname,filters=QFileDialog.getOpenFileName()	
	return fname



def interp_linr() :
	x,y=extract_data('sumi_4_scan_R_zoom.txt')
	x=x[50:176]*43-28.4 #Les coefs sont extraits de conversion_V_NRJ (normalement b=-26.3 mais bon)
	y=y[50:176]
	droite=(y[125]-y[0])*(x-x[0])/(x[125]-x[0])+y[0]
	y=-y+droite
	plt.plot(x,y,label='experimental data')
	Amp,x0,sigma=gauss_fit(x,y)
	def f(x,Amp,x0,sigma) :
		return Amp*np.exp(-((x-x0)/(2*sigma))**2)
	plt.plot(x,f(x,Amp,x0,sigma),label='HWHM=%f'%(sigma*np.log(4)))
	plt.xlabel('delta(E) (MHz)')

interp_linr()

plt.legend()

plt.show()