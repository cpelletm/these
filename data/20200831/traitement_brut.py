import sys
import numpy as np
import matplotlib.pyplot as plt
import glob
from scipy.optimize import curve_fit,root_scalar
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
	x=np.array(x)
	y=np.array(y)
	A=np.vstack([x,np.ones(len(x))]).T
	a,b = np.linalg.lstsq(A, y, rcond=None)[0]
	return(a,b,a*x+b)

def quad_fit(x,y) :
	x=np.array(x)
	y=np.array(y)
	A=np.vstack([x**2,x,np.ones(len(x))]).T
	q,a,b = np.linalg.lstsq(A, y, rcond=None)[0]
	return([q,a,b],q*x**2+a*x+b)

def gauss_fit(x,y,Amp=None,x0=None,sigma=None,ss=0) :
	if not ss :
		ss=y[0]
	if not Amp :
		if max(y)-ss > ss-min(y) :
			Amp=max(y)-ss
		else :
			Amp=min(y)-ss
	if not x0 :
		if max(y)-ss > ss-min(y) :
			x0=x[np.argmax(y)]
		else :
			x0=x[np.argmin(y)]
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

fname='blanc.txt'
x,y=extract_data(fname)
bmin=243
bmax=707
x=x[bmin:bmax]
y=y[bmin:bmax]
y=y-min(y)
y=y/max(y)
plt.plot(x,y)

fname='blanc_rose.txt'
x,y=extract_data(fname)
x=x[bmin:bmax]
y=y[bmin:bmax]
y=y-min(y)
y=y/max(y)
plt.plot(x,y)


Sx=1/np.sqrt(2)*np.array([[0,1,0],[1,0,1],[0,1,0]])
Sy=1/(np.sqrt(2)*1j)*np.array([[0,1,0],[-1,0,1],[0,-1,0]])
Sz=np.array([[1,0,0],[0,0,0],[0,0,-1]])
def Hamiltonian_0(B,classe=1,E=3,D=2870) :
	#Unité naturelle : MHz,Gauss
	B=np.array(B)
	gamma=2.8
	if classe==1 :
		C=np.array([1,1,1])/np.sqrt(3)
		Bz=B.dot(C)
		Bx=np.sqrt(abs(B.dot(B)-Bz**2))
	if classe==2 :
		C=np.array([1,-1,-1])/np.sqrt(3)
		Bz=B.dot(C)
		Bx=np.sqrt(abs(B.dot(B)-Bz**2))
	if classe==3 :
		C=np.array([-1,1,-1])/np.sqrt(3)
		Bz=B.dot(C)
		Bx=np.sqrt(abs(B.dot(B)-Bz**2))
	if classe==4 :
		C=np.array([-1,-1,1])/np.sqrt(3)
		Bz=B.dot(C)
		Bx=np.sqrt(abs(B.dot(B)-Bz**2))
	H=D*Sz**2+gamma*(Bx*Sx+Bz*Sz)+E*(Sx.dot(Sx)-Sy.dot(Sy))
	return H
def egvect(H) :
	val,vec=np.linalg.eigh(H) #H doit être Hermitienne
	vec=vec.T #Les vecteurs propres sortent en LIGNE (vecteur #1 : vec[0])
	return(val,vec)
def zero(nu):
	def f(amp):
		B=[amp,0,0]
		H=Hamiltonian_0(B,classe=1,E=3,D=2870)
		val,vec=egvect(H)		
		return val[2]-val[0]-nu
	RR=root_scalar(f,bracket=[0,200])
	return(RR.root)

print(zero(2963))

plt.legend()
plt.show()