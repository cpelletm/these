import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


plt.figure(num=1,figsize=(4.5,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

# print(glob.glob('**/*.csv',recursive=True))


def plot_PL_100():
	xmin=230
	xmax=285
	x,y=extract_data("adamas 2/scan 100 j'ai compris l'astuce je suis trop refait.csv",ycol=3)
	x=x*35-5.4
	y=y/max(y)
	plt.plot(x[xmin:xmax],y[xmin:xmax],label='ADM-15-1',lw=2)

	x,y=extract_data('le bon adamas/scan 100.csv',ycol=3)
	x=x*35-6.2
	y=y/max(y)
	plt.plot(x[xmin:xmax],y[xmin:xmax],label='ADM-15-4',lw=2)

def plot_PL_1x1x1x1():
	xmin=300
	xmax=740
	x,y=extract_data('adamas 2/scan 20 deg from 100.csv',ycol=3)
	x=x*35-5.8
	y=y/max(y)
	plt.plot(x[xmin:xmax],y[xmin:xmax],label='ADM-15-1',lw=2)

	xmin=150
	xmax=370
	x,y=extract_data('le bon adamas/scan 100 20 deg from 100',ycol=3)
	x=x*35-5.2
	y=y/max(y)
	plt.plot(x[xmin:xmax],y[xmin:xmax],label='ADM-15-4',lw=2)


def plot_T1_1x1x1x1():
	x,y=extract_data('adamas 2/T1 splitté soustraction long',ycol=5)
	x=x*1e3
	y=y/max(y)
	plt.plot(x,y,label='ADM-15-1',lw=2)

	x,y=extract_data('le bon adamas/T1 1x1x1x1',ycol=5)	
	x=x*1e3
	y=y/max(y)
	plt.plot(x,y,label='ADM-15-4',lw=2)
plot_T1_1x1x1x1()


def plot_T1_100():
	x,y=extract_data('adamas 2/T1 0B soustraction',ycol=5)
	x=x*1e3
	y=y/max(y)
	plt.plot(x,y,label='ADM-15-1',lw=2)

	x,y=extract_data('le bon adamas/T1 0B nuit',ycol=5)
	x=x*1e3
	y=y/max(y)
	plt.plot(x,y,label='ADM-15-4',lw=2)
# plot_T1_100()

plt.legend()
plt.show()