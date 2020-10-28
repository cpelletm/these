import numpy as np
from numpy import cos,sin,tan,arccos,arcsin,arctan,exp,sqrt,pi
from numpy.linalg import norm
import matplotlib.pyplot as plt
from qutip import *
import scipy.optimize
from tabulate import tabulate


Sz=np.array([[1,0,0],[0,0,0],[0,0,-1]])
Sx=1/sqrt(2)*np.array([[0,1,0],[1,0,1],[0,1,0]])
Sy=1/(sqrt(2)*1j)*np.array([[0,1,0],[-1,0,1],[0,-1,0]])

c1=np.array([-1,1.,-1])/np.sqrt(3)
c2=np.array([1,1,1])/np.sqrt(3)
c3=np.array([-1,-1,1])/np.sqrt(3)
c4=np.array([1,-1,-1])/np.sqrt(3)

carb=[c1,c2,c3,c4]

def Hamiltonian_base_labo(B,c,E=3,D=2870,gamma=2.8) :
	Bz=c.dot(B)
	Bx=np.sqrt(max(sum(x**2 for x in B)-Bz**2,0))
	H=D*Sz**2+gamma*(Bx*Sx+Bz*Sz)+E*(Sx.dot(Sx)-Sy.dot(Sy))
	return(H)

def transitions(B) :
	egv=[]
	for c in carb :
		H=Hamiltonian_base_labo(B,c)
		egva,egve=np.linalg.eigh(H)
		egva=np.sort(egva)
		egv+=[egva[1]-egva[0]]
		egv+=[egva[2]-egva[0]]
	return np.sort(np.array(egv))

def Hamiltonian_NV_propre_base(B,E=3,D=2870,gamma=2.8) :
	#Unité naturelle : MHz,Gauss
	B=np.array(B)
	H=D*Sz**2+gamma*(B[0]*Sx+B[1]*Sy+B[2]*Sz)+E*(Sx.dot(Sx)-Sy.dot(Sy))
	return H

def egvect(H) :
	val,vec=np.linalg.eigh(H) #H doit être Hermitienne
	val=np.sort(val)
	vec=vec.T #Les vecteurs propres sortent en LIGNE (vecteur #1 : vec[0])
	return(val,vec)

def make_collapse_list(gamma_las,gamma_t1) :
	col=[]
	for i in range(3) :
		for j in range(3) :
			if i!=j :
				single=np.zeros((3,3))
				single[i,j]=sqrt(gamma_t1)
				col+=[Qobj(single)]
	las=np.zeros((3,3))
	las[1,0]=sqrt(gamma_las)
	col+=[Qobj(las)]
	las=np.zeros((3,3))
	las[1,2]=sqrt(gamma_las)
	col+=[Qobj(las)]
	return col

def steady_dm(H,gamma_las,gamma_t1):
	H=Qobj(H)
	dm=steadystate(H,make_collapse_list(gamma_las,gamma_t1))
	rho=np.array(dm)
	return(rho)

def spin_avg(rho):
	s=np.array([np.trace(rho.dot(Sx)),np.trace(rho.dot(Sy)),np.trace(rho.dot(Sz))])
	return(s.real)

def spin_3vx_4classes(B,gamma_las,gamma_t1):
	B=np.array(B)
	Rzplus=np.array([[sqrt(1/2),sqrt(1/2),0],[-sqrt(1/2),sqrt(1/2),0],[0,0,1]])
	Rzmoins=np.array([[sqrt(1/2),-sqrt(1/2),0],[sqrt(1/2),sqrt(1/2),0],[0,0,1]])

	Rxplus=np.array([[1,0,0],[0,sqrt(1/3),sqrt(2/3)],[0,-sqrt(2/3),sqrt(1/3)]])
	Rxmoins=np.array([[1,0,0],[0,sqrt(1/3),-sqrt(2/3)],[0,sqrt(2/3),sqrt(1/3)]])

	Ryplus=np.array([[sqrt(1/3),0,sqrt(2/3)],[0,1,0],[-sqrt(2/3),0,sqrt(1/3)]])
	Rymoins=np.array([[sqrt(1/3),0,-sqrt(2/3)],[0,1,0],[sqrt(2/3),0,sqrt(1/3)]])


	Raller=[Rymoins.dot(Rzplus),Ryplus.dot(Rzplus),Rxplus.dot(Rzplus),Rxmoins.dot(Rzplus)]
	Rretour=[Rzmoins.dot(Ryplus),Rzmoins.dot(Rymoins),Rzmoins.dot(Rxmoins),Rzmoins.dot(Rxplus)]

	spin=np.zeros(3)
	rho_0=0
	for k in range(4) :
		B_base=Raller[k].dot(B)
		H=Hamiltonian_NV_propre_base(B_base)
		rho=steady_dm(H,gamma_las,gamma_t1[k])
		rho_0+=rho[1,1]
		spin_base=spin_avg(rho)
		spin+=Rretour[k].dot(spin_base)
	return(spin,rho_0)	

def make_t1_list(B,gamma_t1_CR=1E-3,gamma_t1_base=1E-3,width=8): #gamma_t1=1,3,5,7 KHz pour deg=1,2,3,4
	B=np.array(B)
	Rzplus=np.array([[sqrt(1/2),sqrt(1/2),0],[-sqrt(1/2),sqrt(1/2),0],[0,0,1]])
	Rzmoins=np.array([[sqrt(1/2),-sqrt(1/2),0],[sqrt(1/2),sqrt(1/2),0],[0,0,1]])

	Rxplus=np.array([[1,0,0],[0,sqrt(1/3),sqrt(2/3)],[0,-sqrt(2/3),sqrt(1/3)]])
	Rxmoins=np.array([[1,0,0],[0,sqrt(1/3),-sqrt(2/3)],[0,sqrt(2/3),sqrt(1/3)]])

	Ryplus=np.array([[sqrt(1/3),0,sqrt(2/3)],[0,1,0],[-sqrt(2/3),0,sqrt(1/3)]])
	Rymoins=np.array([[sqrt(1/3),0,-sqrt(2/3)],[0,1,0],[sqrt(2/3),0,sqrt(1/3)]])

	Raller=[Rymoins.dot(Rzplus),Ryplus.dot(Rzplus),Rxplus.dot(Rzplus),Rxmoins.dot(Rzplus)]
	Rretour=[Rzmoins.dot(Ryplus),Rzmoins.dot(Rymoins),Rzmoins.dot(Rxmoins),Rzmoins.dot(Rxplus)]

	transis=np.zeros((2,4))
	for k in range(4) :
		B_base=Raller[k].dot(B)
		H=Hamiltonian_NV_propre_base(B_base)
		val,vect=egvect(H)
		transis[0,k]=val[1]-val[0]
		transis[1,k]=val[2]-val[0]
	gamma_t1=np.ones(4)*gamma_t1_base
	for i in range(3):
		for j in range(i+1,4):
			for k in range(2):
				gamma_t1[i]+=gamma_t1_CR*1/(1+((transis[k,i]-transis[k,j])**2)/width**2)
				gamma_t1[j]+=gamma_t1_CR*1/(1+((transis[k,i]-transis[k,j])**2)/width**2)
	return(gamma_t1)


def plot_canevas(ax):
	#Theta en ordonée de 0 a 180 ; phi en abscisse de 0 à 360
	lw1=3
	ls1='-'
	#(100)
	color = next(ax._get_lines.prop_cycler)['color']
	ax.plot([90,90],[0,180],linewidth=lw1,ls=ls1,label=r'Plane $\bot (100)$ ',color=color)
	ax.plot([270,270],[0,180],linewidth=lw1,ls=ls1,color=color)

	#(010)
	ax.plot([180,180],[0,180],linewidth=lw1,ls=ls1,label=r'Plane $\bot (010)$ ',color=color)
	ax.plot([0,0],[0,180],linewidth=lw1/2,ls=ls1,color=color)
	ax.plot([360,360],[0,180],linewidth=lw1/2,ls=ls1,color=color)

	#(001)
	ax.plot([0,360],[90,90],linewidth=lw1,ls=ls1,label=r'Plane $\bot (001)$ ',color=color)

	lw2=2
	ls2='--'


	#(110)
	color = next(ax._get_lines.prop_cycler)['color']
	ax.plot([135,135],[0,180],linewidth=lw2,ls=ls2,label=r'Plane $\bot (110)$ ',color=color)
	ax.plot([315,315],[0,180],linewidth=lw2,ls=ls2,color=color)

	#(1-10)
	ax.plot([45,45],[0,180],linewidth=lw2,ls=ls2,label=r'Plane $\bot (1\bar{1}0)$ ',color=color)
	ax.plot([225,225],[0,180],linewidth=lw2,ls=ls2,color=color)


	phis=np.linspace(0,360,500)
	#(101)
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*cos(phi*pi/180)+cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	ax.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (101)$ ',color=color)

	#(10-1)
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*cos(phi*pi/180)-cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	ax.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (10\bar{1})$ ',color=color)

	#(011)
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*sin(phi*pi/180)+cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	ax.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (011)$ ',color=color)

	#(01-1)
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*sin(phi*pi/180)-cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	ax.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (01\bar{1})$ ',color=color)

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


def cart_to_spher(r):
	x=r[0]
	y=r[1]
	z=r[2]
	xphi=x/np.sqrt(x**2+y**2)
	yphi=y/np.sqrt(x**2+y**2)
	if xphi>-1 :
		phi_r=2*arctan(yphi/(xphi+1))
	else :
		phi_r=pi
	theta_r=arccos(z/np.sqrt(x**2+y**2+z**2))
	if phi_r<0 : #Cartes de 0 à 2pi plutot que de -pi à pi
		phi_r+=2*pi
	return(theta_r,phi_r)

def spher_to_cart(theta,phi):
	return(np.array([sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)]))



n=300
fig,ax=plt.subplots()

B_1=np.array([ 37.0815447 ,  27.17222075, 106.08986284])
B_2=np.array([ 40.35446569, -22.06572528, 129.456638  ])

B_in=B_1+(B_2-B_1)*(-0.02)
B_out=B_1+(B_2-B_1)*0.98

Bxs=np.linspace(B_in[0],B_out[0],n)
Bys=np.linspace(B_in[1],B_out[1],n)
Bzs=np.linspace(B_in[2],B_out[2],n)

def show_map():
	ax=plt.gca()
	plot_canevas(ax)
	for i in range(n):
		theta,phi=cart_to_spher([Bxs[i],Bys[i],Bzs[i]])
		theta=theta*180/np.pi
		phi=phi*180/np.pi
		plt.scatter([phi],[theta],color='red',marker='.')
	# plt.scatter([B1[2],B2[2]],[B1[1],B2[1]])

x0=8
x=np.linspace(0,np.linalg.norm(B_out-B_in),n)-x0



transis=np.zeros((n,4))
for i in range(n):
	B=np.array([Bxs[i],Bys[i],Bzs[i]])
	transis[i,:]=transitions(B)[:4]

color = next(ax._get_lines.prop_cycler)['color']
for j in range(4):
	ax.plot(x,transis[:,j],color=color,ls='--',lw=3)

color = next(ax._get_lines.prop_cycler)['color']

fname='ESR-meca_0.3V'
x,y=extract_data(fname+'.txt')
nmax=len(x)//2
nmin=50
x=x*1000
y=y-min(y)
y=y/max(y)
y=-8*y+40-x0
ax.plot(y[nmin:nmax],x[nmin:nmax],'x',color=color,ms=8,mew=2)

fname='ESR-meca_0.2V'
x,y=extract_data(fname+'.txt')
nmax=len(x)//2
nmin=50
x=x*1000
y=y-min(y)
y=y/max(y)
y=-8*y+25-x0
ax.plot(y[nmin:nmax],x[nmin:nmax],'x',color=color,ms=8,mew=2)


fname='ESR-meca_0.1V'
x,y=extract_data(fname+'.txt')
nmax=len(x)//2
nmin=50
x=x*1000
y=y-min(y)
y=y/max(y)
y=-8*y+10-x0
ax.plot(y[nmin:nmax],x[nmin:nmax],'x',color=color,ms=8,mew=2)

fname='ESR-meca_0.4V'
x,y=extract_data(fname+'.txt')
nmax=len(x)//2
nmin=50
x=x*1000
y=y-min(y)
y=y/max(y)
y=-8*y+55-x0
ax.plot(y[nmin:nmax],x[nmin:nmax],'x',color=color,ms=8,mew=2)

# plt.xlabel(r'$\phi$(°)',fontsize=25)
# 	plt.ylabel(r'$\theta$(°)',fontsize=25)
ax.tick_params(labelsize=20)
# ax.set_xlabel(r'$B_{em}$(G)',fontsize=30)
# ax.set_ylabel(r'Frequency (MHz)',fontsize=30)


plt.show()

# print(transis[n//2,:])
# print(transitions(B0_cart))