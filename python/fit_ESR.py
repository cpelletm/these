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

def gauss_fit(x,y,Amp=None,x0=None,sigma=None,ss=0) :
	if not ss :
		ss=y[0]
	if not Amp :
		if max(y)-ss > ss-min(y) :
			Amp=max(y)-ss
		else :
			Amp=min(y)-ss
	if not x0 :
		x0=x[int(len(x)/2)]
	if not sigma :
		sigma=x[int(len(x)/5)]-x[0]
	def f(x,Amp,x0,sigma,ss) :
		return Amp*np.exp(-((x-x0)/(2*sigma))**2)+ss
	p0=[Amp,x0,sigma,ss]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1],popt[2],popt[3]))

def ESR_1_pic(x,y,c1,width=8,ss=None,amp=None) :
	if not ss :
		ss=y[0]
	if not amp :
		if max(y)-ss > ss-min(y) :
			amp=max(y)-ss
		else :
			amp=min(y)-ss
	def f(x,c1,width,ss,amp) :
		return amp*np.exp(-((x-c1)/width)**2)+ss
	p0=[c1,width,ss,amp]
	popt, pcov = curve_fit(f, x, y, p0)
	variables=(x,)
	for p in popt :
		variables+=(p,)
	return(f(*variables))

def ESR_2_pic(x,y,c1,c2,width=8,ss=None,amp=None) :
	if not ss :
		ss=y[0]
	if not amp :
		if max(y)-ss > ss-min(y) :
			amp=max(y)-ss
		else :
			amp=min(y)-ss
	width1=width
	width2=width
	amp1=amp
	amp2=amp
	def f(x,c1,c2,width1,width2,amp1,amp2,ss) :
		return ss+amp1*np.exp(-((x-c1)/width1)**2)+amp2*np.exp(-((x-c2)/width2)**2)
	p0=[c1,c2,width1,width2,amp1,amp2,ss]
	popt, pcov = curve_fit(f, x, y, p0)
	variables=(x,)
	for p in popt :
		variables+=(p,)
	return(f(*variables))

def ESR_n_pics(x,y,cs,width=8,ss=None,amp=None) :
	if not ss :
		ss=y[0]
	if not amp :
		if max(y)-ss > ss-min(y) :
			amp=max(y)-ss
		else :
			amp=min(y)-ss
	n=len(cs)
	widths=np.ones(n)*width
	amps=np.ones(n)*amp
	p0=[ss]
	for c in cs:
		p0+=[c]
	for w in widths:
		p0+=[w]
	for a in amps:
		p0+=[a]
	def f(x,*params):
		ss=params[0]
		n=(len(params)-1)//3
		y=ss
		for i in range(n):
			c=params[1+i]
			width=params[1+n+i]
			amp=params[1+2*n+i]
			y+=amp*np.exp(-((x-c)/width)**2)
		return(y)
	popt, pcov = curve_fit(f, x, y, p0)
	variables=(x,)
	for p in popt :
		variables+=(p,)
	return(f(*variables))




def ask_name():
	qapp = QApplication(sys.argv)
	fname,filters=QFileDialog.getOpenFileName()	
	return fname

ax=plt.gca()
color = next(ax._get_lines.prop_cycler)['color']
x,y=extract_data('fit_ESR/ESR_full_4x.txt')
x=x*1000
y=y/max(y)
plt.plot(x,y,'x',color=color)
yfit=ESR_n_pics(x,y,[2725,3089]) #Attention, pics en MHz
plt.plot(x,yfit,lw=2,color=color)

plt.xlabel('Frequency (MHz)',fontsize=25)
plt.ylabel('PL (arb.)',fontsize=25)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()