import numpy as np
import matplotlib.pyplot as plt
import bresenham

x0=0
y0=50
xf=96
yf=50

xy=[]
with open('map_average.txt','r') as f:
	for line in f:
		line=line.split()
		xy+=[[float(elem) for elem in line]]

map=np.array(xy)

theta_axis=np.linspace(-6,6,len(map[0,:]))
phi_axis=np.linspace(-9,9,len(map[:,0]))


fig,ax=plt.subplots(2)

ax1=ax[0]
ax2=ax[1]

C=ax1.pcolormesh(xy)
bres=list(bresenham.bresenham(x0,y0,xf,yf))
bres=np.array(bres)
ax1.scatter(bres[:,0],bres[:,1],c='r',marker='.')
ax1.set_xlim([0,96])
ax1.set_ylim([0,96])
absc=[]
ord=[]
for point in bres :
	absc+=[np.linalg.norm(point-bres[0,:])]
	ord+=[map[point[1],point[0]]]

absc=np.array(absc)
absc=absc*18/96
ax2.plot(absc,ord)

plt.show()

with open('plot_4x0.txt','w') as f :
	for i in range(len(absc)) :
		f.write('%f \t %f\n'%(absc[i],ord[i]))




				
        


