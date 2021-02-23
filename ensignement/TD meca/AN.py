from math import *

kb=1.38E-23
Na=6.02e23


P=1e5
T=300

m=30e-3/Na
v=sqrt(8*kb*T/(pi*m))

R=2e-10
sigma=4*pi*R**2

tc=kb*T/(P*v*sigma)
l=tc*v

print(3.57E-10*1/(4.6E-6*8)**(1/3))