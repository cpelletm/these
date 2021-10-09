import numpy as np
import matplotlib.pyplot as plt


with open("map_8_gonio.txt",'r') as f:
	xy=[]
	line=f.readline()
	while line != "" :
		line=line.split()
		phi=[]
		for v in line :
			phi+=[float(v)]
		xy+=[phi]
		line=f.readline()



def linfit(x,y): #retourne a,b
	A=np.vstack([x,np.ones(len(x))]).T
	a,b=np.linalg.lstsq(A,y,rcond=None)[0]
	return(a,b)


thetaphi=np.array(xy)

thetaAxis=np.linspace(0,12,len(thetaphi[:,0]))
phiAxis=np.linspace(0,12,len(thetaphi[0,:]))

#x=np.arange(29)
#coefs=[]
#origins=[]
#for i in range(len(thetaphi[0,:])):
	#y=thetaphi[:,i]
	#a,b=a,b=linfit(x,y)
	#coefs+=[a]
	#origins+=[b]
#a=sum(coefs)/len(coefs)
#b=sum(origins)/len(origins)

#for i in range(len(thetaphi[0,:])):
#	y=thetaphi[:,i]
#	thetaphi[:,i]=y-a*x+b

#thetaphi=thetaphi/np.amax(thetaphi)
#thetaphi=np.log(thetaphi)


fig,ax=plt.subplots()


c=ax.pcolormesh(phiAxis, thetaAxis, thetaphi, cmap='plasma')
cb=fig.colorbar(c,ax=ax)


plt.show()