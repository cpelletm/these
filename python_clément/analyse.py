import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit,root_scalar,minimize
from scipy import fftpack
from PyQt5.QtWidgets import QApplication,QFileDialog




def extract_data(filename,xcol=0,ycol=1,exclude_neg=True,data='line',delimiter='auto'):
	import csv
	if filename[-4]!='.' :
		if glob.glob(filename+'.txt') :
			f=glob.glob(filename+'.txt')[0]
		elif glob.glob(filename+'.csv') :
			f=glob.glob(filename+'.csv')[0]
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
	def f(x,Amp,x0,sigma,ss) : #HWHM=1.18*sigma (sqrt(2*ln(2)))
		return Amp*np.exp(-(x-x0)**2/(2*sigma**2))+ss
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

def exp_fit_zero(x,y,Amp=None,tau=None) :
	if not Amp :
		Amp=max(y)-min(y)
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,Amp,tau) :
		return Amp*np.exp(-x/tau)
	p0=[Amp,tau]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1]))

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
	popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,-np.inf,0],[np.inf,np.inf,np.inf]))
	return(popt,f(x,popt[0],popt[1],popt[2]))

def stretch_exp_fit_zero(x,y,Amp=None,tau=None) :
	if not Amp :
		Amp=max(y)-min(y)
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,Amp,tau) :
		return Amp*np.exp(-np.sqrt(x/tau))
	p0=[Amp,tau]
	popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,0],[np.inf,np.inf]))
	return(popt,f(x,popt[0],popt[1]))

def stretch_arb_exp_fit(x,y,Amp=None,ss=None,tau=None,alpha=0.5,fixed=False):
	if not Amp :
		Amp=max(y)-min(y)
	if not ss :
		ss=y[-1]
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	if fixed :
		def f(x,Amp,ss,tau) :
			return Amp*np.exp(-(x/tau)**alpha)+ss
		p0=[Amp,ss,tau]
		popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,-np.inf,0],[np.inf,np.inf,np.inf]))
	else :
		def f(x,Amp,ss,tau,alpha) :
			return Amp*np.exp(-(x/tau)**alpha)+ss
		p0=[Amp,ss,tau,alpha]
		popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,-np.inf,0,0],[np.inf,np.inf,np.inf,np.inf]))
	return(popt,f(x,*popt))

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

def stretch_et_phonons(x,y,Amp=None,tau=None,ss=None,T1ph=5E-3) :
	if not Amp :
		Amp=max(y)-min(y)
	if not ss :
		ss=y[-1]
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,Amp,ss,tau) :
		return Amp*np.exp(-x/((T1ph*np.sqrt(x*tau))/(T1ph+np.sqrt(x*tau))))+ss
	p0=[Amp,ss,tau]
	popt, pcov = curve_fit(f, x, y, p0,bounds=([-np.inf,-np.inf,0],[np.inf,np.inf,np.inf]))
	return(popt,f(x,popt[0],popt[1],popt[2]))

def Rabi_fit(x,y,Amp=None,omega=None,tau=None,ss=None):
	if not Amp :
		Amp=max(y)-min(y)
	if not ss :
		ss=y[-1]
	if not tau :
		tau=x[int(len(x)/3)]-x[0]
	if not omega :
		omega=1/(x[int(len(x)/10)]-x[0])
	def f(x,Amp,ss,tau,omega) :
		return Amp*np.exp(-x/tau)*np.cos(omega*x)+ss
	p0=[Amp,ss,tau,omega]
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
	widths=popt[n+1:2*n+1]
	amps=popt[2*n+1:]
	params=[ss,centers,widths,amps]
	return(params,f(x,*popt))

def ESR_n_pics_auto(x,y,width=False,ss=None,amp=None,typ='gauss'):
	if not ss :
		ss=y[0]
	if not amp : #Attention sur les noms, cette fonction n'utilise que amps, amp sera directement transmis à ESR_n_pics
		if max(y)-ss > ss-min(y) :
			amp=max(y)-ss
			def extremum(x,y):
				return(x[list(y).index(max(y))])
		else :
			amp=min(y)-ss
			def extremum(x,y):
				return(x[list(y).index(min(y))])
	if not width :
		if max(x) < 50 : #Je sq c'est des GHz
			width=8e-3
		elif max(x) < 5E4 : #Je sq c'es des Mhz
			width=8
		else : #Je sq c'es des Hz
			width=8E6
	OGy=y
	threshold=0.2
	cs=[]
	amps=[]
	cs+=[extremum(x,y)]
	popt,yfit=ESR_n_pics(x,y,[extremum(x,y)])
	amps+=[abs(popt[3])]
	for i in range(100):
		y=y-yfit
		c=extremum(x,y)
		try :
			popt,yfit=ESR_n_pics(x,y,[c])
		except :
			break #Si le truc est trop bizarre il arrive pas à fitter
		if abs(popt[3]) < amps[0]*threshold :
			break
		elif min([abs(c-ci) for ci in cs]) < width/2 : #Si il retrouve un pic trop proche d'un pic précédent il l'enregistre pas
			continue
		else :
			cs+=[c]
			amps+=[abs(popt[3])]
	# return(cs)	
	return(ESR_n_pics(x,OGy,cs=cs,width=width,ss=ss,amp=amp,typ=typ))

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
	D=2873 #Mhz
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
		Bx=np.sqrt(abs(B.amp**2-Bz**2))#le amp est la pour éviter les blagues d'arrondis. Je mets tout ce qui n'est pas sur z sur le x
		self.H=self.D*self.Sz2+self.gamma_e*(Bz*self.Sz+Bx*self.Sx) #Rajoute des fioritures si tu veux
	def transitions(self):
		egva,egve=np.linalg.eigh(self.H)
		egva=np.sort(egva)
		return [egva[1]-egva[0],egva[2]-egva[0]]

class magneticField():
	def __init__(self,x=False,y=False,z=False,theta=False,phi=False,amp=False): #Give either x,y,z or theta,phi,amp (polar/azimutal from the z axis)
		if not x:
			self.x=amp*np.cos(theta)*np.sin(phi)
			self.y=amp*np.sin(theta)*np.sin(phi)
			self.z=amp*np.cos(phi)
			self.theta=theta
			self.phi=phi
			self.amp=amp
		elif not theta :
			self.amp=np.sqrt(x**2+y**2+z**2)
			self.theta=np.arccos(z/self.amp)
			self.phi=np.arctan2(y,x)
			self.x=x
			self.y=y
			self.z=z
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

def find_B_spherical(peaks,Bmax=1000): #B in gauss
	peaks=np.sort(peaks)
	if len(peaks)==8 :
		def err_func(B,peaks): #B is given in the form [amp,theta,phi]
			B=magneticField(amp=B[0],theta=B[1],phi=B[2])
			simuPeaks=B.transitions4Classes()
			err=np.linalg.norm(peaks-simuPeaks)
			return err
	elif len(peaks)==2:
		def err_func(B,peaks): #B is given in the form [amp,theta,phi]
			B=magneticField(amp=B[0],theta=B[1],phi=B[2])
			simuPeaks=B.transitions4Classes()
			completePeaks=np.sort([peaks[0]]*4+[peaks[1]]*4)
			err=np.linalg.norm(completePeaks-simuPeaks)
			return err
	elif len(peaks)==4: #Merde y'a le cas de la 111
		print('not implemented yet')
	sol=minimize(err_func,x0=[100,0.4777,0.3927],args=peaks,bounds=[(0,Bmax),(-0.05,0.9554),(-0.05,0.7854)]) #c'est équivalent à un rectangle dans [0,54.74]x[0,45] deg
	return magneticField(amp=sol.x[0],theta=sol.x[1],phi=sol.x[2])

def find_B_cartesian(peaks,Bmax=1000): #B in gauss ; Ca m'a la'ir de moins bien marcher que l'autre
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
	elif len(peaks)==4: #Merde y'a le cas de la 111
		print('not implemented yet')
	sol=minimize(err_func,x0=[0,0,0],args=peaks,bounds=[(-Bmax,Bmax),(-Bmax,Bmax),(-Bmax,Bmax)]) #c'est équivalent à un rectangle dans [0,54.74]x[0,45] deg
	return magneticField(amp=sol.x[0],theta=sol.x[1],phi=sol.x[2])

# peaks=[2626,2702,2805,2867,2989,3042,3115,3160]
# print(find_B_spherical(peaks))
# print(find_B_spherical(peaks).transitions4Classes())

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

def find_nearest_ESR(x,y,peaks,Bmax=1000,typ='gauss',TrueAngles=False): #peaks : centers of resonances in MHz
	popt,yfit= ESR_n_pics(x,y,peaks)
	n=len(peaks)
	ss=popt[0]
	peaks=popt[1:n+1]
	widths=popt[n+1:2*n+1]
	amps=popt[2*n+1:]
	B=find_B_spherical(peaks,Bmax=Bmax)
	cs=B.transitions4Classes()
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
	if TrueAngles :
		popt=[B.amp,B.theta,B.phi]
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
	x_axis=np.linspace(xmin,xmax,len(array[0,:]))
	y_axis=np.linspace(ymin,ymax,len(array[:,0]))
	fig,ax=plt.subplots()
	c=ax.pcolormesh(x_axis, y_axis, array)
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