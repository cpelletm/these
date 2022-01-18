import numpy as np
import matplotlib.pyplot as plt
import random as rd
import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

epsilon0=8.854187e-12
epsilonr=5.7
eV=1.602E-19
dparallel=0.35
dperp=17

def champE(x,y,z,q=-1):	
	q=q*eV
	r3=(x**2+y**2+z**2)**(3/2)
	pref=q/(4*np.pi*epsilonr*epsilon0*r3)*1e16 #1e18 pour passer nm-2 -> m-2 puis 1e-2 pour passer m-1 -> cm-1
	return(np.array([x*pref,y*pref,z*pref])) #E en V/cm



def R0(rho,nCharges=100) : #(rho en ppm) #Attention : pour Mittiga, rho c'est la densité de charges + OU -, et nC le nombre de charges + ET -. Moi je vais prendre le nombre total tout le temps
	n0=1.76e-4 #(conversion ppm nm^-3, on trust Mittiga. J'ai pas trust mais il a raison)
	return((3*nCharges)/(4*np.pi*rho*n0))**(1/3) #en nm


def getRandPos(r) :
	x=r
	y=r
	z=r
	while x**2+y**2+z**2>r**2 :
		x=rd.uniform(-r,r)
		y=rd.uniform(-r,r)
		z=rd.uniform(-r,r)
	return x,y,z

def simu_E(rho,nCharges=100):
	E=np.zeros(3)
	r=R0(rho,nCharges)
	for i in range(nCharges):
		sgn=rd.choice([-1,+1])
		x,y,z=getRandPos(r)
		E+=champE(x,y,z,q=sgn)
	return(dperp*np.sqrt((E[1]**2+E[2]**2)))



# data=[]
# for i in range(int(1e5)) :
# 	data+=[simu_E(rho=2)]
# 	if i%100==0 :
# 		print(i)

# hist,bin_edges=np.histogram(data,bins=100,range=(0,5e6))
# bin_middle=(bin_edges[:-1]+bin_edges[1:])/2

# with open('Simu 1 ppm E.txt','w') as f:
# 	for i in range(len(hist)) :
# 		f.write('%e \t %e \n'%(bin_middle[i],hist[i]))


def inverse_gamma(x,alpha,beta):
	return np.exp(-beta/x)/(x**(alpha+1))

bin_middle,hist=extract_data('Simu 1 ppm E.txt')
x=bin_middle/1e6
y=hist/max(hist)


popt,yfit=fit_inverse_gamma(x,y)
print(popt)

plt.plot(x,y)
plt.plot(x,yfit)
plt.show()
