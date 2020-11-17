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

def spin_3vx_1classe(B,gamma_las,gamma_t1,classe=0):
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
	k=classe
	B_base=Raller[k].dot(B)
	H=Hamiltonian_NV_propre_base(B_base)
	rho=steady_dm(H,gamma_las,gamma_t1[k])
	rho_0+=rho[1,1]
	spin_base=spin_avg(rho)
	spin+=Rretour[k].dot(spin_base)
	return(spin,rho_0)	

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

gamma_las=5E-3


def vector_field_NV_4_classes(amp,thetas,phis):
	nthetas=len(thetas)
	nphis=len(phis)
	Fs_theta=np.zeros((nthetas,nphis))
	Fs_phi=np.zeros((nthetas,nphis))
	for t in range(nthetas) :
		theta=thetas[t]
		for p in range(nphis):
			phi=phis[p]
			r=np.array([sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)])
			B=r*amp
			H=Hamiltonian_NV_propre_base(B)
			# gamma_t1=np.ones(4)*1E-3
			# s0,rho_0=spin_1vx_4classes(B,gamma_las,gamma_t1)
			# gamma_t1=make_t1_list(B)
			# s1,rho_0=spin_3vx_4classes(B,gamma_las,gamma_t1)
			gamma_t1=np.ones(4)*1E-3
			s2,rho_0=spin_3vx_4classes(B,gamma_las,gamma_t1)
			s=s0
			# torque=np.cross(s,r)
			# F=np.cross(torque,r)
			# theta_f,phi_f=cart_to_spher(r+F*0.01)
			theta_f,phi_f=cart_to_spher(r+s*0.01) # 0.01 parce qu'il faut une petite variation pour avoir un vecteur précis
			Fs_theta[t,p]=theta_f-theta
			Fs_phi[t,p]=phi_f-phi
		print('ligne %i sur %i'%(t,nthetas))
	fig,ax=plt.subplots()
	q=ax.quiver(phis*180/pi,thetas*180/pi,Fs_phi,Fs_theta)
	ax.set_xlabel(r'$\phi$ (°)')
	ax.set_ylabel(r'$\theta$ (°)')
	ax.set_title('Torque map for B=%iG'%amp)
	plt.show()
	# plt.savefig('map torque/map_%iG.png'%amp)

def torque_amplitude_map(amp,thetas,phis):
	nthetas=len(thetas)
	nphis=len(phis)
	Gammas=np.zeros((nthetas,nphis))
	for t in range(nthetas) :
		theta=thetas[t]
		for p in range(nphis):
			phi=phis[p]
			r=np.array([sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)])
			B=r*amp
			H=Hamiltonian_NV_propre_base(B)
			# gamma_t1=np.ones(4)*1E-3 #Sans CR
			gamma_t1=make_t1_list(B) #Avec CR
			# s,rho_0=spin_3vx_1classe(B,gamma_las,gamma_t1,classe=0)
			s,rho_0=spin_3vx_4classes(B,gamma_las,gamma_t1)
			torque=np.cross(s,B)*h*gamma_e#*2.5E8

			Gammas[t,p]=np.linalg.norm(torque)
		print('ligne %i sur %i'%(t,nthetas))
	fig,ax=plt.subplots()
	c=ax.pcolormesh(phis*180/pi, thetas*180/pi, Gammas, cmap='plasma')
	cb=fig.colorbar(c,ax=ax)
	cb.ax.tick_params(labelsize=15)
	t = cb.ax.yaxis.get_offset_text()
	t.set_size(15)
	ax.set_xlabel(r'$\phi$ (°)',fontsize=20,fontweight='bold')
	ax.set_ylabel(r'$\theta$ (°)',fontsize=20,fontweight='bold')
	ax.tick_params(labelsize=15)
	# ax.set_title('Torque map for B=%iG'%amp)
	plt.show()

# for amp in np.arange(100,2100,100):
# 	vector_field_NV_4_classes(amp)
# 	print(amp)

h=6.626*1E-34
gamma_e=2.8*1E6 #en Hz/Gauss
n_NV=1E-6 #Densité de NV, je divise par 4 ici donc c'est bien la densité d'une classe
m_C=2E-26 #poids d'un atome de carbone
omega_T=2*np.pi*1000 #fréquence du piège
r=7.5E-6



thetas=np.linspace(0,pi,181)
phis=np.linspace(0,2*pi,361)
torque_amplitude_map(500,thetas,phis)