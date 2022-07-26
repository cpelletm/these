import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

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




def k_func(B,c=1,beta=1):
	alpha=alpha_func(B,c=c)
	k0=k0_func(beta=beta)
	k=np.zeros((7,7))
	for i in range(7) :
		for j in range(7) :
			for p in range(7) :
				for q in range(7) :
					k[i,j]+=(alpha[i,p]**2)*(alpha[j,q]**2)*k0[p,q]

	return k


def M_func(B,c=1,beta=1): #La matrice des 7 equation linéR. J'en prends que 6 du coup vu qu'elles sont couplées
	k=k_func(B,c,beta)
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


def pop_func(B,c=1,beta=1):
	M=M_func(B,c,beta)
	M_inv=np.linalg.inv(M)
	sol=np.zeros(7)
	sol[6]=1 #Correspond a n1+n2+...=1
	pop=M_inv.dot(sol)
	return(pop)

def PL_func(B,c=1,beta=1):
	pop=pop_func(B,c,beta)
	k=k_func(B,c,beta)
	PL=0
	for i in range()

print(pop_func(B=[0,0,100],c=5,beta=0.1))
