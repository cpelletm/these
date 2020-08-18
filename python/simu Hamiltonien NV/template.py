import numpy as np
from numpy import cos,sin,tan,arccos,arcsin,arctan,exp,sqrt,pi
from numpy.linalg import norm
import matplotlib.pyplot as plt
from qutip import *
import scipy.optimize
from scipy.integrate import quad, dblquad, nquad
from scipy.optimize import root_scalar
from tabulate import tabulate


# theta=2*arccos(sqrt(1/3))
# theta=2*arcsin(sqrt(2/3))
# theta=2*arctan(sqrt(2))

Sz=np.array([[1,0,0],[0,0,0],[0,0,-1]])
bnamez=['+1','0','-1']
bname_undemi=['+1/2','-1/2']
bname_troisdemi=['+3/2','+1/2','-1/2','-3/2']
Sx=1/sqrt(2)*np.array([[0,1,0],[1,0,1],[0,1,0]])
Sy=1/(sqrt(2)*1j)*np.array([[0,1,0],[-1,0,1],[0,-1,0]])
rho_0=np.array([[0,0,0],[0,1,0],[0,0,0]])
rho_s=1./3*np.array([[1,0,0],[0,1,0],[0,0,1]])


Sx_12=1/2*np.array([[0,1],[1,0]])
Sy_12=1/2*np.array([[0,0-1j],[0+1j,0]])
Sz_12=1/2*np.array([[1,0],[0,-1]])

Sx_32=1/2*np.array([[0,sqrt(3),0,0],[sqrt(3),0,2,0],[0,2,0,sqrt(3)],[0,0,sqrt(3),0]])
Sy_32=1/2j*np.array([[0,sqrt(3),0,0],[-sqrt(3),0,2,0],[0,-2,0,sqrt(3)],[0,0,-sqrt(3),0]])
Sz_32=np.array([[3/2,0,0,0],[0,1/2,0,0],[0,0,-1/2,0],[0,0,0,-3/2]])

## Collaposologie
col_t1=np.array([[0,1,1],[1,0,1],[1,1,0]])
gamma_phonon=2E-4#5ms en unité MHz
col_laser=np.array([[0,0,0],[1,0,1],[0,0,0]])
gamma_las=1E-3 #Idem que l'autre

def ordre_numpy() : #Les matrices sont à rentrer ligne par ligne
	testM=np.array([[0,0,1],[0,0,0],[0,0,0]])
	testV=np.array([1,2,3])
	testV=testV.T #n'a pas d'influence

	print(testM.dot(testV)) #M.V
	print(testV.dot(testM)) #V.M

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

def print_matrix(M,bname) :
	headers=['']+['|'+name+'>' for name in bname]
	table=[]
	for i in range(len(bname)) :
		line=[]
		line+=['<'+bname[i]+'|']
		values=list(M[:,i])
		line+=values
		table+=[line]
	print(tabulate(table,headers))

def print_vector(v,bname) :
	table=[]
	for i in range(len(v)) :
		line=['%f+%fj'%(v[i].real,v[i].imag),bname[i]]
		table+=[line]
	print(tabulate(table))

def convolution(M1,M2):
	l1=len(M1[:,0])
	l2=len(M2[:,0])
	l=l1*l2
	M=np.zeros((l,l),dtype=complex)
	for i1 in range(l1) :
		for j1 in range(l1) :
			for i2 in range(l2) :
				for j2 in range(l2) :
					i=i1*l2+i2
					j=j1*l2+j2
					M[i,j]=M1[i1,j1]*M2[i2,j2]
	return(M)


def convolution_et_base(M1,M2,bname1,bname2) :
	bname=[]
	for name1 in bname1 :
		for name2 in bname2 :
			bname+=[name1+name2]
	l1=len(M1[:,0])
	l2=len(M2[:,0])
	l=l1*l2
	M=np.zeros((l,l),dtype=complex)
	for i1 in range(l1) :
		for j1 in range(l1) :
			for i2 in range(l2) :
				for j2 in range(l2) :
					i=i1*l2+i2
					j=j1*l2+j2
					M[i,j]=M1[i1,j1]*M2[i2,j2]
	return(M,bname)

def carbon_13(B=[50,0,0],show=True,classe=1):
	C13=True
	H_NV,bname=convolution_et_base(Hamiltonian_0(B,E=3,classe=classe),np.identity(2),bnamez,bname_undemi)
	Ix=1/2*np.array([[0,1],[1,0]])
	Iy=1/2*np.array([[0,0+1j],[0-1j,0]])
	Iz=1/2*np.array([[1,0],[0,-1]])
	gamma_C13=1.07*1e-3
	Axx=190.2
	Ayy=120.3
	Azz=129.1
	Axz=-25
	H_zeeman_nucl=gamma_C13*np.linalg.norm(B)*Iz
	H_nucl=convolution(np.identity(3),H_zeeman_nucl)
	H_dip=Axx*convolution(Sx,Ix)+Ayy*convolution(Sy,Iy)+Azz*convolution(Sz,Iz)+Axz*(convolution(Sx,Iz)+convolution(Sz,Ix))
	H=H_NV+(H_nucl+H_dip)*C13
	val,vec=egvect(H)

	if show :
		print_matrix(H,bname)	
		show_vpropres(val,vec,bname)
		Sx_c13=convolution(Sx,np.identity(2))
		rho0_c13=convolution(rho_0,np.identity(2))
		transitions(val,vec,Sx_c13,rho0_c13)
	else : 
		return(val,vec)

def show_vpropres(val,vec,bname):
	for i in range(len(val)):
		print('Vecteur %i : Vpropre=%f'%(i,val[i]))
		print_vector(vec[i],bname)

def transitions(val,vec,Sx,rho_0,show=True):
	n=len(val)
	transi=[]
	for i in range(1,len(val)):
		for j in range(i) :
			valt=abs(val[i]-val[j])
			pop_0_1=abs(vec[i].dot(rho_0.dot(vec[i])))
			pop_0_2=abs(vec[j].dot(rho_0.dot(vec[j])))
			contraste=abs(vec[i].dot(Sx.dot(vec[j]))*(pop_0_1-pop_0_2)) #Le contratse prend en compte le couplage par la micro onde et la différence de population dans 0 entre les deux états
			transi+=[[valt,contraste,i,j]]
	transi=sorted(transi,key=lambda x:x[1],reverse=True)
	transi=np.array(transi)
	if show :
		headers=['Transition (MHz)','Probability','vecteur 1', 'vecteur 2']
		print(tabulate(transi,headers))
	else :
		return transi



def NV_simple(orientation='111'):

	# B=[5000,0,0]
	# H=Hamiltonian_0(B,classe=1,E=3)
	# val,vec=egvect(H)
	# show_vpropres(val,vec,bnamez)
	# transitions(val,vec,Sx,rho_0)
	if orientation=='111' :
		amps=np.linspace(0,200,100)
		transi_NV=[]
		for amp in amps :
			# B=[amp,0,0]
			B=[amp/sqrt(3),amp/sqrt(3),amp/sqrt(3)]
			H=Hamiltonian_0(B,classe=1,E=3)
			val,vec=egvect(H)
			transi_NV+=[[val[2]-val[0],val[1]-val[0]]]
		transi_NV=np.array(transi_NV)
		ax=plt.gca()
		color = next(ax._get_lines.prop_cycler)['color']
		plt.plot(amps,transi_NV[:,0],color=color)
		plt.plot(amps,transi_NV[:,1],color=color)
		transi_NV=[]
		for amp in amps :
			# B=[amp,0,0]
			B=[amp/sqrt(3),amp/sqrt(3),amp/sqrt(3)]
			H=Hamiltonian_0(B,classe=2,E=3)
			val,vec=egvect(H)
			transi_NV+=[[val[2]-val[0],val[1]-val[0]]]
		transi_NV=np.array(transi_NV)
		ax=plt.gca()
		color = next(ax._get_lines.prop_cycler)['color']
		plt.plot(amps,transi_NV[:,0],color=color)
		plt.plot(amps,transi_NV[:,1],color=color)
		plt.show()
	if orientation=='100' :
		amps=np.linspace(0,200,100)
		transi_NV=[]
		for amp in amps :
			B=[amp,0,0]
			H=Hamiltonian_0(B,classe=1,E=3)
			val,vec=egvect(H)
			transi_NV+=[[val[2]-val[0],val[1]-val[0]]]
		transi_NV=np.array(transi_NV)
		ax=plt.gca()
		color = next(ax._get_lines.prop_cycler)['color']
		plt.plot(amps,transi_NV[:,0],color=color,label='NV-')
		plt.plot(amps,transi_NV[:,1],color=color)
		transi_NV=[]
		for amp in amps :
			B=[amp,0,0]
			H=Hamiltonian_0(B,classe=1,E=3,D=2706)
			val,vec=egvect(H)
			transi_NV+=[[val[2]-val[0],val[1]-val[0]]]
		transi_NV=np.array(transi_NV)
		ax=plt.gca()
		color = next(ax._get_lines.prop_cycler)['color']
		plt.plot(amps,transi_NV[:,0],color=color,label='VH-')
		plt.plot(amps,transi_NV[:,1],color=color)
		def zero():
			def f(amp):
				B=[amp,0,0]
				H=Hamiltonian_0(B,classe=1,E=3,D=2870)
				val,vec=egvect(H)
				transi_NV=[val[2]-val[0],val[1]-val[0]]
				H=Hamiltonian_0(B,classe=1,E=3,D=2706)
				val,vec=egvect(H)
				transi_VH=[val[2]-val[0],val[1]-val[0]]
				return transi_VH[0]-transi_NV[1]
			RR=root_scalar(f,bracket=[0,100])
			if RR.converged :
				amp=RR.root
				B=[amp,0,0]
				H=Hamiltonian_0(B,classe=1,E=3)
				val,vec=egvect(H)
				transi=[val[2]-val[0],val[1]-val[0]]
				transi_NV=transi[1]
				return amp,transi_NV
			else :
				return False
		x_VH,y_VH=zero()
		color = next(ax._get_lines.prop_cycler)['color']
		plt.scatter(x_VH,y_VH,s=80,facecolors='none',edgecolors=color,label='cross relaxation')		
		plt.legend()
		ylim=ax.get_ylim()
		plt.plot([x_VH,x_VH],[y_VH,0],'--',color=color)
		ax.set_ylim(ylim)
		plt.xlabel(r'B$\parallel$(100) (G)')
		plt.ylabel('Transition frequency (MHz)')
		plt.legend()
		plt.show()




def egv_C13(): #Les 4 croisements sont à : 17.96 G, 19.70 G, 22.11 G, 24.31 G 
	amps=np.linspace(0,100,100)
	transi=[]
	transi_NV=[]
	for amp in amps :
		B=[amp,0,0]
		val,vec=carbon_13(B,show=False)
		transi+=[[val[4]-val[0],val[2]-val[1],val[5]-val[1],val[4]-val[1],val[5]-val[0],val[3]-val[0],val[2]-val[0],val[3]-val[1]]]
		H=Hamiltonian_0(B,classe=1,E=3)
		val,vec=egvect(H)
		transi_NV+=[[val[2]-val[0],val[1]-val[0]]]
	transi=np.array(transi)
	transi_NV=np.array(transi_NV)
	ax=plt.gca()
	color = next(ax._get_lines.prop_cycler)['color']
	for i in range(len(transi[0,:])) :
		if i==0 :
			plt.plot(amps,transi[:,i],'--',color=color,label='NV with 13C first shell')
		else :
			plt.plot(amps,transi[:,i],'--',color=color)
	color = next(ax._get_lines.prop_cycler)['color']
	for i in range(len(transi_NV[0,:])) :
		if i==0 :
			plt.plot(amps,transi_NV[:,i],color=color,label='isolated NV')
		else :
			plt.plot(amps,transi_NV[:,i],color=color)
	def zero(i,j):
		def f(amp):
			B=[amp,0,0]
			val,vec=carbon_13(B,show=False)
			transi=[val[2]-val[0],val[2]-val[1],val[3]-val[0],val[3]-val[1],val[4]-val[0],val[4]-val[1],val[5]-val[0],val[5]-val[1]]
			transi_fs=transi[i]
			H=Hamiltonian_0(B,classe=1,E=3)
			val,vec=egvect(H)
			transi=[val[2]-val[0],val[1]-val[0]]
			transi_NV=transi[j]
			return transi_fs-transi_NV
		RR=root_scalar(f,bracket=[0,50])
		if RR.converged :
			amp=RR.root
			B=[amp,0,0]
			H=Hamiltonian_0(B,classe=1,E=3)
			val,vec=egvect(H)
			transi=[val[2]-val[0],val[1]-val[0]]
			transi_NV=transi[j]
			return amp,transi_NV
		else :
			return False

	zero_pairs=[[2,1],[3,1],[4,0],[5,0]]
	x_transi=[]
	y_transi=[]
	for pair in zero_pairs :
		x,y=zero(pair[0],pair[1])
		x_transi+=[x]
		y_transi+=[y]
	print(x_transi)
	print(y_transi)

	color = next(ax._get_lines.prop_cycler)['color']
	plt.scatter(x_transi,y_transi,s=80,facecolors='none',edgecolors=color,label='cross relaxation')		
	plt.legend()
	ylim=ax.get_ylim()
	for i in range(len(x_transi)) :
		x0=x_transi[i]
		y0=y_transi[i]
		plt.plot([x0,x0],[y0,0],'--',color=color)
	ax.set_ylim(ylim)
	plt.xlabel(r'B$\parallel$(100) (G)')
	plt.ylabel('Transition frequency (MHz)')
	plt.show()

# egv_C13()


def p1(): #le soucis pour la 111 c'est que il y a 6 transitions de NV possibles (et 15*2 de P1...). Pour l'instant j'ai pas tout pris en compte.


	def Ham_p1(B,classe=1):
		B=np.array(B)
		gamma=2.8
		gamma_14N=3.07*1E-4
		Axx=81
		Ayy=Axx
		Azz=114
		Q14N=-3.97
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
		H=convolution(Sz_12,np.identity(3))*gamma*Bz+convolution(Sx_12,np.identity(3))*gamma*Bx
		H+=-(convolution(np.identity(2),Sz)*gamma_14N*Bz+convolution(np.identity(2),Sx)*gamma_14N*Bx) #Pourquoi "-" ?
		H+=Axx*convolution(Sx_12,Sx)+Ayy*convolution(Sy_12,Sy)+Azz*convolution(Sz_12,Sz)
		H+=Q14N*convolution(np.identity(2),Sz**2)
		return H

	# B=[82.85779704691888,0,0]
	# H=Hamiltonian_0(B,classe=1,E=0)
	# val,vec=egvect(H)
	# transi_NV=[val[2]-val[0],val[1]-val[0]]
	# H=Ham_p1(B,classe=1)
	# val,vec=egvect(H)
	# single=[]
	# for i in range(3,6) :
	# 	for j in range(3) :
	# 		#print(i,j,len(single))
	# 		single+=[val[i]-val[j]]
	# print([toto+transi_NV[1] for toto in single])
	# M,bname=convolution_et_base(np.identity(2),np.identity(3),bname_undemi,bnamez)
	# show_vpropres(val,vec,bname)

	ax=plt.gca()
	


	amps=np.linspace(0,200,200)
	transi=[]
	transi_NV=[]
	Sx_P1=convolution(Sx_12,np.identity(3))
	for amp in amps :
		B=[amp/sqrt(3),amp/sqrt(3),amp/sqrt(3)]
		# B=[amp,0,0]
		H=Ham_p1(B,classe=1)
		val,vec=egvect(H)
		single=[]
		# for i in range(6) :
		# 	for j in range(i) :
		# 		#print(i,j,len(single))
		# 		single+=[val[i]-val[j]]
		for pair in [[5,0],[4,1],[3,2]] :
			i=pair[0]
			j=pair[1]
			single+=[val[i]-val[j]]
		transi+=[single]
		H=Hamiltonian_0(B,classe=1,E=3)
		val,vec=egvect(H)
		transi_NV+=[[val[2]-val[0],val[1]-val[0]]]
	transi=np.array(transi)
	transi_NV=np.array(transi_NV)
	color = next(ax._get_lines.prop_cycler)['color']

	plt.plot(amps,transi[:,0]+transi_NV[:,1],'--',label='P1',color=color)
	for i in range(1,len(transi[0,:])) :
		plt.plot(amps,transi[:,i]+transi_NV[:,1],'--',color=color)

	color = next(ax._get_lines.prop_cycler)['color']
	plt.plot(amps,transi_NV[:,0],color=color,label='isolated NV')
	plt.plot(amps,transi_NV[:,1],color=color)

	transi=[]
	transi_NV=[]
	Sx_P1=convolution(Sx_12,np.identity(3))
	for amp in amps :
		B=[amp/sqrt(3),amp/sqrt(3),amp/sqrt(3)]
		# B=[amp,0,0]
		H=Ham_p1(B,classe=2)
		val,vec=egvect(H)
		single=[]
		for i in range(6) :
			for j in range(i) :
				#print(i,j,len(single))
				single+=[val[i]-val[j]]
		# for pair in [[5,0],[4,1],[3,2]] :
		# 	i=pair[0]
		# 	j=pair[1]
		# 	single+=[val[i]-val[j]]
		transi+=[single]
		H=Hamiltonian_0(B,classe=2,E=3)
		val,vec=egvect(H)
		transi_NV+=[[val[2]-val[0],val[1]-val[0]]]
	transi=np.array(transi)
	transi_NV=np.array(transi_NV)
	color = next(ax._get_lines.prop_cycler)['color']

	plt.plot(amps,transi[:,0]+transi_NV[:,1],'--',label='P1',color=color)
	for i in range(1,len(transi[0,:])) :
		plt.plot(amps,transi[:,i]+transi_NV[:,1],'--',color=color)

	color = next(ax._get_lines.prop_cycler)['color']
	plt.plot(amps,transi_NV[:,0],color=color,label='isolated NV')
	plt.plot(amps,transi_NV[:,1],color=color)
	

	def zero(i,c1,c2):
		def f(amp):
			B=[amp/sqrt(3),amp/sqrt(3),amp/sqrt(3)]
			H=Ham_p1(B,classe=c1)
			val,vec=egvect(H)
			single=[]
			for i2 in range(6) :
				for j2 in range(i2) :
					#print(i,j,len(single))
					single+=[val[i2]-val[j2]]
			transi=single
			transi_fs=transi[i]
			H=Hamiltonian_0(B,classe=c1,E=3)
			val,vec=egvect(H)
			transi=[val[2]-val[0],val[1]-val[0]]
			return transi_fs-transi[0]+transi[1]
		RR=root_scalar(f,bracket=[0,200])
		if RR.converged :
			amp=RR.root
			B=[amp/sqrt(3),amp/sqrt(3),amp/sqrt(3)]
			H=Hamiltonian_0(B,classe=c2,E=3)
			val,vec=egvect(H)
			transi=[val[2]-val[0],val[1]-val[0]]
			transi_NV=transi[0]
			return amp,transi_NV
		else :
			return False

	# for i in range(len(transi[0,:])) :
	# 	try :
	# 		x,y=zero(i,1,1)
	# 		print('%ic bon'%(i))
	# 	except :
	# 		print('%ic mort'%(i))
	# x_transi=[]
	# y_transi=[]
	# for i in range(len(transi[0,:])) :
	# 	try :
	# 		x,y=zero(i,1,1)
	# 		x_transi+=[x]
	# 		y_transi+=[y]
	# 	except :
	# 		pass

	# color = next(ax._get_lines.prop_cycler)['color']
	# plt.scatter(x_transi,y_transi,s=80,facecolors='none',edgecolors=color,label=r'cross relaxation $B_{11}$')			
	# ylim=ax.get_ylim()
	# for i in range(len(x_transi)) :
	# 	x0=x_transi[i]
	# 	y0=y_transi[i]
	# 	plt.plot([x0,x0],[y0,0],'--',color=color)

	# x_transi=[]
	# y_transi=[]
	# for i in range(len(transi[0,:])) :
	# 	try :
	# 		x,y=zero(i,1,2)
	# 		x_transi+=[x]
	# 		y_transi+=[y]
	# 	except :
	# 		pass

	
	# color = next(ax._get_lines.prop_cycler)['color']
	# plt.scatter(x_transi,y_transi,s=80,facecolors='none',edgecolors=color,label=r'cross relaxation $B_{12}$')			
	# for i in range(len(x_transi)) :
	# 	x0=x_transi[i]
	# 	y0=y_transi[i]
	# 	plt.plot([x0,x0],[y0,0],'--',color=color)

	# x_transi=[]
	# y_transi=[]
	# for i in range(len(transi[0,:])) :
	# 	try :
	# 		x,y=zero(i,2,1)
	# 		x_transi+=[x]
	# 		y_transi+=[y]
	# 	except :
	# 		pass

	# color = next(ax._get_lines.prop_cycler)['color']
	# plt.scatter(x_transi,y_transi,s=80,facecolors='none',edgecolors=color,label=r'cross relaxation $B_{21}$')			
	# for i in range(len(x_transi)) :
	# 	x0=x_transi[i]
	# 	y0=y_transi[i]
	# 	plt.plot([x0,x0],[y0,0],'--',color=color)

	# x_transi=[]
	# y_transi=[]
	# for i in range(len(transi[0,:])) :
	# 	try :
	# 		x,y=zero(i,2,2)
	# 		x_transi+=[x]
	# 		y_transi+=[y]
	# 	except :
	# 		pass

	# color = next(ax._get_lines.prop_cycler)['color']
	# plt.scatter(x_transi,y_transi,s=80,facecolors='none',edgecolors=color,label=r'cross relaxation $B_{22}$')			
	# for i in range(len(x_transi)) :
	# 	x0=x_transi[i]
	# 	y0=y_transi[i]
	# 	plt.plot([x0,x0],[y0,0],'--',color=color)

	# ax.set_ylim(ylim)
	
	plt.legend()
	plt.xlabel(r'B$\parallel$(111) (G)')
	plt.ylabel('Transition frequency (MHz)')
	plt.show()
	# H=Ham_p1([0,0,0],classe=1)
	# val,vec=egvect(H)
	# show_vpropres(val,vec,bname)
	# print(abs(vec[4].dot(Sx_P1).dot(vec[3]))*2)



def NV_0():

	D=1685
	gamma=2.8
	Axx=-23.8
	Ayy=Axx
	Azz=-35.7
	Q=-4.654
	def Ham_NV0(B,classe=1):
		B=np.array(B)
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
		
		H_e=D*Sz_32**2+gamma*(Bz*Sz_32+Bx*Sx_32)-5*D/4*np.identity(4)
		H_n=Q*Sz**2
		H_hf=Axx*convolution(Sx_32,Sx)+Ayy*convolution(Sy_32,Sy)+Azz*convolution(Sz_32,Sz)
		H=convolution(H_e,np.identity(3))+convolution(np.identity(4),H_n)+H_hf
		return H
	# H=Ham_NV0([65,0,0])
	# val,vec=egvect(H)
	# M,bname=convolution_et_base(np.identity(4),np.identity(3),bname_troisdemi,bnamez)
	# show_vpropres(val,vec,bname)
	# single=[]
	# minmax=3500
	# minmin=1000
	# for i in range(len(val)) :
	# 	for j in range(i) :
	# 		single+=[val[i]-val[j]]
	# 		if single[-1]>minmin and single[-1]<minmax :
	# 			print(i,j,len(single))
				
	# 			print(single[-1])
	# 			minmax=single[-1]
	amps=np.linspace(0,200,200)
	transi=[]
	transi_NV=[]
	for amp in amps :
		# B=[amp/sqrt(3),amp/sqrt(3),amp/sqrt(3)]
		B=[amp,0,0]
		H=Ham_NV0(B,classe=1)
		val,vec=egvect(H)
		single=[]
		for i in range(6,12) :
			for j in range(6) :
				#print(i,j,len(single))
				single+=[val[i]-val[j]]
		transi+=[single]
		H=Hamiltonian_0(B,classe=1,E=3)
		val,vec=egvect(H)
		transi_NV+=[[val[2]-val[0],val[1]-val[0]]]
	transi=np.array(transi)
	transi_NV=np.array(transi_NV)
	ax=plt.gca()
	color = next(ax._get_lines.prop_cycler)['color']
	for i in range(len(transi[0,:])) :
		if i==0 :
			plt.plot(amps,transi[:,i],color=color,label='NV0')
		else :
			plt.plot(amps,transi[:,i],color=color)
	color = next(ax._get_lines.prop_cycler)['color']
	for i in range(len(transi_NV[0,:])) :
		if i==0 :
			plt.plot(amps,transi_NV[:,i],color=color,label='NV-')
		else :
			plt.plot(amps,transi_NV[:,i],color=color)


	def zero(i,j):
		def f(amp):
			B=[amp,0,0]
			H=Ham_NV0(B,classe=1)
			val,vec=egvect(H)
			single=[]
			for i2 in range(6,12) :
				for j2 in range(6) :
				#print(i,j,len(single))
					single+=[val[i2]-val[j2]]
			transi=single
			transi_fs=transi[i]
			H=Hamiltonian_0(B,classe=1,E=3)
			val,vec=egvect(H)
			transi=[val[2]-val[0],val[1]-val[0]]
			transi_NV=transi[j]
			return transi_fs-transi_NV
		RR=root_scalar(f,bracket=[0,200])
		if RR.converged :
			amp=RR.root
			B=[amp,0,0]
			H=Hamiltonian_0(B,classe=1,E=3)
			val,vec=egvect(H)
			transi=[val[2]-val[0],val[1]-val[0]]
			transi_NV=transi[j]
			return amp,transi_NV
		else :
			return False

	x_transi=[]
	y_transi=[]

	for i in range(len(transi[0,:])) :
		for j in range(2) :
			try : 
				x,y=zero(i,j)
				x_transi+=[x]
				y_transi+=[y]
			except : 
				pass
	print(x_transi)
	print(y_transi)

	color = next(ax._get_lines.prop_cycler)['color']
	plt.scatter(x_transi,y_transi,s=80,facecolors='none',edgecolors=color,label='cross relaxation')		
	plt.legend()
	ylim=ax.get_ylim()
	for i in range(len(x_transi)) :
		x0=x_transi[i]
		y0=y_transi[i]
		plt.plot([x0,x0],[y0,0],'--',color=color)
	ax.set_ylim(ylim)
	plt.xlabel(r'B$\parallel$(100) (G)')
	plt.ylabel('Transition frequency (MHz)')
	plt.show()

# NV_0()

def transpose_basepm(M) :
	#base : (+)=(+1)+(-1)/sqrt(2), 0=0 , (-)=(+1)-(-1)/sqrt(2)
	U=np.array([[1/sqrt(2),0,1/sqrt(2)],[0,1,0],[1/sqrt(2),0,-1/sqrt(2)]])
	return(np.matmul(U.T,np.matmul(M,U)))

def some_matrices() :
	transpose_pm=False # Transpose la matrice dans la base (0+-) au lieu de (0,+1,-1)
	matrice='hplus'
	if transpose_pm :
		Sxf=transpose_basepm(Sx)
		Syf=transpose_basepm(Sy)
		Szf=transpose_basepm(Sz)
	else :
		Sxf=Sx
		Syf=Sy
		Szf=Sz

	if matrice=='gplus' :
		M1,bname=convolution(Sxf,Sxf,bnamez,bnamez)
		M2,bname=convolution(Syf,Syf,bnamez,bnamez)
		print_matrix(M1+M2,bname)

	if matrice=='gmoins' :
		M1,bname=convolution(Sxf,Sxf,bnamez,bnamez)
		M2,bname=convolution(Syf,Syf,bnamez,bnamez)
		print_matrix(M1-M2,bname)

	if matrice=='hplus' :
		M1,bname=convolution(Sxf,Syf,bnamez,bnamez)
		M2,bname=convolution(Syf,Sxf,bnamez,bnamez)
		print_matrix(M1+M2,bname)

	if matrice=='hplus' :
		M1,bname=convolution(Sxf,Syf,bnamez,bnamez)
		M2,bname=convolution(Syf,Sxf,bnamez,bnamez)
		print_matrix(M1-M2,bname)

	if matrice=='SzSz' :
		M1,bname=convolution(Szf,Szf,bnamez,bnamez)
		print_matrix(M1,bname)

	if matrice=='SxSx' :
		M1,bname=convolution(Sxf,Sxf,bnamez,bnamez)
		print_matrix(M1,bname)

	if matrice=='SySy' :
		M1,bname=convolution(Syf,Syf,bnamez,bnamez)
		print_matrix(M1,bname)

	if matrice=='SxSy' :
		M1,bname=convolution(Sxf,Syf,bnamez,bnamez)
		print_matrix(M1,bname)

	if matrice=='SySx' :
		M1,bname=convolution(Syf,Sxf,bnamez,bnamez)
		print_matrix(M1,bname)



def test_mesolve():
	H=Qobj(Hamiltonian_0([0,0,100])) #en ms
	c_op=Qobj(0.3*depop)
	rho=Qobj(rho_0)
	tlist=np.linspace(0,20,100)
	e_op=Qobj(rho_0)
	result=mesolve(H,rho,tlist,[],e_op)
	plt.plot(tlist,result[0])
	plt.show()

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

def base_1():
	return [np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1])]
def base_2(phi=0):
	b1=base_1()
	theta=2*arccos(1/sqrt(3))
	T1=np.array([[1,0,0],[0,cos(theta),sin(theta)],[0,-sin(theta),cos(theta)]])
	T2=np.array([[cos(phi),sin(phi),0],[-sin(phi),cos(phi),0],[0,0,1]])
	b2=[]
	for v in b1 :
		v2=T2.dot(T1.dot(v))
		b2+=[v2]
	return b2




def Ham_dip(b1,b2,r): # b1
	r=np.array(r)
	S=[Qobj(spin) for spin in [Sx,Sy,Sz]]
	J=52/norm(r)**3 #MHz, r en nm
	H=tensor(qeye(3),qeye(3))-tensor(qeye(3),qeye(3)) #c'est con mais je peux pas faire de zéros rapidement
	u=r/norm(r)
	for i in range(3) :
		for j in range(3) :
			H=H-J*(3*b1[i].dot(u)*b2[j].dot(u)-b1[i].dot(b2[j]))*tensor(S[i],S[j])
	return H



def test_steady():
	t1_phonon=Qobj(col_t1*sqrt(gamma_phonon))
	laser_pump=Qobj(col_laser*sqrt(gamma_las))
	collapse=t1_phonon+laser_pump
	thetas=np.linspace(0,2*pi,10)
	Bs=np.linspace(0,1000,100)
	#thetas=[0,pi/2*0.99,0.9*pi,3*pi/2*0.99]
	rho_0=[]
	print(collapse)
	# for theta in thetas :
	# 	H=Qobj(Hamiltonian_0([100*sin(theta),0,100*cos(theta)]))
	# 	dm=steadystate(H,[t1_phonon,laser_pump])
	# 	rho_0+=[dm[1,1]]
	# 	print('theta=%f'%theta)
	# 	print(H)
	# 	print(dm)
	for B in Bs :
		H=Qobj(Hamiltonian_0([B*sin(pi/2),0,B*cos(pi/2)]))
		dm=steadystate(H,make_collapse_list(gamma_las,gamma_phonon))
		rho_0+=[dm[1,1]]
	plt.plot(Bs,rho_0)
	plt.show()

def superpose_dir(ax):
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



def Hamiltonian_NV_propre_base(B,E=3,D=2870) :
	#Unité naturelle : MHz,Gauss
	B=np.array(B)
	gamma=2.8
	H=D*Sz**2+gamma*(B[0]*Sx+B[1]*Sy+B[2]*Sz)+E*(Sx.dot(Sx)-Sy.dot(Sy))
	return H

def spin_NV_propre_base(B,gamma_las=1E-3,gamma_phonon=2E-4): #Attention : gamma en MHz
	H=H=Qobj(Hamiltonian_NV_propre_base(B))
	dm=steadystate(H,make_collapse_list(gamma_las,gamma_phonon))
	rho=np.array(dm)
	s=np.array([np.trace(rho.dot(Sx)),np.trace(rho.dot(Sy)),np.trace(rho.dot(Sz))])
	return(s)



def NV_torque_propre_base(B,gamma_las=1E-3,gamma_phonon=2E-4):
	H=Qobj(Hamiltonian_NV_propre_base(B))
	dm=steadystate(H,make_collapse_list(gamma_las,gamma_phonon))
	rho=np.array(dm)
	s=np.array([np.trace(rho.dot(Sx)),np.trace(rho.dot(Sy)),np.trace(rho.dot(Sz))])
	torque=np.cross(s,B)
	return(torque)

def torque_3nvx_1classe(amp):
	thetas=np.linspace(0,2*pi,200)
	spins=[]
	B=amp
	for theta in thetas :
		spins+=[spin_NV_propre_base([B*sin(theta),0,B*cos(theta)])]

	fig,ax=plt.subplots(3)
	spins=np.array(spins)

	plt.clf()
	torques_sz=spins[:,2]*amp*sin(thetas)
	torques_sx=-spins[:,0]*amp*cos(thetas)
	NRJ_sx=-amp*spins[:,0]*sin(thetas)
	NRJ_sz=-amp*spins[:,2]*cos(thetas)
	# plt.plot(thetas,torques[:,0],label='Torque x')
	ax[0].plot(thetas,torques_sz,label='Torque Sz')
	ax[0].plot(thetas,torques_sx,label='Torque Sx')
	ax[0].plot(thetas,torques_sz+torques_sx,label='Torque total')
	ax[0].legend()
	ax[1].plot(thetas,spins[:,2],label='spin z')
	ax[1].plot(thetas,spins[:,0],label='spin x')
	ax[1].legend()
	ax[2].plot(thetas,NRJ_sz,label='Energie Sz')
	ax[2].plot(thetas,NRJ_sx,label='Energie Sx')
	ax[2].plot(thetas,NRJ_sz+NRJ_sx,label='Energie total')
	ax[2].legend()

	# plt.plot(thetas,torques[:,2],label='Torque z')
	plt.xlabel('theta dans le plan zOx')
	# plt.show()
	plt.savefig('torque une classe/simu torque 3 nvx 1 classe %iG.png'%amp)

for amp in np.arange(50,2050,50) :
	torque_3nvx_1classe(amp)
	print(amp)

def torque_1classe_amplitude(theta):
	amps=np.linspace(0,5000,200)
	spins=[]
	for amp in amps:
		spins+=[spin_NV_propre_base([amp*sin(theta),0,amp*cos(theta)])]
	fig,ax=plt.subplots(2)
	spins=np.array(spins)


	torques_sz=spins[:,2]*amps*sin(theta)
	torques_sx=-spins[:,0]*amps*cos(theta)

	ax[0].plot(amps,torques_sx,label='Torque Sx')
	ax[0].plot(amps,torques_sz,label='Torque Sz')
	ax[0].plot(amps,torques_sz+torques_sx,label='Torque total')
	ax[0].legend()
	ax[1].plot(amps,spins[:,0],label='spin x')
	ax[1].plot(amps,spins[:,2],label='spin z')
	ax[1].legend()

	plt.xlabel('theta dans le plan zOx')
	plt.show()

# torque_1classe_amplitude(0.3)

def spin_3vx_4classes(B):
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

	spin=np.zeros(3,dtype='complex128')
	for k in range(4) :
		B_base=Raller[k].dot(B)
		spin_base=spin_NV_propre_base(B_base)
		spin+=Rretour[k].dot(spin_base)
	return(spin.real)	

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
	return(theta_r,phi_r)


def vector_field_static_torque(torque):
	nthetas=20
	nphis=40
	thetas=np.linspace(pi*0.1,pi*0.9,nthetas)
	phis=np.linspace(-pi*0.9,pi*0.9,nphis)
	Fs_theta=np.zeros((nthetas,nphis))
	Fs_phi=np.zeros((nthetas,nphis))
	for t in range(nthetas) :
		theta=thetas[t]
		for p in range(nphis):
			phi=phis[p]
			r=(sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta))
			F=np.cross(torque,r)
			theta_f,phi_f=cart_to_spher(r+F*0.01)
			Fs_theta[t,p]=theta_f-theta
			Fs_phi[t,p]=phi_f-phi
	fig,ax=plt.subplots()
	q=ax.quiver(phis,thetas,Fs_phi,Fs_theta)
	plt.show()

# vector_field_static_torque([1,0,0])

def vector_field_NV_4_classes(amp):
	nthetas=20
	nphis=40
	thetas=np.linspace(pi*0.1,pi*0.9,nthetas)
	phis=np.linspace(-pi*0.9,pi*0.9,nphis)
	Fs_theta=np.zeros((nthetas,nphis))
	Fs_phi=np.zeros((nthetas,nphis))
	for t in range(nthetas) :
		theta=thetas[t]
		for p in range(nphis):
			phi=phis[p]
			r=np.array([sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)])
			B=r*amp
			s=spin_3vx_4classes(B)
			# torque=np.cross(s,r)
			# F=np.cross(torque,r)
			# theta_f,phi_f=cart_to_spher(r+F*0.01)
			theta_f,phi_f=cart_to_spher(r+s*0.01) # 0.01 parce qu'il faut une petite variation pour avoir un vecteur précis
			Fs_theta[t,p]=theta_f-theta
			Fs_phi[t,p]=phi_f-phi
	fig,ax=plt.subplots()
	q=ax.quiver(phis*180/pi,thetas*180/pi,Fs_phi,Fs_theta)
	ax.set_xlabel(r'$\phi$ (°)')
	ax.set_ylabel(r'$\theta$ (°)')
	ax.set_title('Torque map for B=%iG'%amp)
	plt.show()
	# plt.savefig('map torque/map_%iG.png'%amp)

# for amp in np.arange(100,2100,100):
# 	vector_field_NV_4_classes(amp)
# 	print(amp)

# vector_field_NV_4_classes(600)

def NRJ_map(amp):
	nthetas=100
	nphis=200
	thetas=np.linspace(pi*0.1,pi*0.9,nthetas)
	phis=np.linspace(-pi*0.9,pi*0.9,nphis)
	NRJs=np.zeros((nthetas,nphis))
	for t in range(nthetas) :
		theta=thetas[t]
		for p in range(nphis):
			phi=phis[p]
			r=np.array([sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)])
			B=r*amp
			s=spin_3vx_4classes(B)
			NRJs[t,p]=-B.dot(s)
		print('ligne %i sur %i'%(t,nthetas))
	fig,ax=plt.subplots()
	c=ax.pcolormesh(phis, thetas, NRJs, cmap='seismic')
	ax.set_title('Energie')
	cb=fig.colorbar(c,ax=ax)
	plt.show()
# NRJ_map(1300)



def torque_4classes_dir(theta,phi,amp):
	r=np.array([sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)])
	B=r*amp
	s=spin_3vx_4classes(B)
	theta_f,phi_f=cart_to_spher(r-s*0.01)
	return(phi_f-phi)
	# return(np.linalg.norm(s))

# theta=arccos(sqrt(1/3))
# phi=pi/4+3*pi/180
# amps=np.linspace(0,2000,200)
# torques=[]
# for amp in amps:
# 	torques+=[torque_4classes_dir(theta,phi,amp)*amp]
# plt.plot(amps,torques)
# plt.xlabel('B (G)')
# plt.ylabel('Torque')
# plt.show()



def torque_3nvx_4classes(B): #B exprimé dans la base (100)
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
	
	torque=np.zeros(3,dtype='complex128')
	for k in range(4) :
		B_base=Raller[k].dot(B)
		torque_base=NV_torque_propre_base(B_base)
		torque+=Rretour[k].dot(torque_base)
	return(torque.real)

def div_3vx_4classes(B):
	B=np.array(B)
	step=1E3*np.linalg.norm(B)
	
	Rzplus=np.array([[sqrt(1/2),sqrt(1/2),0],[-sqrt(1/2),sqrt(1/2),0],[0,0,1]])
	Rzmoins=np.array([[sqrt(1/2),-sqrt(1/2),0],[sqrt(1/2),sqrt(1/2),0],[0,0,1]])

	Rxplus=np.array([[1,0,0],[0,sqrt(1/3),sqrt(2/3)],[0,-sqrt(2/3),sqrt(1/3)]])
	Rxmoins=np.array([[1,0,0],[0,sqrt(1/3),-sqrt(2/3)],[0,sqrt(2/3),sqrt(1/3)]])

	Ryplus=np.array([[sqrt(1/3),0,sqrt(2/3)],[0,1,0],[-sqrt(2/3),0,sqrt(1/3)]])
	Rymoins=np.array([[sqrt(1/3),0,-sqrt(2/3)],[0,1,0],[sqrt(2/3),0,sqrt(1/3)]])


	R=Rxplus.dot(Rzplus)
	Raller=[Rymoins.dot(Rzplus),Ryplus.dot(Rzplus),Rxplus.dot(Rzplus),Rxmoins.dot(Rzplus)]
	Rretour=[Rzmoins.dot(Ryplus),Rzmoins.dot(Rymoins),Rzmoins.dot(Rxmoins),Rzmoins.dot(Rxplus)]

	div=0
	for k in range(4):
		B_base=Raller[k].dot(B)
		H=Qobj(Hamiltonian_NV_propre_base(B))
		dm=steadystate(H,make_collapse_list(gamma_las,gamma_phonon))
		rho=np.array(dm)
		s=np.array([np.trace(rho.dot(Sx)),np.trace(rho.dot(Sy)),np.trace(rho.dot(Sz))])
		for i in range(3):
			Bstep=np.zeros(3)
			Bstep[i]=step/2
			div+=(np.cross(s,B+Bstep)-np.cross(s,B-Bstep))




def map_torque(amp,ntheta=100,nphi=200):
	thetas=np.linspace(0,pi,ntheta)
	phis=np.linspace(0,2*pi,nphi)
	cartex=np.zeros((ntheta,nphi))
	cartey=np.zeros((ntheta,nphi))
	cartez=np.zeros((ntheta,nphi))
	for i in range(ntheta):
		theta=thetas[i]
		for j in range(nphi):			
			phi=phis[j]
			B=np.array([sin(theta)*sin(phi),sin(theta)*cos(phi),cos(theta)])*amp		
			torque=torque_3nvx_4classes(B)
			cartex[i,j]=torque[0]
			cartey[i,j]=torque[1]
			cartez[i,j]=torque[2]
		print('ligne %i sur %i, amp=%iG'%(i,ntheta,amp))
	fig,ax=plt.subplots(3)
	c=ax[0].pcolormesh(phis, thetas, cartex, cmap='seismic')
	ax[0].set_title('Torque en x')
	cb=fig.colorbar(c,ax=ax)
	c=ax[1].pcolormesh(phis, thetas, cartey, cmap='seismic')
	ax[1].set_title('Torque en y')
	# cb=fig.colorbar(c,ax=ax)
	c=ax[2].pcolormesh(phis, thetas, cartez, cmap='seismic')
	ax[2].set_title('Torque en z')
	# cb=fig.colorbar(c,ax=ax)
	fig.savefig('cartes_meca/map_torque_%iG.eps'%amp)
	# plt.show()



def ligne_torque():
	print(torque_3nvx_4classes([200,100,100]))
	print(torque_3nvx_4classes([0,100,0]))
	print(torque_3nvx_4classes([0,0,100]))



def steady_2_spins_1():
	thetas=np.linspace(0.6,0.64,100)
	
	fig,ax=plt.subplots(2)
	
	for gamma_f in [1,3,5,10] :
		rho_0_1=[]
		rho_0_2=[]
		for theta in thetas :
			H_0=Qobj(Hamiltonian_0([100*sin(theta),0,100*cos(theta)]))
			H_1=Qobj(Hamiltonian_0([100*sin(theta+2*arccos(1/sqrt(3))),0,100*cos(theta+2*arccos(1/sqrt(3)))]))
			H=tensor(H_0,qeye(3))+tensor(qeye(3),H_1)+Ham_dip(base_1(),base_2(),[5*cos(1.2),0,5*sin(1.2)])
			col_1=make_collapse_list(gamma_las,gamma_phonon)
			col_2=make_collapse_list(gamma_las,gamma_phonon*gamma_f)
			col_tot=[tensor(op,qeye(3)) for op in col_1]+[tensor(qeye(3),op) for op in col_2]
			dm=steadystate(H,col_tot)
			rho_0_1+=[dm.ptrace(0)[1,1]]
			rho_0_2+=[dm.ptrace(1)[1,1]]
		ax[0].plot(thetas,rho_0_1,label='gamma_f=%f'%gamma_f)
	for r in [10,13,15,20] :
		rho_0_1=[]
		rho_0_2=[]
		thetas=np.linspace(0.614,0.617,100)
		for theta in thetas :
			H_0=Qobj(Hamiltonian_0([100*sin(theta),0,100*cos(theta)]))
			H_1=Qobj(Hamiltonian_0([100*sin(theta+2*arccos(1/sqrt(3))),0,100*cos(theta+2*arccos(1/sqrt(3)))]))
			H=tensor(H_0,qeye(3))+tensor(qeye(3),H_1)+Ham_dip(base_1(),base_2(),[r*cos(1.2),0,r*sin(1.2)])
			col_1=make_collapse_list(gamma_las,gamma_phonon)
			col_2=make_collapse_list(gamma_las,gamma_phonon*5)
			col_tot=[tensor(op,qeye(3)) for op in col_1]+[tensor(qeye(3),op) for op in col_2]
			dm=steadystate(H,col_tot)
			rho_0_1+=[dm.ptrace(0)[1,1]]
			rho_0_2+=[dm.ptrace(1)[1,1]]
		ax[1].plot(thetas,rho_0_1,label='r=%f'%r)
	ax[0].legend()
	ax[1].legend()
	plt.show()

#steady_2_spins_1()

def double_quantum():
	Bs=np.linspace(0,100,100)
	fig,ax=plt.subplots(3)
	rho_0_1=[]
	rho_0_2=[]
	for B in Bs :
		H_0=Qobj(Hamiltonian_0([B,B,B]))
		H_1=Qobj(Hamiltonian_0([B,B,B]))
		H=tensor(H_0,qeye(3))+tensor(qeye(3),H_1)+Ham_dip(base_1(),base_1(),[10*cos(1.2),0,10*sin(1.2)])
		col_1=make_collapse_list(gamma_las,gamma_phonon)
		col_2=make_collapse_list(gamma_las,gamma_phonon*5)
		col_tot=[tensor(op,qeye(3)) for op in col_1]+[tensor(qeye(3),op) for op in col_2]
		dm=steadystate(H,col_tot)
		rho_0_1+=[dm.ptrace(0)[1,1]]
		rho_0_2+=[dm.ptrace(1)[1,1]]
	ax[0].plot(Bs,rho_0_1)
	ax[1].plot(Bs,rho_0_2)
	ax[2].plot(Bs,np.array(rho_0_2)+np.array(rho_0_1))
	plt.show()



def test_steady_2_levels(): ##j'ai pas séparé les collapses sur celui la, gaffe. En plus le hamiltonien dipolaire est peut-etre bien faux
	gamma_phonon=1E-4#5ms en unité MHz
	gamma_las=1E-3 #Idem que l'autre
	sx=sigmax()
	sy=sigmay()
	sz=sigmaz()
	J0=52 # MHz/nm3

	def Ham_up(B,theta) :
		#Unité naturelle : MHz,Gauss
		D=2880
		gamma=2.8
		H=np.array([[0,gamma*B*sin(theta)],[gamma*B*sin(theta),gamma*B*cos(theta)+D]])
		return(Qobj(H))
	def Ham_down(B,theta) :
		#Unité naturelle : MHz,Gauss
		D=2880
		gamma=2.8
		theta=theta+2*arccos(1/sqrt(3))
		H=np.array([[0,gamma*B*sin(theta)],[gamma*B*sin(theta),-gamma*B*cos(theta)+D]])
		return(Qobj(H))
	def Dip_same(r) :
		u=r/norm(r)
		return(-J0/norm(r)**3*(3*tensor(u[0]*sx+u[1]*sy+u[2]*sz,u[0]*sx+u[1]*sy+u[2]*sz)-(tensor(sx,sx)+tensor(sy,sy)+tensor(sz,sz))))


	def Dip_diff(r) :
		u=r/norm(r)
		theta=2*arccos(1/sqrt(3))
		sx2=cos(theta)*sx+sin(theta)*sz
		sz2=cos(theta)*sz-sin(theta)*sx
		return(-J0/norm(r)**3*(3*tensor(u[0]*sx+u[1]*sy+u[2]*sz,u[0]*sx2+u[1]*sy+u[2]*sz2)-(tensor(sx,sx2)+tensor(sy,sy)+tensor(sz,sz2))))

	laser=Qobj([[0,sqrt(gamma_las)],[0,0]])
	t1=Qobj([[0,sqrt(gamma_phonon)],[sqrt(gamma_phonon),0]])

	thetas=np.linspace(0,2*pi,100)
	Bs=np.linspace(0,1000,100)
	rho00=[]
	# for B in Bs :
	# 	H=Ham_up(B,pi/2)
	# 	rho=steadystate(H,[t1,laser])
	# 	rho00+=[rho[0,0]]
	# plt.plot(Bs,rho00)
	for theta in thetas :
		H=tensor(Ham_up(30,theta),qeye(2))+tensor(qeye(2),Ham_down(30,theta))+Dip_diff([5,0,5])
		laser2=tensor(laser,qeye(2))+tensor(qeye(2),laser)
		t12=tensor(t1,qeye(2))+tensor(qeye(2),t1)*2
		rho=steadystate(H,[t12,laser2])
		rho00+=[rho[0,0]+rho[1,1]]
	plt.plot(thetas,rho00)
	plt.show()

def gplus(theta,phi,alpha) :
	return(1/2*(3*sin(theta)*cos(phi)*(cos(alpha)*sin(theta)*cos(phi)+sin(alpha)*cos(theta))-cos(alpha)+3*(sin(theta)*sin(phi))**2-1))
def hmoins(theta,phi,alpha) :
	return(1/2*(3*sin(theta)*cos(phi)*(sin(theta)*sin(phi))-3*(sin(theta)*sin(phi))*(cos(alpha)*sin(theta)*cos(phi)+sin(alpha)*cos(theta))))

def gplus_same(theta,phi) :
	alpha=2*arccos(1/sqrt(3))
	return sqrt(gplus(theta,phi,alpha)**2+hmoins(theta,phi,alpha)**2)*sin(theta)/(4*pi)

def angular_average_manuel(f) : 
	N=100
	thetas=np.linspace(0,pi,N)
	phis=np.linspace(0,2*pi,N)
	dtheta=thetas[1]-thetas[0]
	dphi=phis[1]-phis[0]
	tot=0
	for theta in thetas[1:-1] :
		for phi in phis[1:-1] :
			tot+=f(theta,phi)*dtheta*dphi
		tot+=(f(theta,phis[0])+f(theta,phis[-1]))/2*dtheta*dphi
	for theta in (thetas[0],thetas[-1]) :
		for phi in phis[1:-1] :
			tot+=f(theta,phi)/2*dtheta*dphi
		tot+=(f(theta,phis[0])+f(theta,phis[-1]))/4*dtheta*dphi
	return(tot)

def angular_average(f) :
	return(dblquad(f,0,2*np.pi,lambda x:0,lambda x:np.pi))




#Le principal problème ici c'est que je considère tous les états comme étant |+1> et |-1>. Y'a peut-etre moyen de faire mieux mais on verra ca plus tard
#L'autre soucis c'est que je ne prend pas en compte l'élargissement inhomogène
def Lukin(B,gamma_las=1E-3,gamma_phonon=3E-4,gamma_f=1): #En Mhz
	B=np.array(B)
	PL=0
	Ci=[np.array([1,1,1])*1/np.sqrt(3),np.array([1,-1,-1])*1/np.sqrt(3),np.array([-1,1,-1])*1/np.sqrt(3),np.array([-1,-1,1])*1/np.sqrt(3)]
	Hi=[]
	egplus=[]
	egmoins=[]
	for i in range(4) :
		C=Ci[i]
		Bz=B.dot(C)
		B_rel=[np.sqrt(max(B.dot(B)-Bz**2,0)),0,Bz] #Il aime pas les racines de nobres négatifs avec les arrondis
		H=Hamiltonian_0(B_rel)
		Hi+=[H]
		val,vec=egvect(H)
		egmoins+=[val[1]-val[0]]
		egplus+=[val[2]-val[0]]
	



