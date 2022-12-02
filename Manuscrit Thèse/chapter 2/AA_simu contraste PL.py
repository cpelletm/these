import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


#REF : "Magnetic-field-dependent photodynamics of single NV defects in diamond: an application to qualitative all-optical magnetic imaging"
# unité naturelle pour k et Omega : µs-1 ; Beta est une fraction du temps de vie radiatif (beta=1 saturation de la transition)

def alpha_func(B,c=1):
	alpha=np.zeros((7,7))
	alpha[6,6]=1
	H=NVHamiltonian(B,c=c,E=0,D=2870,order='ascending')
	egvect=np.array(H.egvect())
	alpha[0:3,0:3]=egvect
	H=NVHamiltonian(B,c=c,E=0,D=1420,order='ascending')
	egvect=np.array(H.egvect())
	alpha[3:6,3:6]=egvect
	return (alpha)

def k0_func(beta=1):
	k0r=65
	k047=8
	k057=55
	k071=1
	k072=1
	k0=np.zeros((7,7))
	k0[4-1,1-1]=k0r
	k0[1-1,4-1]=beta*k0r
	k0[5-1,2-1]=k0r
	k0[2-1,5-1]=beta*k0r
	k0[6-1,3-1]=k0r
	k0[3-1,6-1]=beta*k0r
	k0[4-1,7-1]=k047
	k0[5-1,7-1]=k057
	k0[6-1,7-1]=k057
	k0[7-1,1-1]=k071
	k0[7-1,2-1]=k072
	k0[7-1,3-1]=k072

	return k0




def k_func(B,c=1,beta=1,Omega12=0):
	alpha=alpha_func(B,c=c)
	k0=k0_func(beta=beta)
	k=np.zeros((7,7))
	for i in range(7) :
		for j in range(7) :
			for p in range(7) :
				for q in range(7) :
					k[i,j]+=(alpha[i,p]**2)*(alpha[j,q]**2)*k0[p,q]

	k[1-1,2-1]=Omega12
	k[2-1,1-1]=Omega12
	return k

# print_matrix(k_func(B=[0,0,100],c=1,beta=0.5,Omega12=10))

def M_func(B,c=1,beta=1,Omega12=0): #La matrice des 7 equation linéR. J'en prends que 6 du coup vu qu'elles sont couplées
	k=k_func(B,c,beta,Omega12)
	M=np.zeros((7,7))
	M[6,:]=np.ones(7) #Correspond a n1+n2+...=1
	for i in range(6):
		for j in range(7):
			if i==j:
				M[i,j]=-sum(k[i,:])
			else :
				M[i,j]=k[j,i]


	return(M)
# print_matrix(M_func(B=[0,0,100],c=5,beta=0.5))


def pop_func(B,c=1,beta=1,Omega12=0):
	M=M_func(B,c,beta,Omega12)
	M_inv=np.linalg.inv(M)
	sol=np.zeros(7)
	sol[6]=1 #Correspond a n1+n2+...=1
	pop=M_inv.dot(sol)
	return(pop)

# print(pop_func(B=[0,0,100],c=5,beta=0.1))

def PL_func(B,c=1,beta=1,Omega12=0):
	pop=pop_func(B,c,beta,Omega12)
	k=k_func(B,c,beta,Omega12)
	PL=0
	for i in range(4,7):
		for j in range(1,3):
			PL+=pop[i-1]*k[i-1,j-1]

	return PL

def plot_PL(theta=0,beta=1):
	theta_rad=theta*pi/180
	Brange=np.linspace(5,400,100)
	PL=np.zeros(100)
	for i in range(100):
		PL[i]=PL_func(B=[Brange[i]*sin(theta_rad),0,Brange[i]*cos(theta_rad)],c=5,beta=beta)
	PL=PL/max(PL)
	plt.plot(Brange,PL,label=r'$\theta=$%i°'%(int(theta)))

	


def plot_ODMR_contrast(beta=0.5,Omega12=10,c=1,label='',color=color(0),ls='-'):
	Brange=np.linspace(5,500,100)
	PL_sans_uw=np.zeros(100)
	PL_avec_uw=np.zeros(100)
	for i in range(100):
		PL_sans_uw[i]=PL_func(B=[0,0,Brange[i]],c=c,beta=beta,Omega12=0)
		PL_avec_uw[i]=PL_func(B=[0,0,Brange[i]],c=c,beta=beta,Omega12=Omega12)
	contrast=(PL_sans_uw-PL_avec_uw)/PL_sans_uw

	plt.plot(Brange,contrast/max(contrast),label=label,color=color,ls=ls)

plt.figure(num=1,figsize=(6,3),dpi=80)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.locator_params(axis='x', nbins=7)
plt.locator_params(axis='y', nbins=5)
	

plot_PL(0)
# plot_PL(5,beta=1e-5)
# plot_PL(10,beta=1e-5)
# plot_PL(20,beta=1e-5)
# plot_PL(30,beta=1e-5)
# plot_PL(40,beta=1e-5)
plot_PL(45,beta=1e-5)

# plot_ODMR_contrast(beta=0.5,Omega12=10,c=1)
# plot_ODMR_contrast(beta=0.5,Omega12=10,c=5,label=r'NV $\parallel$ [111]',ls='-')
# plot_ODMR_contrast(beta=0.5,Omega12=10,c=6,label=r'NV $\nparallel$ [111]',ls='--')

plt.legend()
plt.show()