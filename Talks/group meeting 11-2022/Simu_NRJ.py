import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(4,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

Bs=np.linspace(-150,150,200)

for c in range(1,5):
	vp=[]
	vm=[]
	for B in Bs:
		theta=60*pi/180
		phi=40*pi/180
		u=np.array([sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)])
		H=NVHamiltonian(u*B,c=c)
		transis=H.transitions()
		vp+=[transis[1]]
		vm+=[transis[0]]
	plt.plot(Bs,vp,color=color(0))
	plt.plot(Bs,vm,color=color(0))



plt.plot(Bs,np.ones(len(Bs))*2600,color=color(1),ls='--',)
plt.show()