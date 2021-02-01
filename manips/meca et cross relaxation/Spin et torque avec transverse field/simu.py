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

h=6.626*1E-34
gamma_e=2.8*1E6 #en Hz/Gauss (Lui c'est juste pour avoir des unités SI à la fin, donc c'est normal qu'il soit en Hz)
gamma_las=5E-3/(2*pi) #le piège classique, mes unités sont en MHz
gamma_t1=1E-3/(2*pi) 

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

amp=100 #G
thetas=np.linspace(0,2*np.pi,200)
spins=[]
torques=[]
for theta in thetas :
	B=np.array([sin(theta),0,cos(theta)])*amp
	H=Hamiltonian_NV_propre_base(B)
	rho=steady_dm(H,gamma_las,gamma_t1)
	spin=spin_avg(rho)
	spins+=[spin]
	torque=np.cross(spin,B)*h*gamma_e
	torques+=[np.linalg.norm(torque)]

spins=np.array(spins)
torques=np.array(torques)

plt.figure(num=1,figsize=(9,6),dpi=80) #à écrire au début a priori
ax=plt.gca()

thetas=thetas*180/pi
# ax.plot(thetas,spins[:,0],linewidth=3,label=r'$\langle S_\perp \rangle$')
# # ax.plot(thetas,spins[:,1])
# ax.plot(thetas,spins[:,2],ls='--',linewidth=3, label=r'$\langle S_\parallel \rangle$')

ax.plot(thetas,torques, lw=3)
ax.set_xlabel(r'$\theta$ (°)',fontsize=20,fontweight='bold')
ax.set_ylabel(r'Torque amplitude' ,fontsize=20,fontweight='bold')
ax.tick_params(labelsize=15)
# ax.legend(fontsize=20)
plt.show()

