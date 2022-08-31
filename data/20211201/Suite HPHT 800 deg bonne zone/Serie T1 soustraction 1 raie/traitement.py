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

def plot_T1_ligne():

	data=[]
	for i in range(n) :
		x,y=extract_data('x=0,y=%.6f'%(xs[i]),xcol=4,ycol=5)
		popt,yfit=stretch_arb_exp_fit_zero(x,y)
		data+=[popt[2]]
		print(popt[1])

	plt.plot(xs,data)


def plot_T1():
	xmin=0
	xmax=150
	x,y=extract_data('x=0,y=2.413793',ycol=5)
	y=y/max(y)
	plt.plot(x[xmin:xmax],y[xmin:xmax],label='region A',lw=2)

	x,y=extract_data('x=0,y=10.000000',ycol=5)
	y=y/max(y)
	plt.plot(x[xmin:xmax],y[xmin:xmax],label='region B',lw=2)
	plt.legend()

plot_T1()

plt.show()
