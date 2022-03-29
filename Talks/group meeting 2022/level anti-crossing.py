import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *



transiplus=[]
transimoins=[]
Bs=np.linspace(-15,15,200)
for B in Bs:
	mf=magneticField(x=0,y=0,z=B)
	t=mf.transitions4Classes()
	transiplus+=[t[-1]]
	transimoins+=[t[0]]

Bs=np.array(Bs)/10
plt.plot(Bs,transiplus,lw=2)
plt.plot(Bs,transimoins,lw=2)
plt.xlabel('Magnetic Field (mT)',fontsize=15)
plt.ylabel('Frequency (MHz)',fontsize=15)
# plt.yticks(fontsize=15)
# plt.xticks(fontsize=15)
plt.show()