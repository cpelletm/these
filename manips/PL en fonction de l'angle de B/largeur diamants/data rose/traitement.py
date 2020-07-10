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
	return(a,b,a*x+b)

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
	return(popt,f(x,popt[0],popt[1],popt[2]))

def lor_fit(x,y,Amp=None,x0=None,sigma=None,origin=None) :
	if not Amp :
		Amp=max(y)
	if not x0 :
		x0=x[int(len(x)/2)]
	if not sigma :
		sigma=x[int(len(x)/10)]-x[0]
	if not origin :
		origin=y[0]
	def f(x,Amp,x0,sigma,origin) :
		return Amp*1/(1+((x-x0)/(sigma))**2)+origin
	p0=[Amp,x0,sigma,origin]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1],popt[2],popt[3]))

def exp_fit(x,y,Amp=None,ss=None,tau=None) :
	if not Amp :
		Amp=max(y)-min(y)
	if not ss :
		ss=y[-1]
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,Amp,ss,tau) :
		return Amp*np.exp(-x/tau)+ss
	p0=[Amp,ss,tau]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1],popt[2]))

def stretch_exp_fit(x,y,Amp=None,ss=None,tau=None) :
	if not Amp :
		Amp=max(y)-min(y)
	if not ss :
		ss=y[-1]
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,Amp,ss,tau) :
		return Amp*np.exp(-np.sqrt(x/tau))+ss
	p0=[Amp,ss,tau]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1],popt[2]))

def ask_name():
	qapp = QApplication(sys.argv)
	fname,filters=QFileDialog.getOpenFileName()	
	return fname






x,y1=extract_data('peaks.txt')
y2,y3=extract_data('peaks.txt',xcol=2,ycol=3)
x,y4=extract_data('peaks.txt',ycol=4)

def show_all():

	plt.plot(x,y1,label='y1(x)')
	plt.plot(x,y2,label='y2(x)')
	plt.plot(x,y3,label='y3(x)')
	plt.plot(x,y4,label='y4(x)')
def conversion() :
	plt.plot(x,y2-y1, label='data -')
	a,b,fit=lin_fit(x,y2-y1)
	plt.plot(x,fit,label='fit - %f'%a)
	plt.plot(x,y4-y3, label='data +')
	a,b,fit=lin_fit(x,y4-y3)
	plt.plot(x,fit,label='fit + %f'%a)

x,y=extract_data('scan_transition_correspond_ESR.txt')

x=x*28 #conversion MHz
up=136
down=179
x=x[up:down]
y=y[up:down]
droite=(y[-1]-y[0])/(x[-1]-x[0])*(x-x[0])+y[0]
y=droite-y
y=y/max(y)

plt.plot(x,y,label='exp data')
popt,fit=lor_fit(x,y)
plt.plot(x,fit,label='lorentzian fit, HWHM=%f'%popt[2])
plt.legend()

plt.show()