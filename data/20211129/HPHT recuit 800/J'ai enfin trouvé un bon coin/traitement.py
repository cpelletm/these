import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


plt.figure(num=1,figsize=(4.5,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)


def plot_scan_1x1x1x1():
	xmin=192
	xmax=330

	x,y=extract_data('scan 1x1x1x1 0,0',ycol=3)
	y=y/max(y)
	x=x*35-8
	plt.plot(x[xmin:xmax],y[xmin:xmax],label='region A',lw=2)

	x,y=extract_data('scan 1x1x1x1 0,10',ycol=3)
	y=y/max(y)
	x=x*35-8
	plt.plot(x[xmin:xmax],y[xmin:xmax],label='region B',lw=2)

	plt.legend()


def plot_T1_bruts():
	x,y=extract_data('T1 0B/T1 brut 0,5',ycol=1)
	x=x*1000
	y=y-min(y)
	y=y/max(y)
	plt.plot(x,y)

	x,y=extract_data('T1 0B/T1 brut 0,10 fit stretch',ycol=1)
	x=x*1000
	y=y-min(y)
	y=y/max(y)
	plt.plot(x,y)

	x,y=extract_data('T1 1x1x1x1/T1 brut 0,5 fit exp',ycol=1)
	x=x*1000
	y=y-min(y)
	y=y/max(y)
	plt.plot(x,y)

	x,y=extract_data('T1 1x1x1x1/T1 brut 0,10 fit exp',ycol=1)
	x=x*1000
	y=y-min(y)
	y=y/max(y)
	plt.plot(x,y)

plt.show()