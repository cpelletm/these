import numpy as np
import matplotlib.pyplot as plt
from bresenham import bresenham #permet de tracer des lignes pixelisées

thetamin=-9
thetamax=9
phimin=-6
phimax=6


with open('map_weekend.txt','r') as f :
	c=f.read()
	c=c.split('\n\n\n')
	map=np.zeros((100,100,2))
	for k in range(len(c)-1):
		map_inter=c[k]
		map_inter=map_inter.split('\n')
		for i in range(len(map_inter)) :
			line=map_inter[i]
			line=line.split()
			#print(line)
			for j in range(len(line)) :				
				v=float(line[j])
				if (v>1e6) :
					v=v/2
				map[i,j,1]+=1
				map[i,j,0]=map[i,j,0]*(1-1./(map[i,j,1]))+v*(1./(map[i,j,1]))

phi=np.linspace(-6,6,99)
theta=np.linspace(-9,9,99)
map=map[1:-1,:-2,0]
map=map/np.amax(map)
fig,ax=plt.subplots(2)
c=ax[0].pcolormesh(theta,phi,map) #y'a une random ligne en y=0 que je comprend pas...




xrouge=np.linspace(thetamin,thetamax,2)
yrouge=np.linspace(phimin,phimax,2)
#ax[0].plot(xrouge,yrouge,'r-')

i=0
xmin=i
while theta[i]<thetamin and i < len(theta):
	xmin=i
	i+=1

i=0
xmax=i
while theta[i]<thetamax and i < len(theta):
	xmax=i
	i+=1

i=0
ymin=i
while phi[i]<phimin and i < len(phi):
	ymin=i
	i+=1

i=0
ymax=i
while phi[i]<phimax and i < len(phi):
	ymax=i
	i+=1


ligne=list(bresenham(xmin,ymin,xmax,ymax))
ax[0].plot([theta[p[0]] for p in ligne],[phi[p[1]] for p in ligne], 'r-')
coupe=[]
for p in ligne :
	coupe+=[map[p[1],p[0]]]



angle=np.linspace(0,np.sqrt((thetamax-thetamin)**2+(phimax-phimin)**2),len(coupe))



ax[1].plot(angle,coupe,'x-')
ax[0].set_xlabel(r'$\theta$ (°)')
ax[0].set_ylabel(r'$\phi$ (°)',rotation=0)
fig.colorbar(c,ax=ax)
plt.show()
