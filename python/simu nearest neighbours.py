import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

nSample=10000
nNeighbours=100

def nearest_elem(e,l):
	base=abs(e-l[0])
	for k in l :
		if abs(e-k) < base :
			base=abs(e-k)

	return(base)


distances=np.zeros(nNeighbours)

for dummy in range(nSample):
	rd=np.random.random(nNeighbours)
	for i in range(2,nNeighbours):
		minimum=nearest_elem(rd[0],rd[1:i])
		distances[i]+=minimum/nSample

x=np.arange(1,99)
y=distances[2:]
plt.plot(x,y,'x',label='random')
popt,yfit=invert_fit(x,y)
print(popt)
plt.plot(x,1/x,label='Uniform') #Pour une répartition uniforme
plt.plot(x,0.5/x,label='Uniform/2')
plt.legend()
plt.show()
