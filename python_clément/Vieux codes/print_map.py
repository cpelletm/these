import numpy as np
import matplotlib.pyplot as plt


with open("map_1_gonio.txt",'r') as f:
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



thetaAxis=np.linspace(0,12,24)
phiAxis=np.linspace(0,12,24)

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
thetaphi=np.ones((12,70))
c=ax.pcolor(phiAxis, thetaAxis, thetaphi)
cb=fig.colorbar(c,ax=ax)
thetaphi=np.array(xy)
c=ax.pcolor(phiAxis, thetaAxis, thetaphi)
cb.update_normal(c)
print(dir(cb))
plt.show()