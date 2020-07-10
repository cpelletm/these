import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit




def extract_data(filename,xcol=0,ycol=1):

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
			x[i]=float(line[xcol])
			y[i]=float(line[ycol])

	return(x,y)




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



for i in (20,52,107,266,600,1200) :
	fname='%iuW.txt'%i
	x,y=extract_data(fname)
	ymax=sum(y[-10:])/10
	y=y/ymax
	plt.plot(x,y,label='%i uW'%i)





plt.legend()

plt.show()