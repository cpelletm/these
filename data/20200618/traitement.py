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

def lor_fit(x,y,Amp=None,x0=None,sigma=None) :
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
		return ss+Amp*1/(1+((x-x0)/(2*sigma))**2)
	p0=[Amp,x0,sigma,ss]
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

def stretch_soustraction(x,y,Amp=None,tau=None) :
	if not Amp :
		Amp=max(y)-min(y)
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,Amp,tau) :
		return Amp*np.exp(-np.sqrt(x/tau))
	p0=[Amp,tau]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1]))

def third_stretch(x,y,Amp=None,tau=None) :
	if not Amp :
		Amp=max(y)-min(y)
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,Amp,tau) :
		return Amp*np.exp(-(x/tau)^(1/3))
	p0=[Amp,tau]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1]))


def ask_name():
	qapp = QApplication(sys.argv)
	fname,filters=QFileDialog.getOpenFileName()	
	return fname





# fname='ESR_0B_sans_uW'
# x,y=extract_data(fname+'.txt')
# # y=y-min(y)
# # y=y/max(y)
# plt.plot(x,y,'-x',label='ESR sans uW')

# fname='tdv_1x2x1_2676'
# x,y=extract_data(fname+'.txt')
# y=y/max(y)
# plt.plot(x,y,'x',label='tdv_x1')
# popt,yfit=stretch_soustraction(x,y)
# plt.plot(x,yfit,label='stretch, tau=%f'%popt[1])


# fname='tdv_1x2x1_2850'
# x,y=extract_data(fname+'.txt')
# y=y/max(y)
# plt.plot(x,y,'x',label='tdv_2x')
# popt,yfit=stretch_soustraction(x,y)
# plt.plot(x,yfit,label='stretch, tau=%f'%popt[1])

# fname='tdv_3x_400_us'
# x,y=extract_data(fname+'.txt')
# y=y/max(y)
# plt.plot(x,y,'x',label=fname)
# popt,yfit=stretch_soustraction(x,y)
# plt.plot(x,yfit,label='stretch, tau=%f'%popt[1])

# fname='tdv_0B'
# x,y=extract_data(fname+'.txt')
# y=y/max(y)
# plt.plot(x,y,'x',label=fname)
# popt,yfit=stretch_soustraction(x,y)
# plt.plot(x,yfit,label='stretch, tau=%f'%popt[1])


# fname='tdv_0B_uW_detuned_a_donf'
# x,y=extract_data(fname+'.txt')
# y=y/max(y)
# plt.plot(x,y,'x',label=fname)
# popt,yfit=stretch_soustraction(x,y)
# plt.plot(x,yfit,label='stretch, tau=%f'%popt[1])

fname='tdv_1x_400us'
x,y=extract_data(fname+'.txt')
x=x*1000
y=y/max(y)
plt.plot(x,y,'x',label=fname)
popt,yfit=stretch_soustraction(x,y)
plt.plot(x,yfit,label='stretch, tau=%f'%popt[1])

fname='tdv_1x_100us'
x,y=extract_data(fname+'.txt')
y=y/max(y)
plt.plot(x,y,'x',label=fname)
popt,yfit=stretch_soustraction(x,y)
plt.plot(x,yfit,label='stretch, tau=%f'%popt[1])

# fname='tdv_1x2x1_2770'
# x,y=extract_data(fname+'.txt')
# y=y/max(y)
# plt.plot(x,y,'x',label=fname)
# popt,yfit=stretch_soustraction(x,y)
# plt.plot(x,yfit,label='stretch, tau=%f'%popt[1])



plt.legend()

plt.show()