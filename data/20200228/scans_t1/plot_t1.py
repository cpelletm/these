import sys
import time
import random
import os
import matplotlib.pyplot as plt
import numpy as np

from scipy.optimize import curve_fit

voltage=np.arange(0,1.40,0.02)


fnames=['%3i.txt'%(v*100) for v in voltage]
taux=[]
error=[]

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
	popt, pcov = curve_fit(f, x, y, p0)#,sigma=np.ones(len(y))*2E3, absolute_sigma=True)
	return(popt,pcov,f(x,popt[0],popt[1],popt[2]))

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
	return(popt,pcov,f(x,popt[0],popt[1],popt[2]))

for fname in fnames :
	x,y=extract_data(fname)
	popt,pcov,yfit=exp_fit(x,y)
	taux+=[popt[2]]
	perr = np.sqrt(np.diag(pcov))
	error+=[perr[2]]

taux=np.array(taux)

print(taux,error)
#plt.plot(voltage,taux)
plt.errorbar(voltage,taux,yerr=error)
plt.xlabel('tension(V)')
plt.ylabel('t1(s)')

plt.show()
