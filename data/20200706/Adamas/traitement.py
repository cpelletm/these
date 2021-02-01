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

def lor_fit(x,y,Amp=None,x0=None,sigma=None,ss=None) :
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

def stretch_et_phonon(x,y,Amp=None,tau=None) :
	if not Amp :
		Amp=max(y)-min(y)
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,Amp,tau) :
		return Amp*np.exp(-np.sqrt(x/tau)-x/5E-3)
	p0=[Amp,tau]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1]))

def ask_name():
	qapp = QApplication(sys.argv)
	fname,filters=QFileDialog.getOpenFileName()	
	return fname


# fname='scan_rose_4x_0B_zoom_align3'
# x,y=extract_data(fname+'.txt')
# x2,y2=extract_data(fname+'.txt',xcol=2,ycol=3)
# y2=list(y2)
# xmin=y2.index(max(y2))
# xmax=y2.index(min(y2))
# y2=y2[xmin:xmax]
# y=y[xmin:xmax]
# plt.plot(y2,y)
# popt,yfit=lor_fit(y2,y)
# plt.plot(y2,yfit,label='lor, sigma=%f'%popt[2])


center=2.863

# fname='ESR_4x_3V_zoom_align3'
# x,y=extract_data(fname+'.txt')
# y=y-min(y)
# y=y/max(y)
# y=list(y)
# mil=y.index(min(y))
# x=x+center-x[mil]
# plt.plot(x,y,label=fname)

# fname='ESR_zoom_3V'
# x,y=extract_data(fname+'.txt')
# y=y-min(y)
# y=y/max(y)
# y=list(y)
# mil=y.index(min(y))
# x=x+center-x[mil]
# plt.plot(x,y,label=fname)

# fname='ESR_zoom_5V'
# x,y=extract_data(fname+'.txt')
# y=y-min(y)
# y=y/max(y)
# y=list(y)
# mil=y.index(min(y))
# x=x+center-x[mil]
# plt.plot(x,y,label=fname)

# fname='ESR_zoom_0V'
# x,y=extract_data(fname+'.txt')
# y=y-min(y)
# y=y/max(y)
# plt.plot(x,y,label=fname)

ax = plt.gca()
color = next(ax._get_lines.prop_cycler)['color']

fname='t1_nuit_1x-15-07'
x,y=extract_data(fname+'.txt')
x=x[3:]
y=y[3:]
y=y/y[0]
plt.plot(x*1E3,y,'x',color=color)
popt,yfit=exp_fit(x,y)
plt.plot(x*1E3,yfit,label='No degenerancies',color=color)
print(popt[2])

color = next(ax._get_lines.prop_cycler)['color']
fname='t1_2x2'
x,y=extract_data(fname+'.txt')
x=x[3:]
y=y[3:]
y=y/y[0]
plt.plot(x*1E3,y,'x',color=color)
popt,yfit=exp_fit(x,y)
plt.plot(x*1E3,yfit,label='2-classes degenerancy',color=color)
print(popt[2])


color = next(ax._get_lines.prop_cycler)['color']
fname='T1_100_2V_setup2_nuit'
x,y=extract_data(fname+'.txt')
x=x[1:]
y=y[1:]
y=y/y[0]
plt.plot(x*1E3,y,'x',color=color)
popt,yfit=exp_fit(x,y)
plt.plot(x*1E3,yfit,label='4-classes degenerancy',color=color)
print(popt[2])


# color = next(ax._get_lines.prop_cycler)['color']
# fname='T1_100_0V_setup2_nuit'
# x,y=extract_data(fname+'.txt')
# x=x[1:]
# y=y[1:]
# y=y/y[0]
# plt.plot(x*1E3,y,'x',color=color)
# popt,yfit=exp_fit(x,y)
# plt.plot(x*1E3,yfit,label='0-Field',color=color)





ax.tick_params(labelsize='large')
plt.xlabel(r'Dark time $\tau$ (ms)',fontsize='xx-large')
plt.ylabel('PL (arb.)',fontsize='xx-large')


plt.legend(fontsize='x-large')

plt.show()