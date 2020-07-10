import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


filename='scan_PL_sumi4_large.txt'

with open(filename,'r') as f:
	N=0
	for line in f :
		N+=1

x=np.zeros(N)
y=np.zeros(N)

with open(filename,'r') as f:
	for i in range(N) :
		line=f.readline()
		line=line.split()
		x[i]=float(line[0])
		y[i]=float(line[1])

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

x2=x[95:115]
y2=y[95:115]
a,b=lin_fit(x2,y2)

x=x[100:]
y=y[100:]
y=(a*x+b)-y

plt.plot(x,y,'x')

Amp,x0,sigma=gauss_fit(x,y,30000,7,0.5)
yfit=Amp*np.exp(-((x-x0)/(2*sigma))**2)
plt.plot(x,yfit,label='gaussienne')

Amp,x0,sigma=lor_fit(x,y,30000,7,0.5)
yfit=Amp*1/(1+((x-x0)/(2*sigma))**2)
plt.plot(x,yfit,label='lorentzienne')



plt.legend()

plt.show()