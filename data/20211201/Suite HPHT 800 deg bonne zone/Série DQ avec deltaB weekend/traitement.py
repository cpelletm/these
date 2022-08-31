import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

#les x et y sont inversés pour cette série

plt.figure(num=1,figsize=(4.5,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

n=30
xs=np.linspace(0,10,n)

def plot_DQ_contrast():
	data=[]
	for i in range(n) :
		x,y=extract_data('x=0,y=%.6f'%(xs[i]),xcol=2,ycol=3)
		PL=sum(y)
		x,y=extract_data('x=0,y=%.6f'%(xs[i]))
		y=y/PL

		data+=[sum(y[495:527])-sum(y[527:560])]

	plt.plot(xs,data)


def plot_DQ_PL():
	xmin=350
	xmax=700
	x,y=extract_data('x=0,y=2.413793',ycol=3)
	y=y/max(y)-0.0004
	x=x*35-4
	plt.plot(x[xmin:xmax],y[xmin:xmax],label='region A',lw=2)
	x,y=extract_data('x=0,y=10.000000',ycol=3)
	y=y/max(y)
	x=x*35-4
	plt.plot(x[xmin:xmax],y[xmin:xmax],label='region B',lw=2)
	plt.legend()

plot_DQ_PL()
plt.show()
