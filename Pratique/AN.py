from math import *
import numpy as np

kb=1.38E-23
Na=6.02e23
hbar=1.05e-34
h=2*pi*hbar

density_diam=3.5 #g/cm3
m_carbon=12.01/Na #g
# print(density_diam/m_carbon) #1.75e23 atomes/cm3

P=1e5
T=300
eV=1.6E-19
# print('%e'%(kb*T/h))
# Theta_NV=acos(-1/3)
# print(Theta_NV*180/pi)


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

# couplage_NV()

print(1.5*sqrt(0.003))

