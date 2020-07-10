import numpy as np
import matplotlib.pyplot as plt


V=[5.2,5.3,5.4,5.5,6.5,6.6,6.7,6.8,6.9]
V=np.array(V)
p1=[858,860,860,862,863,863,861,858,858]
p2=[882,880,880,877,874,877,879,880,881]
p3=[909,911,913,915,927,924,924,923,923]
p4=[933,930,930,929,936,938,941,943,943]
peaks=[[p1[i],p2[i],p3[i],p4[i]] for i in (0,1,2,3)]
peaks+=[[p2[i],p1[i],p4[i],p3[i]] for i in (4,5,6,7,8)]

def lin_fit(x,y) :
	A=np.vstack([x,np.ones(len(x))]).T
	a,b = np.linalg.lstsq(A, y, rcond=None)[0]
	return(a,b,a*x+b)

peaks=np.array(peaks)

def plot_levels() :
	plt.plot(V,peaks[:,0],label='0')
	plt.plot(V,peaks[:,1],label='1')
	plt.plot(V,peaks[:,2],label='2')
	plt.plot(V,peaks[:,3],label='3')

def plot_delta():
	delta1=peaks[:,2]-peaks[:,3]
	plt.plot(V,delta1)
	a,b,yfit=lin_fit(V,delta1)
	plt.plot(V,yfit,label='%fx+%f'%(a,b))

plot_delta()
plt.legend()
plt.show()