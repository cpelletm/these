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

def quad_fit(x,y) :
	A=np.vstack([x**2,x,np.ones(len(x))]).T
	a,b,c = np.linalg.lstsq(A, y, rcond=None)[0]
	return([a,b,c],a*x**2+b*x+c)

def fit_ordre_4(x,y) :
	A=np.vstack([x**4,x**3,x**2,x,np.ones(len(x))]).T
	a,b,c,d,e = np.linalg.lstsq(A, y, rcond=None)[0]
	return([a,b,c,d,e],a*x**4+b*x**3+c*x**2+d*x+e)

def fit_ordre_6(x,y) :
	A=np.vstack([x**6,x**5,x**4,x**3,x**2,x,np.ones(len(x))]).T
	w,z,a,b,c,d,e = np.linalg.lstsq(A, y, rcond=None)[0]
	return([w,z,a,b,c,d,e],w*x**6+z*x**5+a*x**4+b*x**3+c*x**2+d*x+e)
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

def lissage(y):
	yl=np.zeros(len(y))
	yl[0]=y[0]
	yl[-1]=y[-1]
	for i in range(1,len(y)-1):
		yl[i]=(y[i]/2+y[i-1]/4+y[i+1]/4)
	return(yl)


def ask_name():
	qapp = QApplication(sys.argv)
	fname,filters=QFileDialog.getOpenFileName()	
	return fname




def fit_droite():
	# xmin=0
	# xmax=-1
	indices=[294,313,327,339,352,368,383,405,456,474]
	xmin=295
	xmax=474#295+113#474

	fname='scan_rose_111'
	x,y=extract_data(fname+'.txt',ycol=1)
	x=x*56.528132258549384-9.624229803755462
	y=y/max(y)
	xs=[]
	ys=[]
	for i in indices :
		xs+=[x[i]]
		ys+=[y[i]]
	xs=np.array(xs)
	ys=np.array(ys)
	plt.plot(x,y)


	# fname='scan_uW_2783'
	# x,y=extract_data(fname+'.txt',ycol=1)
	# x=x*56.528132258549384-9.624229803755462
	# y=y/max(y)


	x=x[xmin:xmax]
	y=y[xmin:xmax]
	popt,yfit=fit_ordre_4(xs,ys)
	plt.plot(x,popt[0]*x**4+popt[1]*x**3+popt[2]*x**2+popt[3]*x+popt[4])

	plt.show()







# Gauche :

# xmax=-1 #c'est pas les bon indices, faut retrouver. Déso
# xmin=292
# x,y=extract_data(fname+'.txt',ycol=1)
# x=x*56.528132258549384-9.624229803755462

# y=y/max(y)
# x=-x
# indices=[211,206,194,190,179,167,154,143,137,119,97,52,45,40]
# xs=[]
# ys=[]
# for i in indices :
# 	xs+=[x[i]]
# 	ys+=[y[i]]
# xs=np.array(xs)
# ys=np.array(ys)
# # popt,yfit=fit_ordre_4(xs,ys)
# popt,yfit=fit_ordre_6(xs,ys)
# x=x[xmin:xmax]
# y=y[xmin:xmax]

# # plt.plot(x,y,lw=2)
# # plt.plot(x,(popt[0]*x**6+popt[1]*x**5+popt[2]*x**4+popt[3]*x**3+popt[4]*x**2+popt[5]*x+popt[6]),'--',lw=2)

# plt.plot(x,y-(popt[0]*x**6+popt[1]*x**5+popt[2]*x**4+popt[3]*x**3+popt[4]*x**2+popt[5]*x+popt[6]))

#Droite : 
ax=plt.gca()
fname='scan_rose_111'
xmax=-1
xmin=295
x,y=extract_data(fname+'.txt',ycol=1)
x=x*56.528132258549384-9.624229803755462
y=y/max(y)
x=x[xmin:xmax]
y=y[xmin:xmax]
popt,yfit=fit_ordre_4(x,y)
yfit=yfit+0.0002
# plt.plot(x,y,lw=2)
# plt.plot(x,yfit,'--',lw=2)

plt.plot(x,y-yfit,'o-',lw=2,markerfacecolor="None")


x_transis=[29.4, 113.2, 45.8, 42.0, 86.2, 76.2, 72.1, 122.2, 97.3] #Cruddace
x_VH=[31.4, 125.0, 49.4, 45.1, 92.4, 81.1] #nous
x_War1=[ 71.8, 96.8, 121.7]
ylim=ax.get_ylim()
color=next(ax._get_lines.prop_cycler)['color']
for x in x_VH :
	plt.plot([x,x],[-1,1],ls='dotted',color=color,lw=2.5)
color=next(ax._get_lines.prop_cycler)['color']
for x in x_War1 :
	plt.plot([x,x],[-1,1],ls='dashed',color=color,lw=2)
ax.set_ylim(ylim)

plt.xlabel(r'B$\parallel$[111] (G)', fontsize=15)
plt.ylabel('Photoluminescence', fontsize=15)
ax.tick_params(labelsize=15)
plt.show()