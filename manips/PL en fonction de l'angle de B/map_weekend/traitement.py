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

thetas=np.linspace(-6,6,len(map[0,:]))
phis=np.linspace(-9,9,len(map[:,0]))


fig,ax=plt.subplots()

c=ax.pcolormesh(phis, thetas, map)
ax.tick_params(labelsize=15)
ax.set_xlabel(r'$\phi (°)$',fontsize=25)
ax.set_ylabel(r'$\theta (°)$',fontsize=25)
cb=fig.colorbar(c,ax=ax)
cb.ax.tick_params(labelsize=15)
cb.set_label('PL (arb.)',fontsize=25)
plt.show()




				
        


