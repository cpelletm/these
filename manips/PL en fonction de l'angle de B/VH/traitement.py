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


x_transi=[82.85779704691888, 49.26889421556611, 153.09765463190857, 80.9166748302668, 6.222636078130301, 136.53699671424204, 17.389247810767305]

# fname='scan_rose_100_7V_'
# x,y=extract_data(fname+'.txt')
# y=y/max(y)
# xmin=258
# x=x-x[xmin]
# x=x[:xmin]
# y=y[:xmin]
# x=x*64
# plt.plot(x,y,label='Photoluminescence')

fname='scan_100_rose_10V'
x,y=extract_data(fname+'.txt')
y=y/max(y)
xmin=507
x=x-x[xmin]
x=x[xmin:]
y=y[xmin:]
x=x*62
plt.plot(-x,y,label='Photoluminescence')


# fname='scan_100_sample_ludo_aligne_vitedeuf'
# x,y=extract_data(fname+'.txt')
# y=y/max(y)
# x=x*62
# xmin=251
# x=x-x[xmin]
# x=x[:xmin]
# y=y[:xmin]
# plt.plot(x,y,label='Photoluminescence')

# fname='scan_10V_uW_2796'
# x,y=extract_data(fname+'.txt')
# y=y/max(y)
# x=x-x[253]
# x=x*62
# plt.plot(-x,y,label='Photoluminescence')


ax=plt.gca()
ylim=ax.get_ylim()
color = next(ax._get_lines.prop_cycler)['color']
# x=x_transi[0]
# plt.plot([x,x],[0,2],'--',color=color,label='P1 cross relaxation')
# # plt.plot([-x,-x],[0,2],'--',color=color)
# for x in x_transi[1:] :
# 	plt.plot([x,x],[0,2],'--',color=color)
# 	# plt.plot([-x,-x],[0,2],'--',color=color)
# color = next(ax._get_lines.prop_cycler)['color']
x=50.5276
plt.plot([x,x],[0,2],'--',color=color,label='VH cross relaxation')
ax.set_ylim(ylim)

plt.xlabel(r'B$\parallel$(100) (G)')
plt.legend()

plt.show()