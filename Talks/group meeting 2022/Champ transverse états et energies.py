import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

n=200
levels=np.zeros((n,3))
Bs=np.linspace(0,200,n)
DeltaE=np.zeros(n)
DeltaVect=np.zeros(n)




for i in range(n):
	theta=90*pi/180
	B=Bs[i]
	H=NVHamiltonian(B=[B*sin(theta),0,B*cos(theta)],c=5)
	E=H.egval()
	V=H.egvect()
	levels[i,:]=E
	DeltaE[i]=E[2]-E[1]
	DeltaVect[i]=(V[2].dot([1/sqrt(2),0,1/sqrt(2)]))**2
	# DeltaVect[i]=abs(V[2].dot([0,1,0]))
	# DeltaVect[i]=abs(V[0].dot([0,1,0]))


Bs=np.array(Bs)/10

plt.xlabel('Magnetic Field (mT)',fontsize=15)
ax1=plt.gca()
ax2=ax1.twinx()
ax1.plot(Bs,DeltaE,lw=2)
ax1.set_ylabel(r'$E_e - E_d$ (MHz)',fontsize=15)
ax1.set_ylim(0,max(DeltaE)*1.05)
ax2.plot(Bs,DeltaVect,lw=2,color='r')
ax2.set_ylim(0.9,1.005)
# plt.yticks(fontsize=15)
# plt.xticks(fontsize=15)
plt.show()