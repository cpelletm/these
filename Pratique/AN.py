from math import *

kb=1.38E-23
Na=6.02e23
hbar=1.05e-34

density_diam=3.5 #g/cm3
m_carbon=12.01/Na #g
# print(density_diam/m_carbon) #1.75e23 atomes/cm3

P=1e5
T=300
eV=1.6E-19
Theta_NV=acos(-1/3)
print(Theta_NV*180/pi)


def pola_NV(T):
	dE=2.87E9*2*pi*hbar
	pzero=1/(1+2*exp(-(dE)/(kb*T)))
	dp=pzero-1/3
	print(pzero,dp)

# pola_NV(0.065)


