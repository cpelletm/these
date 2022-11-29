import numpy as np
from numpy import cos, sin, tan, pi, arccos, arcsin, sqrt, exp, log
import matplotlib.pyplot as plt
import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('C:\\Users\\cleme\\OneDrive\\Documents\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

kb=1.38E-23
Na=6.02e23
hbar=1.05e-34
h=2*pi*hbar
mu0=4*pi*1e-7
c=3e8

density_diam=3.5 #g/cm3
m_carbon=12.01/Na #g
# print(density_diam/m_carbon) #1.75e23 atomes/cm3
#Autre odg : ppm=1e5/µm3
#Autre odg : 5 ppm = 10.4 nm de distance moyenne

# print(1e5*(20e-3**3)*5)

P=1e5
T=300
eV=1.6E-19
# print('%e'%(kb*T/h))
# Theta_NV=arccos(-1/3)
# print(Theta_NV*180/pi)

gamma_SI=1.761*1e11
J0=mu0/(4*pi)*(gamma_SI*hbar)**2




def pola_NV(T):
	dE=2.87E9*2*pi*hbar
	pzero=1/(1+2*exp(-(dE)/(kb*T)))
	dp=pzero-1/3
	print(pzero,dp)
# pola_NV(0.065)

def couplage_NV():
	rho_atom=density_diam/m_carbon #densité en atomes/cm3
	d=(1/rho_atom)**(1/3)*1e-2 #distance entre atome en m
	rho_NV=3E-6 #3 ppm
	d_NV=d/(rho_NV**(1/3)) #distance entre 2 NV pour une répartition parfaite
	# print(d_NV)
	J=52*1e6*(1e-9**3) #J=52 MHz*nm3 en SI
	c=J/(d_NV**3)
	print('%e'%c)

def simu_NRJ_NV():
	D=2870
	gamma=2.8
	theta=1.5
	Bmax=500
	n=300
	Bs=[[B*sin(theta),0,B*cos(theta)] for B in np.linspace(0,Bmax,n)]
	Bnorms=np.array([np.linalg.norm(B) for B in Bs])
	levels=np.zeros((n,3))
	for i in range(n):
		H=NVHamiltonian(Bs[i],c=5)
		levels[i,:]=H.egval()
	plt.plot(Bnorms,levels)
	approx_zero=-(gamma*Bnorms*sin(theta))**2/D
	approx_moins=D-gamma*Bnorms*cos(theta)+(gamma*Bnorms*sin(theta))**2/(D-gamma*Bnorms*cos(theta))
	approx_plus=D+gamma*Bnorms*cos(theta)+(gamma*Bnorms*sin(theta))**2/(D+gamma*Bnorms*cos(theta))
	plt.plot(Bnorms,approx_zero,'--')
	plt.plot(Bnorms,approx_moins,'--')
	plt.plot(Bnorms,approx_plus,'--')
	plt.show()


def shot_noise_limit(lbda=700e-9,P=0.8e-6):
	pass



