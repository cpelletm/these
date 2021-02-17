import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit,root_scalar
from scipy import fftpack
from PyQt5.QtWidgets import QApplication,QFileDialog




def extract_data(filename,xcol=0,ycol=1,exclude_neg=True):
	x=[]
	y=[]
	with open(filename,'r',encoding = "ISO-8859-1") as f:
		for line in f :
			line=line.split()
			try :
				if exclude_neg :
					if float(line[xcol])!=-1 :
						x+=[float(line[xcol])]
						y+=[float(line[ycol])]
				else :
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


def stretch_arb_fit(x,y,Amp=None,ss=None,tau=None,alpha=0.5) :
	if not Amp :
		Amp=max(y)-min(y)
	if not ss :
		ss=y[-1]
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,Amp,ss,tau,alpha) :
		return Amp*np.exp(-(x/tau)**alpha)+ss
	p0=[Amp,ss,tau,alpha]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1],popt[2],popt[3]))


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

def exp_soustraction(x,y,Amp=None,tau=None) :
	if not Amp :
		Amp=max(y)-min(y)
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,Amp,tau) :
		return Amp*np.exp(-(x/tau))
	p0=[Amp,tau]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1]))

def third_stretch(x,y,Amp=None,ss=None,tau=None) :
	if not Amp :
		Amp=max(y)-min(y)
	if not ss :
		ss=y[-1]
	if not tau :
		tau=x[int(len(x)/10)]-x[0]
	def f(x,Amp,ss,tau) :
		return Amp*np.exp(-(x/tau)**(0.3333))+ss
	p0=[Amp,ss,tau]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1],popt[2]))

def stretch_et_phonon(x,y,Amp_stretch=None,Amp_exp=0.1,tau_stretch=None,tau_exp=5e-3) :
	if not Amp_stretch :
		Amp_stretch=max(y)-min(y)
	if not tau_stretch :
		tau_stretch=x[int(len(x)/10)]-x[0]
	def f(x,Amp_stretch,Amp_exp,tau_stretch,tau_exp) :
		return Amp_stretch*np.exp(-np.sqrt(x/tau_stretch))+Amp_exp*np.exp(-(x/tau_exp))
	p0=[Amp_stretch,Amp_exp,tau_stretch,tau_exp]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1],popt[2],popt[3]))

def fit_B_dipole(x,y,B0=2000,x0=10) : #x : distance en mm, y : champ mag en G
	def f(x,B0,x0):
		return(B0/(x+x0)**3)
	p0=[B0,x0]
	popt, pcov = curve_fit(f, x, y, p0)
	return(popt,f(x,popt[0],popt[1]))

def ESR_n_pics(x,y,cs,width=8,ss=None,amp=None) :
	if not ss :
		ss=y[0]
	if not amp :
		if max(y)-ss > ss-min(y) :
			amp=max(y)-ss
		else :
			amp=min(y)-ss
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
			y+=amp*np.exp(-((x-c)/width)**2)
		return(y)
	popt, pcov = curve_fit(f, x, y, p0)
	variables=(x,)
	for p in popt :
		variables+=(p,)
	return(popt,f(*variables))



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

#510=6.85 ; 592=5.77 ; 1020=2.03

xmax=-1

# x,y=extract_data('T1_brut_86uW_0B_long.txt')
# x=x[:xmax]
# y=y[:xmax]
# y=y/max(y)
# plt.plot(x,y,'x',label='OB_ordi2')
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])

# x,y=extract_data('T1_brut_86uW_100_3V_long.txt')
# x=x[:xmax]
# y=y[:xmax]
# y=y-min(y)
# y=y/max(y)
# plt.plot(x,y,'x',label='100_ordi2')
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])


# x,y=extract_data('T1_0B_ordi1.txt')
# y=y-min(y)
# y=y/max(y)
# plt.plot(x,y,'x',label='100_ordi1')

# x,y=extract_data('T1_100_3V_comme_ordi1.txt')
# y=y-min(y)
# y=y/max(y)
# plt.plot(x,y,'x',label='100_ordi2_comme_1')
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])

# x,y=extract_data('T1_sub_0B.txt')
# y=y-min(y)
# y=y/max(y)
# plt.plot(x,y,'x',label='0B_sub')
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])


# x,y=extract_data('T1_sub_100_3V.txt')
# y=y-min(y)
# y=y/max(y)
# plt.plot(x,y,'x',label='100')
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])


# x,y=extract_data('T1_100_sub.txt')
# y=y-min(y)
# y=y/max(y)
# x=x[1:]
# y=y[1:]
# plt.plot(x,y,'o',markerfacecolor="None",label='100')
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])


# x,y=extract_data('T1_sub_0B_le_switch_est_mort.txt')
# y=y-min(y)
# y=y/max(y)
# x=x[1:]
# y=y[1:]
# plt.plot(x,y,'s',markerfacecolor="None",label='0B')
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
# popt,yfit=stretch_arb_fit(x,y)
# plt.plot(x,yfit,label='tau=%f,alpha=%f'%(popt[2],popt[3]))

taux=[]

x,y=extract_data('T1_sub_100_2V_align=0.txt')
y=y-min(y)
y=y/max(y)
x=x[1:]
y=y[1:]
# plt.plot(x,y,'s',markerfacecolor="None",label='100')
popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
taux+=[popt[2]]

x,y=extract_data('T1_sub_100_2V_align=+1.txt')
y=y-min(y)
y=y/max(y)
x=x[1:]
y=y[1:]
# plt.plot(x,y,'s',markerfacecolor="None",label='100+1')
popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
taux+=[popt[2]]

x,y=extract_data('T1_sub_100_2V_align=+2.txt')
y=y-min(y)
y=y/max(y)
x=x[1:]
y=y[1:]
# plt.plot(x,y,'s',markerfacecolor="None",label='100+2')
popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
taux+=[popt[2]]

x,y=extract_data('T1_sub_100_2V_align=+3.txt')
y=y-min(y)
y=y/max(y)
x=x[1:]
y=y[1:]
# plt.plot(x,y,'s',markerfacecolor="None",label='100+3')
popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
taux+=[popt[2]]

x,y=extract_data('T1_sub_100_2V_align=-1.txt')
y=y-min(y)
y=y/max(y)
x=x[1:]
y=y[1:]
# plt.plot(x,y,'s',markerfacecolor="None",label='100-1')
popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
taux+=[popt[2]]

x,y=extract_data('T1_sub_100_2V_align=-2.txt')
y=y-min(y)
y=y/max(y)
x=x[1:]
y=y[1:]
# plt.plot(x,y,'s',markerfacecolor="None",label='100-2')
popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
taux+=[popt[2]]
# popt,yfit=stretch_arb_fit(x,y)
# plt.plot(x,yfit,label='tau=%f,alpha=%f'%(popt[2],popt[3]))

x,y=extract_data('T1_sub_100_2V_align=-3.txt')
y=y-min(y)
y=y/max(y)
x=x[1:]
y=y[1:]
# plt.plot(x,y,'s',markerfacecolor="None",label='100-3')
popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
taux+=[popt[2]]

x,y=extract_data('T1_sub_100_2V_align=-4.txt')
y=y-min(y)
y=y/max(y)
x=x[1:]
y=y[1:]
# plt.plot(x,y,'s',markerfacecolor="None",label='100-3')
popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
taux+=[popt[2]]

x,y=extract_data('T1_sub_100_2V_align=+4.txt')
y=y-min(y)
y=y/max(y)
x=x[1:]
y=y[1:]
# plt.plot(x,y,'s',markerfacecolor="None",label='100-3')
popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
taux+=[popt[2]]

x,y=extract_data('T1_sub_100_2V_align=+5.txt')
y=y-min(y)
y=y/max(y)
x=x[1:]
y=y[1:]
# plt.plot(x,y,'s',markerfacecolor="None",label='100-3')
popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
taux+=[popt[2]]

xs=[0,1,2,3,-1,-2,-3,-4,+4,+5]
taux=np.array(taux)
taux=1/taux
# plt.plot(xs,taux,'s')


# x,y=extract_data('T1_100_sub.txt')
# xmin=0
# xmax=-1
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# y=y/max(y)
# plt.plot(x,y,'x',label='100')
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
# popt,yfit=stretch_soustraction(x,y)
# plt.plot(x,yfit,label='tau=%e'%popt[1])
# popt,yfit=stretch_et_phonon(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[1])
# print(popt)


# x,y=extract_data('T1_sub_0B_weekend.txt')
# xmin=3
# xmax=-1
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# y=y/max(y)
# plt.plot(x,y,'x',label='0B')
# popt,yfit=stretch_soustraction(x,y)
# plt.plot(x,yfit,label='tau=%e'%popt[1])
# popt,yfit=stretch_et_phonon(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[1])
# print(popt)

# x,y=extract_data('T1_100_sub_+2deg.txt')
# y=y-min(y)
# y=y/max(y)
# x=x[1:]
# y=y[1:]
# plt.plot(x,y,'x',label='100')
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])

# x,y=extract_data('T1_1classe_sub_weekend.txt')
# y=y-min(y)
# y=y/max(y)
# plt.plot(x,y,'x',label='100')
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
# popt,yfit=stretch_arb_fit(x,y)
# plt.plot(x,yfit,label='tau=%f,alpha=%f'%(popt[2],popt[3]))

# x,y=extract_data('T1_1classe_brut_10min.txt')
# y=y-min(y)
# y=y/max(y)
# plt.plot(x,y,'x',label='100')
# popt,yfit=exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])

ax=plt.gca()


x,y=extract_data('T1_sub_1111_mieux.txt')
x=x[2:]
y=y[2:]
y=y/max(y)
# plt.plot(x,y,'v',markerfacecolor="None",ms=5,mew=1,label='1 class',color=color)
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2],color=color,lw=2)
# popt,yfit=stretch_et_phonon(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[1])
# print(popt)


def R2(y,yfit):
	avg=np.sum(y)/len(y)
	SStot=sum((y-avg)**2)
	SSres=sum((y-yfit)**2)
	return 1-SSres/SStot

x,y=extract_data('T1_100_sub.txt')
x=x[0:]*1e3
y=y[0:]
y=y/max(y)
plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=1)
popt,yfit=stretch_soustraction(x,y)
print(R2(y,yfit),popt[1])
plt.plot(x,yfit,label='stretch exponential fit',lw=2)
popt,yfit=exp_soustraction(x,y)
print(R2(y,yfit),popt[1])
plt.plot(x,yfit,'--',label='exponential fit',color='red',lw=2)
ax.tick_params(labelsize=12)

# popt,yfit=stretch_soustraction(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[1])
# popt,yfit=stretch_et_phonon(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
# print(popt)

x,y=extract_data('T1_sub_100_long.txt')
y=y/max(y)
x1=x[1:]
y1=y[1:]

# plt.plot(x,y,'x',label='100')
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
# popt,yfit=stretch_soustraction(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[1])
# popt,yfit=stretch_et_phonon(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
# print(popt)

color = next(ax._get_lines.prop_cycler)['color']
x,y=extract_data('T1_sub_100_long_2.txt')
x=x[1:]
y=y[1:]
y=y/max(y)
x=(x+x1)/2
y=(y+y1)/2
# plt.plot(x,y,'o',markerfacecolor="None",ms=5,mew=1,label='4 classes',color=color)
# popt,yfit=stretch_exp_fit(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2],color=color,lw=2)
# popt,yfit=stretch_soustraction(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[1])
# popt,yfit=stretch_et_phonon(x,y)
# plt.plot(x,yfit,label='tau=%f'%popt[2])
# print(popt)

plt.legend()
plt.show()