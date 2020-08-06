import sys
import re
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
				try :
					if ',' in line[xcol] :
						line[xcol]=line[xcol].split(',')
						xval=float(line[xcol][0])+float(line[xcol][1])*10**(-len(line[xcol][1]))
					else :
						xval=float(line[xcol])
					if ',' in line[ycol] :
						line[ycol]=line[ycol].split(',')
						yval=float(line[ycol][0])+float(line[ycol][1])*10**(-len(line[ycol][1]))
					else :
						yval=float(line[ycol])

					x+=[xval]
					y+=[yval]
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





# fname='uW_3000'
# transi=[46.41,99.83]
# x,y=extract_data(fname+'.txt')
# y=y/max(y)
# x=x-x[253]
# x=x*63
# plt.plot(x,y,'-',label=fname)
# ax=plt.gca()
# ylim=ax.get_ylim()
# color = next(ax._get_lines.prop_cycler)['color']
# for t in transi :
# 	plt.plot([t,t],[0,2],'--',color=color)
# 	plt.plot([-t,-t],[0,2],'--',color=color)
# ax.set_ylim(ylim)




fname='scan_direct'
transi=[46.41,99.83]
x,y=extract_data(fname+'.txt')
y=y/max(y)
x=x-x[253]
x=x*63
plt.plot(x,y,'-',label=fname)





plt.legend()

plt.show()