import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

Bs=np.linspace(0,100,200)
vp=2870+2.8*Bs
vm=2870-2.8*Bs

plt.plot(Bs,vp,color=color(0))
plt.plot(Bs,vm,color=color(0))
plt.plot(Bs,np.ones(len(Bs))*2700,color=color(1),ls='--')
plt.show()