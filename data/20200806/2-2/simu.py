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


h=6.626*1E-34
gamma_e=2.8*1E6 #en Hz/Gauss
n_centers=1E9/4 #nb de spins par classe

xmin=30
xmax=200

fig,axs=plt.subplots(2)


theta_111=arctan(sqrt(2))
gamma_las=5E-3

B_1=np.array([ 37.0815447 ,  27.17222075, 106.08986284])
B_2=np.array([ 40.35446569, -22.06572528, 129.456638  ])

B_in=B_1+(B_2-B_1)*(-0.02)
B_out=B_1+(B_2-B_1)*0.98
n=201
xs=np.linspace(0,np.linalg.norm(B_out-B_in),n)
xs=xs-xs[xmin]
Bxs=np.linspace(B_in[0],B_out[0],n)
Bys=np.linspace(B_in[1],B_out[1],n)
Bzs=np.linspace(B_in[2],B_out[2],n)
torques=[]
PLs=[]
torques_sans=[]
PLs_sans=[]
for i in range(n):
	B=[Bxs[i],Bys[i],Bzs[i]]
	H=Hamiltonian_NV_propre_base(B)
	gamma_t1=make_t1_list(B,width=6)
	s,rho_0=spin_3vx_4classes(B,gamma_las,gamma_t1)
	PLs+=[rho_0]
	torques+=[np.cross(s,B)]
	gamma_t1=np.ones(4)*1E-3
	s,rho_0=spin_3vx_4classes(B,gamma_las,gamma_t1)
	PLs_sans+=[rho_0]
	torques_sans+=[np.cross(s,B)]




torques=np.array(torques)*h*gamma_e*n_centers*1E19
torques_sans=np.array(torques_sans)*h*gamma_e*n_centers*1E19
PLs=np.array(PLs)/4
PLs_sans=np.array(PLs_sans)/4


ax=axs[1]
color = next(ax._get_lines.prop_cycler)['color']
ax.plot(xs[xmin:],PLs[xmin:],lw=3,label='With CR',color=color)
ax.plot(xs[xmin:],PLs_sans[xmin:],'--',lw=3,color=color,label='Without CR')
# ax.set_xlabel(r'B$_{em}$ (G)',fontsize=15)
# ax.set_ylabel(r'|$m_s$=0> population',fontsize=15)
ax.legend(fontsize=20)
ax.tick_params(labelsize=20)

# color = next(ax._get_lines.prop_cycler)['color']
# ax.plot(xs[xmin:],torques[xmin:,0],label='With CR',color=color)
# ax.plot(xs[xmin:],torques_sans[xmin:,0],'--',label='Without CR', color=color)
# ax.set_xlabel('Secondary B (g)',fontsize=25)
# ax.set_ylabel(r'Torque ($10^{-19}$Nm)',fontsize=25)

# color = next(ax._get_lines.prop_cycler)['color']
# ax.plot(xs[xmin:],torques[xmin:,1],lw=3,label='With CR',color=color)
# ax.plot(xs[xmin:],torques_sans[xmin:,1],'--',lw=3,label='Without CR', color=color)
# # ax.set_xlabel(r'B$_{em}$ (G)',fontsize=15)
# # ax.set_ylabel(r'Torque ($10^{-19}$Nm)',fontsize=15)
# ax.legend(fontsize=20)
# ax.tick_params(labelsize=20)

# color = next(ax._get_lines.prop_cycler)['color']
# ax.plot(xs[xmin:],torques[xmin:,2],label='With CR',color=color)
# ax.plot(xs[xmin:],torques_sans[xmin:,2],'--',label='Without CR', color=color)
# ax.set_xlabel('Secondary B (g)',fontsize=25)
# ax.set_ylabel(r'Torque ($10^{-19}$Nm)',fontsize=25)




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


y_tot=np.zeros(201)
pool=['0-0.5V_PLdown','0-0.5V_PLdown-c','0-0.5V_PLdown-e-14uW','0-0.5V_PLdown-f-18.5uW','0-0.5V_PLdown-d-14uW_was9']
for fname in pool :
	x,y=extract_data(fname+'.txt',ycol=3)
	y=y/max(y)
	y_tot+=y/5

ax=axs[0]
# ax.set_xlabel(r'B$_{em}$ (G)',fontsize=15)
# ax.set_ylabel('Reflected signal (a.u)',fontsize=15)
# ax.legend(fontsize=15)
ax.tick_params(labelsize=20)

ax.plot(xs[xmin:xmax],y_tot[xmin:xmax])


# fname='0-0.5V_PLdown'
# x,y=extract_data(fname+'.txt',ycol=1)
# y=y/max(y)
# ax.set_xlabel('Secondary B (G)',fontsize=25)
# ax.set_ylabel('Signal (a.u.)',fontsize=25)
# ax.plot(xs[xmin:],y[xmin:])




plt.show()