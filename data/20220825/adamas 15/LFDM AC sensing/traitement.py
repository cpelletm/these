import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(4.5,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

# print(glob.glob('*.csv'))

def plot_AC():
	xmin=150
	xmax=370
	for ycol in [1,5,9,13,17]:
		x,y=extract_data('V_AC from 1 V to 0.2 V.csv',ycol=ycol)
		x=x*35+5.9
		plt.plot(x[xmin:xmax],y[xmin:xmax],color=color(0))

def plot_DC():
	xmin=150
	xmax=370
	x,y=extract_data('V_AC from 1 V to 0.2 V.csv',ycol=5)
	x=x*35+5.9
	plt.plot(x[xmin:xmax],y[xmin:xmax],color=color(0))

plot_DC()

plt.show()