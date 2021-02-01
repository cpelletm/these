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

def Hamiltonian_NV_propre_base(B,E=3,D=2870,gamma=2.8) :
	#Unité naturelle : MHz,Gauss
	B=np.array(B)
	H=D*Sz**2+gamma*(B[0]*Sx+B[1]*Sy+B[2]*Sz)+E*(Sx.dot(Sx)-Sy.dot(Sy))
	return H

def egvect(H) :
	val,vec=np.linalg.eigh(H) #H doit être Hermitienne
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


	R=Rxplus.dot(Rzplus)
	Raller=[Rymoins.dot(Rzplus),Ryplus.dot(Rzplus),Rxplus.dot(Rzplus),Rxmoins.dot(Rzplus)]
	Rretour=[Rzmoins.dot(Ryplus),Rzmoins.dot(Rymoins),Rzmoins.dot(Rxmoins),Rzmoins.dot(Rxplus)]

	spin=np.zeros(3)
	for k in range(4) :
		B_base=Raller[k].dot(B)
		H=Hamiltonian_NV_propre_base(B)
		rho=steady_dm(H,gamma_las,gamma_t1)
		spin_base=spin_avg(rho)
		spin+=Rretour[k].dot(spin_base)
	return(spin)	

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


def plot_canevas(ax):

	#Theta en ordonée de 0 a 180 ; phi en abscisse de 0 à 360
	lw1=3
	ls1='-'
	#(100)
	color = next(ax._get_lines.prop_cycler)['color']
	ax.plot([90,90],[0,180],linewidth=lw1,ls=ls1,label=r'Plane $\bot (100)$ ',color=color)
	ax.plot([270,270],[0,180],linewidth=lw1,ls=ls1,color=color)

	#(010)
	color = next(ax._get_lines.prop_cycler)['color']
	ax.plot([180,180],[0,180],linewidth=lw1,ls=ls1,label=r'Plane $\bot (010)$ ',color=color)
	ax.plot([0,0],[0,180],linewidth=lw1/2,ls=ls1,color=color)
	ax.plot([360,360],[0,180],linewidth=lw1/2,ls=ls1,color=color)

	#(001)
	color = next(ax._get_lines.prop_cycler)['color']
	ax.plot([0,360],[90,90],linewidth=lw1,ls=ls1,label=r'Plane $\bot (001)$ ',color=color)

	lw2=2
	ls2='--'


	#(110)
	color = next(ax._get_lines.prop_cycler)['color']
	ax.plot([135,135],[0,180],linewidth=lw2,ls=ls2,label=r'Plane $\bot (110)$ ',color=color)
	ax.plot([315,315],[0,180],linewidth=lw2,ls=ls2,color=color)

	#(1-10)
	color = next(ax._get_lines.prop_cycler)['color']
	ax.plot([45,45],[0,180],linewidth=lw2,ls=ls2,label=r'Plane $\bot (1\bar{1}0)$ ',color=color)
	ax.plot([225,225],[0,180],linewidth=lw2,ls=ls2,color=color)


	phis=np.linspace(0,360,500)
	#(101)
	color = next(ax._get_lines.prop_cycler)['color']
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*cos(phi*pi/180)+cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	ax.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (101)$ ',color=color)

	#(10-1)
	color = next(ax._get_lines.prop_cycler)['color']
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*cos(phi*pi/180)-cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	ax.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (10\bar{1})$ ',color=color)

	#(011)
	color = next(ax._get_lines.prop_cycler)['color']
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*sin(phi*pi/180)+cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	ax.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (011)$ ',color=color)

	#(01-1)
	color = next(ax._get_lines.prop_cycler)['color']
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*sin(phi*pi/180)-cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	ax.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (01\bar{1})$ ',color=color)


	# ax.plot(phis,90+45*cos(pi/180*phis)) #Pour les mauvaises langues qui disent que ça sert à rien

	#Particular directions
	ax.scatter([0,180,360],[90,90,90],s=80,facecolors='red',edgecolors='red',label=r'$(100)$ direction',zorder=10)
	theta_111=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*np.sqrt(2)/2-cos(theta*pi/180),bracket=[0,180]).root
	ax.scatter([45,225],[theta_111,180-theta_111], marker='s',s=80,facecolors='g',edgecolors='g',label=r'$(111)$ direction',zorder=10)




	ax.set_xlabel(r'$\phi$(°)',fontsize=25)
	ax.set_ylabel(r'$\theta$(°)',fontsize=25)
	ax.tick_params(labelsize='large')

fig,ax=plt.subplots()
plot_canevas(ax)

theta_111=arctan(sqrt(2))


B_in=np.array([77.05651621, 28.6554855 , 82.52557109])
B_out=np.array([ 26.79109384,  50.35396382, 115.30922273])
n=10
Bxs=np.linspace(B_in[0],B_out[0],n)
Bys=np.linspace(B_in[1],B_out[1],n)
Bzs=np.linspace(B_in[2],B_out[2],n)
thetas=[]
phis=[]
for i in range(n):
	B=[Bxs[i],Bys[i],Bzs[i]]
	theta,phi=cart_to_spher(B)
	theta=theta*180/pi
	phi=phi*180/pi
	thetas+=[theta]
	phis+=[phi]
ax.scatter(phis,thetas,s=15,facecolors='blue',edgecolors='blue',zorder=10)
plt.show()