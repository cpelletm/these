import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


def poly(L,G):
	x=L**5+ 0.07842*L**4*G+ 4.47163*L**3*G**2+ 2.42843*L**2*G**3+ 2.69269*L*G**4+ G**5
	return(x**(1/5))

def find_L_dicho(G=4.33,tot=8.78):
	xmin,xmax=dichotomy(f=poly,target=tot,xmin=0,xmax=20,precision='auto',G=G)
	print(xmin,xmax)



print(5.3/2) #ODMR rose
print(2.1*2*2.8/sqrt(3)) #VH- (a peu près, fait pas chier)
print(5*2*2.8/sqrt(3))
find_L_dicho(G=2.7,tot=6.8)