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

def nrj_4_niveaux(B):
	B=np.array(B)
	Rzplus=np.array([[sqrt(1/2),sqrt(1/2),0],[-sqrt(1/2),sqrt(1/2),0],[0,0,1]])
	Rzmoins=np.array([[sqrt(1/2),-sqrt(1/2),0],[sqrt(1/2),sqrt(1/2),0],[0,0,1]])

	Rxplus=np.array([[1,0,0],[0,sqrt(1/3),sqrt(2/3)],[0,-sqrt(2/3),sqrt(1/3)]])
	Rxmoins=np.array([[1,0,0],[0,sqrt(1/3),-sqrt(2/3)],[0,sqrt(2/3),sqrt(1/3)]])

	Ryplus=np.array([[sqrt(1/3),0,sqrt(2/3)],[0,1,0],[-sqrt(2/3),0,sqrt(1/3)]])
	Rymoins=np.array([[sqrt(1/3),0,-sqrt(2/3)],[0,1,0],[sqrt(2/3),0,sqrt(1/3)]])


	Raller=[Rymoins.dot(Rzplus),Ryplus.dot(Rzplus),Rxplus.dot(Rzplus),Rxmoins.dot(Rzplus)]
	Rretour=[Rzmoins.dot(Ryplus),Rzmoins.dot(Rymoins),Rzmoins.dot(Rxmoins),Rzmoins.dot(Rxplus)]
	transis=[]
	for k in range(4) :
		B_base=Raller[k].dot(B)
		H=Hamiltonian_NV_propre_base(B_base)
		val,vec=egvect(H)
		transis+=[val[1]-val[0]]
	return(transis)

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

xmin=30 # 80 Pour 121

fig,ax=plt.subplots()


theta_111=arctan(sqrt(2))
gamma_las=5E-3

B_in=np.array([77.05651621, 28.6554855 , 82.52557109]) #121
B_out=np.array([ 26.79109384,  50.35396382, 115.30922273])

B_1=np.array([ 37.0815447 ,  27.17222075, 106.08986284]) #22
B_2=np.array([ 40.35446569, -22.06572528, 129.456638  ])
B_in=B_1+(B_2-B_1)*(-0.02)
B_out=B_1+(B_2-B_1)*0.98


n=201
xs=np.linspace(0,np.linalg.norm(B_out-B_in),n)
xs=xs-xs[xmin]
Bxs=np.linspace(B_in[0],B_out[0],n)
Bys=np.linspace(B_in[1],B_out[1],n)
Bzs=np.linspace(B_in[2],B_out[2],n)

# color = next(ax._get_lines.prop_cycler)['color']
# transis=[]
# for i in range(n):
# 	B=[Bxs[i],Bys[i],Bzs[i]]
# 	transis+=[nrj_4_niveaux(B)]

# transis=np.array(transis)
# for i in range(4):
# 	plt.plot(xs[xmin:],transis[xmin:,i],color=color,lw=3)

# torques=[]
# PLs=[]
# torques_sans=[]
# PLs_sans=[]
# for i in range(n):
# 	B=[Bxs[i],Bys[i],Bzs[i]]
# 	H=Hamiltonian_NV_propre_base(B)
# 	gamma_t1=make_t1_list(B,width=6)
# 	s,rho_0=spin_3vx_4classes(B,gamma_las,gamma_t1)
# 	PLs+=[rho_0]
# 	torques+=[np.cross(s,B)]
# 	gamma_t1=np.ones(4)*1E-3
# 	s,rho_0=spin_3vx_4classes(B,gamma_las,gamma_t1)
# 	PLs_sans+=[rho_0]
# 	torques_sans+=[np.cross(s,B)]

# torques=np.array(torques)*h*gamma_e*n_centers*1E19
# torques_sans=np.array(torques_sans)*h*gamma_e*n_centers*1E19
# PLs=np.array(PLs)/4
# PLs_sans=np.array(PLs_sans)/4


# color = next(ax._get_lines.prop_cycler)['color']
# ax.plot(xs[xmin:],PLs[xmin:],label='With CR',color=color)
# ax.plot(xs[xmin:],PLs_sans[xmin:],'--',color=color,label='Without CR')
# ax.set_xlabel('Secondary B (G)',fontsize=25)
# ax.set_ylabel(r'$\rho_{00}$',fontsize=25)

# color = next(ax._get_lines.prop_cycler)['color']
# ax.plot(xs[xmin:],torques[xmin:,0],label='With CR',color=color)
# ax.plot(xs[xmin:],torques_sans[xmin:,0],'--',label='Without CR', color=color)
# ax.set_xlabel('Secondary B (G)',fontsize=25)
# ax.set_ylabel(r'Torque ($10^{-19}$Nm)',fontsize=25)

# color = next(ax[1]._get_lines.prop_cycler)['color']
# ax[1].plot(xs,torques[:,1],label='Torque y',color=color)
# ax[1].plot(xs,torques_sans[:,1],'--',color=color)
# color = next(ax[1]._get_lines.prop_cycler)['color']
# ax[1].plot(xs,torques[:,2],label='Torque z',color=color)
# ax[1].plot(xs,torques_sans[:,2],'--',color=color)

torques=[]
torques_sans=[]
for i in range(n):
	B=[Bxs[i],Bys[i],Bzs[i]]
	H=Hamiltonian_NV_propre_base(B)
	gamma_t1=make_t1_list(B,width=6)
	torque_4_classes=[]
	for k in range(4):
		s,rho_0=spin_3vx_1classe(B,gamma_las,gamma_t1,classe=k)
		torque_4_classes+=[np.cross(s,B)]
	torques+=[torque_4_classes]
	gamma_t1=np.ones(4)*1E-3
	torque_4_classes=[]
	for k in range(4):
		s,rho_0=spin_3vx_1classe(B,gamma_las,gamma_t1,classe=k)
		torque_4_classes+=[np.cross(s,B)]
	torques_sans+=[torque_4_classes]

torques=np.array(torques)*h*gamma_e*n_centers*1E19
torques_sans=np.array(torques_sans)*h*gamma_e*n_centers*1E19
color = next(ax._get_lines.prop_cycler)['color']

for i in range(4) :
	plt.plot(xs[xmin:],torques[xmin:,i,1],'--',color=color,lw=2)

torques_total=torques[:,0,:]+torques[:,1,:]+torques[:,2,:]+torques[:,3,:]

color = next(ax._get_lines.prop_cycler)['color']
plt.plot(xs[xmin:],torques_total[xmin:,1],color=color,lw=3)

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

# fname='0-0.8V_PLdown-Db'
# x,y=extract_data(fname+'.txt')
# y=y/max(y)
# # ax.set_xlabel('Secondary B (G)',fontsize=25)
# # ax.set_ylabel('Signal (a.u.)',fontsize=25)
# ax.plot(xs[xmin:],y[xmin:],'o',markerfacecolor="None")


# x,y=extract_data(fname+'.txt',ycol=3)
# y=y/max(y)
# ax.set_xlabel('Secondary B (G)',fontsize=25)
# ax.set_ylabel('Signal (a.u.)',fontsize=25)
# ax.plot(xs[xmin:],y[xmin:])



# ax.legend(fontsize=25)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()