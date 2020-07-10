import numpy as np
import matplotlib.pyplot as plt


with open("map_2.txt",'r') as f:
	xy=[]
	line=f.readline()
	while line != "" :
		line=line.split()
		phi=[]
		for v in line :
			phi+=[float(v)]
		xy+=[phi]
		line=f.readline()


thetaphi=np.array(xy)

thetaAxis=np.linspace(50,80,30)
phiAxis=np.linspace(200,170,32)

plt.plot(thetaphi[:,0])
#plt.pcolor(phiAxis, thetaAxis, thetaphi)
plt.show()