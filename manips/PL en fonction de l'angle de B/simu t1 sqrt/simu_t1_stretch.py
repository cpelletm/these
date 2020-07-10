import numpy as np
from numpy import exp,sqrt
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy.random import random,seed



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

seed(1234)

taux=random(1000)

x=np.linspace(0,5,200)
y=np.zeros(200)

for tau in taux :
	y+=exp(-x/tau)

y=y/len(taux)
plt.plot(x,y,'x')

popt,yfit=stretch_exp_fit(x,y)
plt.plot(x,yfit,label='stretch')

popt,yfit=exp_fit(x,y)
plt.plot(x,yfit,label='exp')

plt.legend()
plt.show()

