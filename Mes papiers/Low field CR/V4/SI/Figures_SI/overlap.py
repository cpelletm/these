import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)


def gaussian(x,sigma,x0):
	return np.exp(-(x-x0)**2/(2*sigma**2))

def lorentzian(x,sigma,x0):
	return 1/(1+(x-x0)**2/sigma**2)

def plot_overlap():
	x=np.linspace(2650,2750,500)
	y1=gaussian(x,6,2692)
	y2=gaussian(x,6,2708)
	y3=y1*y2
	plt.plot(x,y1,label='NV1 spectral response')
	plt.plot(x,y2,label='NV2 spectral response')
	l3=plt.plot(x,y3,label='spectral overlap')
	plt.fill_between(x,0,y3,color=color(2))
	plt.legend()


def compute_overlap():
	n=500
	x=np.linspace(-10,10,n)
	deltas=np.linspace(-10,10,n)
	ol=np.zeros(n)
	for i in range(n):
		delta=deltas[i]
		y1=lorentzian(x,1,-delta/2)
		y2=lorentzian(x,1,+delta/2)
		y3=y1*y2
		ol[i]=integration(x,y3)

	ol=ol/max(ol)
	plt.plot(x,ol)
	popt,yfit=lor_fit(x,ol)
	plt.plot(x,yfit)
	print(popt)
compute_overlap()

plt.show()