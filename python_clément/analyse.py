import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit,root_scalar,minimize
from scipy.signal import find_peaks
from scipy import fftpack
from PyQt5.QtWidgets import QApplication,QFileDialog




def extract_data(filename,xcol=0,ycol=1,exclude_neg=True,data='line',delimiter='auto'):
	import csv
	if len(filename)<=4 or filename[-4]!='.' :
		if glob.glob(filename+'.txt') :
			f=glob.glob(filename+'.txt')[0]
		elif glob.glob(filename+'.csv') :
			f=glob.glob(filename+'.csv')[0]
		elif glob.glob(filename+'.asc') :
			f=glob.glob(filename+'.asc')[0]
		else :
			print('file not found')
			quit()
		filename=f
	if filename[-4:] =='.txt' : #Assumes that data is in column
		x=[]
		y=[]
		with open(filename,'r',encoding = "ISO-8859-1") as f:
			for line in f :
				line=line.split()
				try :
					if exclude_neg : #c'est extrèmement gitan ça monsieur
						if float(line[xcol])!=-1 :
							x+=[float(line[xcol])]
							y+=[float(line[ycol])]
					else :
						x+=[float(line[xcol])]
						y+=[float(line[ycol])]				
				except :
					pass
		return(np.array(x),np.array(y))
	elif filename[-4:] =='.asc' :
		x=[]
		y=[]
		def convert_comma_number(x):
			x=x.split(',')
			if len(x)==2 :
				y=float(x[0])+float(x[1])*10**(-len(x[1]))
			elif len(x)==1 :
				y=float(x[0])
			return y
		with open(filename,'r',encoding = "ISO-8859-1") as f:
			for line in f:
				line=line.split()
				try :
					x+=[convert_comma_number(line[0])]
					y+=[convert_comma_number(line[1])]
				except :
					pass
		return(np.array(x),np.array(y))
	elif filename[-4:] =='.csv' and data=='line':
		if delimiter=='auto' :
			delimiter=' '
		with open(filename,'r',encoding = "ISO-8859-1") as f:
			content=f.readlines()
			x=content[xcol]
			x=x.split()
			xdata=[]
			for item in x :
				try :
					xdata+=[np.float(item)]
				except :
					pass
			y=content[ycol]
			y=y.split()
			y=[np.float(item) for item in y]
			ydata=[]
			for item in y :
				try :
					ydata+=[np.float(item)]
				except :
					pass
		return(np.array(xdata),np.array(ydata))
	elif filename[-4:] =='.csv' and (data=='column' or data=='col'):
		if delimiter=='auto' :
			delimiter=','
		with open(filename,'r',encoding = "ISO-8859-1") as f:
			reader = csv.reader(f, delimiter=delimiter, quotechar='|')
			xdata=[]
			ydata=[]
			for line in reader:
				try :
					xdata+=[np.float(line[xcol])]
					ydata+=[np.float(line[ycol])]
				except :
					continue #pass marcherait aussi mais je me la pète
		return(np.array(xdata),np.array(ydata))


#~~~~ Fits ~~~~
def lin_fit(x,y) :
	A=np.vstack([x,np.ones(len(x))]).T
	a,b = np.linalg.lstsq(A, y, rcond=None)[0]
	return([a,b],a*x+b)

def quad_fit(x,y) :
	A=np.vstack([x**2,x,np.ones(len(x))]).T
	a,b,c = np.linalg.lstsq(A, y, rcond=None)[0]
	return([a,b,c],a*x**2+b*x+c)

def parabola_fit(x,y):
	if y[0]-min(y) > max(y)-y[0] :
		typ='upside'
	else :
		typ='downside'

	if typ=='upside' :
		x0=x[list(y).index(min(y))]
		y0=min(y)
		a=(y[0]-min(y))/(x[0]-x0)**2
	else :
		x0=x[list(y).index(max(y))]
		y0=max(y)
		a=(y[0]-max(y))/(x[0]-x0)**2

	def f(x,a,x0,y0):
		return a*(x-x0)**2+y0

	p0=[a,x0,y0]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,*popt))

def fit_ordre_4(x,y) :
	A=np.vstack([x**4,x**3,x**2,x,np.ones(len(x))]).T
	a,b,c,d,e = np.linalg.lstsq(A, y, rcond=None)[0]
	return([a,b,c,d,e],a*x**4+b*x**3+c*x**2+d*x+e)

def fit_ordre_6(x,y) :
	A=np.vstack([x**6,x**5,x**4,x**3,x**2,x,np.ones(len(x))]).T
	w,z,a,b,c,d,e = np.linalg.lstsq(A, y, rcond=None)[0]
	return([w,z,a,b,c,d,e],w*x**6+z*x**5+a*x**4+b*x**3+c*x**2+d*x+e)

def gauss_fit(x,y,amp=None,x0=None,sigma=None,ss=0) :
	if not ss :
		ss=y[0]
	if not amp :
		if max(y)-ss > ss-min(y) :
			amp=max(y)-ss
		else :
			amp=min(y)-ss
	if not x0 :
		x0=x[int(len(x)/2)]
	if not sigma :
		sigma=x[int(len(x)/5)]-x[0]
	def f(x,amp,x0,sigma,ss) : #HWHM=1.18*sigma (sqrt(2*ln(2)))
		return amp*np.exp(-(x-x0)**2/(2*sigma**2))+ss
	p0=[amp,x0,sigma,ss]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1],popt[2],popt[3]))

def lor_fit(x,y,amp=None,x0=None,sigma=None,ss=None) :
	if not ss :
		ss=y[0]
	if not amp :
		if max(y)-ss > ss-min(y) :
			amp=max(y)-ss
		else :
			amp=min(y)-ss
	if not x0 :
		x0=x[int(len(x)/2)]
	if not sigma :
		sigma=x[int(len(x)/5)]-x[0]
	def f(x,amp,x0,sigma,ss) :
		return ss+amp*1/(1+((x-x0)/(2*sigma))**2)
	p0=[amp,x0,sigma,ss]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1],popt[2],popt[3]))

def cos_fit(x,y,amp=None,omega=None,phi=0,ss=None):
	if not amp :
		amp=max(y)-min(y)
	if not omega :
		omega=2*np.pi/(max(x)-min(x))
	if not ss :
		ss=y[-1]
	def f(x,amp,omega,phi,ss):
		return amp*np.cos(omega*x+phi)+ss
	p0=[amp,omega,phi,ss]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,*popt))


def exp_fit(x,y,amp=None,ss=None,tau=None) :
	if not amp :
		amp=max(y)-min(y)
	if not ss :
		ss=y[-1]
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,amp,ss,tau) :
		return amp*np.exp(-x/tau)+ss
	p0=[amp,ss,tau]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1],popt[2]))

def exp_fit_zero(x,y,amp=None,tau=None) :
	if not amp :
		amp=max(y)-min(y)
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,amp,tau) :
		return amp*np.exp(-x/tau)
	p0=[amp,tau]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1]))

def stretch_exp_fit(x,y,amp=None,ss=None,tau=None) :
	if not amp :
		amp=max(y)-min(y)
	if not ss :
		ss=y[-1]
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,amp,ss,tau) :
		return amp*np.exp(-np.sqrt(x/tau))+ss
	p0=[amp,ss,tau]
	popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,-np.inf,0],[np.inf,np.inf,np.inf]))
	return(popt,f(x,popt[0],popt[1],popt[2]))

def stretch_exp_fit_zero(x,y,amp=None,tau=None) :
	if not amp :
		amp=max(y)-min(y)
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,amp,tau) :
		return amp*np.exp(-np.sqrt(x/tau))
	p0=[amp,tau]
	popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,0],[np.inf,np.inf]))
	return(popt,f(x,popt[0],popt[1]))

def stretch_arb_exp_fit(x,y,amp=None,ss=None,tau=None,alpha=0.5,fixed=False):
	if not amp :
		amp=max(y)-min(y)
	if not ss :
		ss=y[-1]
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	if fixed :
		def f(x,amp,ss,tau) :
			return amp*np.exp(-(x/tau)**alpha)+ss
		p0=[amp,ss,tau]
		popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,-np.inf,0],[np.inf,np.inf,np.inf]))
	else :
		def f(x,amp,ss,tau,alpha) :
			return amp*np.exp(-(x/tau)**alpha)+ss
		p0=[amp,ss,tau,alpha]
		popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,-np.inf,0,0],[np.inf,np.inf,np.inf,np.inf]))
	return(popt,f(x,*popt))

def stretch_arb_exp_fit_zero(x,y,amp=None,tau=None,alpha=0.5,fixed=False):
	if not amp :
		amp=max(y)-min(y)
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	if fixed :
		def f(x,amp,tau) :
			return amp*np.exp(-(x/tau)**alpha)
		p0=[amp,tau]
		popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,0],[np.inf,np.inf]))
	else :
		def f(x,amp,tau,alpha) :
			return amp*np.exp(-(x/tau)**alpha)
		p0=[amp,tau,alpha]
		popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,0,0],[np.inf,np.inf,np.inf]))
	return(popt,f(x,*popt))


def stretch_with_baseline(x,y,tau_BL=5e-3,alpha_BL=1,alpha_dip=0.5,amp=None,tau=None):
	if not amp :
		amp=max(y)-min(y)
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,amp,tau) :
		return amp*np.exp(-(x/tau_BL)**alpha_BL)*np.exp(-(x/tau)**alpha_dip)
	p0=[amp,tau]
	popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,0],[np.inf,np.inf]))
	return(popt,f(x,*popt))

def third_stretch(x,y,amp=None,tau=None) :
	if not amp :
		amp=max(y)-min(y)
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,amp,tau) :
		return amp*np.exp(-(x/tau)^(1/3))
	p0=[amp,tau]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1]))

def stretch_et_phonons(x,y,amp=None,tau=None,ss=None,T1ph=5E-3) :
	if not amp :
		amp=max(y)-min(y)
	if not ss :
		ss=y[-1]
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,amp,ss,tau) :
		return amp*np.exp(-x/((T1ph*np.sqrt(x*tau))/(T1ph+np.sqrt(x*tau))))+ss
	p0=[amp,ss,tau]
	popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,-np.inf,0],[np.inf,np.inf,np.inf]))
	return(popt,f(x,popt[0],popt[1],popt[2]))

def Rabi_fit(x,y,amp=None,omega=None,tau=None,ss=None):
	if not amp :
		amp=max(y)-min(y)
	if not ss :
		ss=y[-1]
	if not tau :
		tau=x[int(len(x)/3)]-x[0]
	if not omega :
		omega=1/(x[int(len(x)/10)]-x[0])
	def f(x,amp,ss,tau,omega) :
		return amp*np.exp(-x/tau)*np.cos(omega*x)+ss
	p0=[amp,ss,tau,omega]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,*popt))

def fit_B_dipole(x,y,B0=2000,x0=10) : #x : distance en mm, y : champ mag en G
	def f(x,B0,x0):
		return(B0/(x+x0)**3)
	p0=[B0,x0]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1]))

def ESR_n_pics(x,y,cs,width=False,ss=None,amp=None,typ='gauss') : #typ="gauss" ou "lor"
	if not ss :
		ss=y[0]
	if not amp :
		if max(y)-ss > ss-min(y) :
			amp=max(y)-ss
		else :
			amp=min(y)-ss
	if not width :
		if max(x) < 50 : #Je sq c'est des GHz
			width=8e-3
		elif max(x) < 5E4 : #Je sq c'es des Mhz
			width=8
		else : #Je sq c'es des Hz
			width=8E6
	n=len(cs)
	widths=np.ones(n)*width
	amps=np.ones(n)*amp
	p0=[ss]
	for c in cs:
		p0+=[c]
	for w in widths:
		p0+=[w]
	for a in amps:
		p0+=[a]
	def f(x,*params):
		ss=params[0]
		n=(len(params)-1)//3
		y=ss
		for i in range(n):
			c=params[1+i]
			width=params[1+n+i]
			amp=params[1+2*n+i]
			if typ=="gauss" :
				y+=amp*np.exp(-((x-c)/width)**2)
			elif typ=="lor" :
				y+=amp*1/(1+((x-c)/width)**2)
		return(y)
	popt, pcov = curve_fit(f, x, y, p0)
	ss=popt[0]
	centers=popt[1:n+1]
	widths=abs(popt[n+1:2*n+1])
	amps=popt[2*n+1:]
	params=[ss,centers,widths,amps]
	return(params,f(x,*popt))

def ESR_fixed_amp_and_width(x,y,cs,amp=False,width=False,ss=False,typ='gauss'):
	if not ss :
		ss=y[0]
	if not amp :
		if max(y)-ss > ss-min(y) :
			amp=max(y)-ss
		else :
			amp=min(y)-ss
	if not width :
		if max(x) < 50 : #Je sq c'est des GHz
			width=1e-3
		elif max(x) < 5E4 : #Je sq c'es des Mhz
			width=1
		else : #Je sq c'es des Hz
			width=1E6
	p0=[ss,amp,width,*cs]
	def f(x,*params):
		ss=params[0]
		amp=params[1]
		width=params[2]
		cs=params[3:]
		y=ss
		for c in cs :
			if typ=="gauss" :
				y+=amp*np.exp(-((x-c)/width)**2)
			elif typ=="lor" :
				y+=amp*1/(1+((x-c)/width)**2)
		return(y)
	popt, pcov = curve_fit(f, x, y, p0)
	ss=popt[0]
	centers=popt[3:]
	width=abs(popt[2])
	amp=popt[1]
	params=[ss,centers,width,amp]
	return(params,f(x,*popt))

def find_ESR_peaks(x,y,width=False,threshold=0.1,returnUnit='x',precise=False):
	'''
	width in unit of x  
	thrsehold = min peak height in proportion of max peak height 
	returnUnit='x' : return the x position of the peaks ; ='n' return the index of the peaks
	'''
	if not width :
		distance=int(10/(x[1]-x[0])) #assumes that x is in MHz, and takes an ESR width of 10 MHz
	else :
		distance=int(width/(x[1]-x[0]))

	y=y-min(y)
	y=y/max(y)
	if y[0]-min(y) > max(y)-y[0] : #Setup "ESR PL" (pics à l'envers)
		y=1-y
	height=threshold

	ns=find_peaks(y,height=height,distance=distance)[0]
	cs=[x[i] for i in ns]

	if precise :
		popt,yfit=ESR_n_pics(x,y,cs,width=width)
		cs=popt[1]
		for k in range(len(cs)):
			i=0
			while x[i]<cs[k] :
				i+=1
			ns[k]=i

	if returnUnit=='x' :
		return(np.array(cs))
	if returnUnit=='n' :
		return(ns)

def find_B_111(freq,transi='-') : #freq en MHz
	D=2870
	gamma=2.8
	if transi=='-' :
		return(D-freq)/gamma
	elif transi =='+' :
		return(freq-D)/gamma

def find_B_100(freq,transi='-',B_max=100) :
	Sz=np.array([[1,0,0],[0,0,0],[0,0,-1]])
	Sx=1/np.sqrt(2)*np.array([[0,1,0],[1,0,1],[0,1,0]])
	Sy=1/(np.sqrt(2)*1j)*np.array([[0,1,0],[-1,0,1],[0,-1,0]])

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


	def f(amp):
		B=[amp,0,0]
		H=Hamiltonian_0(B,classe=1,E=3,D=2870)
		val,vec=egvect(H)
		if transi=='-' :
			transi_NV=val[1]-val[0]
		if transi=='+' :
			transi_NV=val[2]-val[0]

		return transi_NV-freq


	RR=root_scalar(f,bracket=[0,B_max])
	return RR.root



class NVHamiltonian(): #x,y and z axis are taken as (100) axis
	D=2870 #Mhz
	gamma_e=2.8 #Mhz/gauss

	Sz=np.array([[1,0,0],[0,0,0],[0,0,-1]])
	Sy=np.array([[0,-1j,0],[1j,0,-1j],[0,1j,0]])*1/np.sqrt(2)
	Sx=np.array([[0,1,0],[1,0,1],[0,1,0]])*1/np.sqrt(2)
	Sz2=np.array([[1,0,0],[0,0,0],[0,0,1]]) # Pour éviter une multilplcation matricielle

	c1=np.array([-1,1.,-1])/np.sqrt(3)
	c2=np.array([1,1,1])/np.sqrt(3)
	c3=np.array([-1,-1,1])/np.sqrt(3)
	c4=np.array([1,-1,-1])/np.sqrt(3)
	cs=[c1,c2,c3,c4]
	def __init__(self,B,c=1): #If B is not a magneticField Instance it should be of the form [Bx,By,Bz]
		if not isinstance(B,magneticField):
			B=magneticField(x=B[0],y=B[1],z=B[2])
		Bz=self.cs[c].dot(B.cartesian) #Attention, ici Bz est dans la base du NV (Bz')
		Bx=np.sqrt(abs(B.amp**2-Bz**2))#le abs est la pour éviter les blagues d'arrondis. Je mets tout ce qui n'est pas sur z sur le x
		self.H=self.D*self.Sz2+self.gamma_e*(Bz*self.Sz+Bx*self.Sx) #Rajoute des fioritures si tu veux
	def transitions(self):
		egva,egve=np.linalg.eigh(self.H)
		egva=np.sort(egva)
		return [egva[1]-egva[0],egva[2]-egva[0]]

class magneticField():
	def __init__(self,x='spherical',y='spherical',z='spherical',theta='cartesian',phi='cartesian',amp='cartesian'): #Give either x,y,z or theta,phi,amp (polar/azimutal from the z axis)
		if x=='spherical':
			self.x=amp*np.cos(theta)*np.sin(phi)
			self.y=amp*np.sin(theta)*np.sin(phi)
			self.z=amp*np.cos(phi)
			self.theta=theta
			self.phi=phi
			self.amp=amp
		elif theta=='cartesian' :
			self.amp=np.sqrt(x**2+y**2+z**2)
			self.theta=np.arccos(z/self.amp)
			self.phi=np.arctan2(y,x)
			self.x=x
			self.y=y
			self.z=z
		else :
			raise(ValueError('You must either give (x,y,z) or (theta,phi,amp )'))
		self.cartesian=np.array([self.x,self.y,self.z])
		self.sphericalDeg=np.array([self.theta*180/np.pi,self.phi*180/np.pi])
	def transitions4Classes(self):
		transis=[]
		for i in range(4):
			t=NVHamiltonian(self,c=i).transitions()
			transis+=[t[0],t[1]]
		return np.sort(transis)
	def transitions4ClassesPlus(self):
		transis=[]
		for i in range(4):
			t=NVHamiltonian(self,c=i).transitions()
			transis+=[t[1]]
		return np.sort(transis)
	def transitions4ClassesMoins(self):
		transis=[]
		for i in range(4):
			t=NVHamiltonian(self,c=i).transitions()
			transis+=[t[0]]
		return np.sort(transis)

	def __repr__(self):
		return('Bx=%f; By=%f, Bz= %f'%(self.x,self.y,self.z))

class electricField():
	def __init__(*params,base='NV'):
		pass

def find_B_cartesian(peaks,Bmax=1000,startingB=False,transis='all'): #B in gauss ; Ca m'a la'ir de moins bien marcher que l'autre
	peaks=np.sort(peaks)
	if len(peaks)==8 :
		def err_func(B,peaks): #B is given in the form [amp,theta,phi]
			B=magneticField(x=B[0],y=B[1],z=B[2])
			simuPeaks=B.transitions4Classes()
			err=np.linalg.norm(peaks-simuPeaks)
			return err
	elif len(peaks)==2:
		def err_func(B,peaks): #B is given in the form [amp,theta,phi]
			B=magneticField(x=B[0],y=B[1],z=B[2])
			simuPeaks=B.transitions4Classes()
			completePeaks=np.sort([peaks[0]]*4+[peaks[1]]*4)
			err=np.linalg.norm(completePeaks-simuPeaks)
			return err
	elif len(peaks)==4 and transis=='-': 
		def err_func(B,peaks): #B is given in the form [amp,theta,phi]
			B=magneticField(amp=B[0],theta=B[1],phi=B[2])
			simuPeaks=B.transitions4ClassesMoins()
			err=np.linalg.norm(peaks-simuPeaks)
			return err
	elif len(peaks)==4 and transis=='+': 
		def err_func(B,peaks): #B is given in the form [amp,theta,phi]
			B=magneticField(amp=B[0],theta=B[1],phi=B[2])
			simuPeaks=B.transitions4ClassesPlus()
			err=np.linalg.norm(peaks-simuPeaks)
			return err
	if startingB :
		x0=[startingB.amp,startingB.theta,startingB.phi]
	else :
		x0=[100,0,0]
	sol=minimize(err_func,x0=x0,args=peaks,bounds=[(-Bmax,Bmax),(-Bmax,Bmax),(-Bmax,Bmax)]) #c'est équivalent à un rectangle dans [0,54.74]x[0,45] deg
	return magneticField(amp=sol.x[0],theta=sol.x[1],phi=sol.x[2])



def simu_ESR(x,peaks,widths=8,amps=-0.1,ss=1,typ='gauss'):
	n=len(peaks)
	if not (isinstance(widths,list) or isinstance(widths,np.ndarray)):
		widths=[widths]*n
	if not (isinstance(amps,list) or isinstance(amps,np.ndarray)):
		amps=[amps]*n
	y=np.ones(len(x))*ss
	for i in range(n):
		c=peaks[i]
		width=widths[i]
		amp=amps[i]
		if typ=='gauss' :
			y+=amp*np.exp(-((x-c)/width)**2)
		elif typ=="lor" :
			y+=amp*1/(1+((x-c)/width)**2)
	return y

def find_nearest_ESR(x,y,peaks,Bmax=1000,typ='gauss',returnType='default',transis='all',fittingProtocol='spherical'): #peaks : centers of resonances in MHz
	popt,yfit= ESR_n_pics(x,y,peaks)
	n=len(peaks)
	ss=popt[0]
	peaks=popt[1]
	widths=popt[2]
	amps=popt[3]
	if fittingProtocol=='spherical' :
		B=find_B_spherical(peaks,Bmax=Bmax,transis=transis)
	elif fittingProtocol=='cartesian' :
		B=find_B_cartesian(peaks,Bmax=Bmax,transis=transis)
	if transis=='all' :
		cs=B.transitions4Classes()
	elif transis=='+':
		cs=B.transitions4ClassesPlus()
	elif transis=='-':
		cs=B.transitions4ClassesMoins()

	if n==2 :
		widths=[widths[0]]*4+[widths[1]]*4
		amps=[amps[0]/4]*4+[amps[1]/4]*4
	elif n==4 :
		pass #A implanter avec la 111, comme find_B
	yfit=simu_ESR(x,cs,widths,amps,ss,typ=typ)
	def angleFrom100(B):
		scalar=max(abs(B.x),abs(B.y),abs(B.z))/B.amp
		angle=np.arccos(scalar)
		return angle*180/np.pi
	def angleFrom111(B):
		scalar=0
		for c in NVHamiltonian.cs :
			if abs(c.dot(B.cartesian)) > scalar :
				scalar=abs(c.dot(B.cartesian))
		scalar=scalar/B.amp
		angle=np.arccos(scalar)
		return angle*180/np.pi
	if returnType=='spherical' :
		popt=[B.amp,B.theta,B.phi]
	elif returnType=='cartesian' :
		popt=[B.x,B.y,B.z]
	else :
		popt=[B.amp,angleFrom100(B),angleFrom111(B),sum(widths)/len(widths)]
	return popt,yfit

#~~~~~~ stats ~~~~~~
def mean(y):
	return np.average(y)

def hist_mean(x,y):
	return np.average(x,weights=y)

def sigma(y):
	mu=mean(y)
	return np.sqrt(np.average((y-mu)**2))

def hist_sigma(x,y):
	mu=hist_mean(x,y)
	return np.sqrt(np.average((x-mu)**2,weights=y))

#~~~~~~ 2D plot ~~~~~~
def extract_2d(fname):
	data=[]
	with open(fname,'r',encoding = "ISO-8859-1") as f:
		for line in f:
			line=line.split()
			try :
				row=[float(elem) for elem in line]
				data+=[row]
			except :
				pass
	return(np.array(data))

def print_map(array,xmin=0,xmax=1,ymin=0,ymax=1):
	xsize=len(array[:,0])
	ysize=len(array[0,:])
	arrayToPlot=np.zeros((xsize+1,ysize+1))
	for i in range(xsize):
		for j in range(ysize):
			arrayToPlot[i,j]=array[i,j]
	x_axis=np.linspace(xmin,xmax,xsize+1)
	y_axis=np.linspace(ymin,ymax,ysize+1)
	fig,ax=plt.subplots()
	c=ax.pcolormesh(x_axis, y_axis, arrayToPlot.T)
	cb=fig.colorbar(c,ax=ax)
	plt.show()

#~~~~~~ Présentation ~~~~~~

def ecris_gros():
	plt.figure(num=1,figsize=(9,6),dpi=80) #à écrire au début a priori


	ax=plt.gca()
	ax.tick_params(labelsize=20)
	ax.set_xlabel(r'B $\parallel$[100] (G)',fontsize=20,fontweight='bold')
	ax.set_ylabel(r'Photoluminescence' ,fontsize=20,fontweight='bold')
	plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2)

def ask_name():
	qapp = QApplication(sys.argv)
	fname,filters=QFileDialog.getOpenFileName()	
	return fname

# x,y=extract_data('ESR 100 2V')
# x=x*1000
# cs=[2765,3020]
# plt.plot(x,y)
# popt,yfit=find_nearest_ESR(x,y,cs)
# print(popt)
# plt.plot(x,yfit)
# plt.show()