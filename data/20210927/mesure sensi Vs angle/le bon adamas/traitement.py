import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('C:\\Users\\cleme\\OneDrive\\Documents\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(4.5,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)


def plot_sensi_angulaire():
	x=[]
	y=[]
	with open("sensi.txt",'r',encoding = "ISO-8859-1") as f:
		f.readline()
		f.readline()
		f.readline()
		f.readline()
		while True:
			try :
				[a,b]=f.readline().split()
				x+=[float(a)]
				y+=[float(b)]
			except :
				break
	x=np.array(x)
	y=np.array(y)
	y=y*sqrt(2)
	errbars=0.09*y
	plt.errorbar(x,y,lw=2,elinewidth=1.5,ecolor=color(0),yerr=errbars,capsize=4)
	plt.ylim([0,170])

# plot_sensi_angulaire()

def plot_sensi_alternee():
	fname='sensi joli gaussiennes'
	scale=1.5
	fig,ax=plt.subplots(2,figsize=(3*scale,4*scale),dpi=80)
	ax1=ax[1]
	ax2=ax[0]
	dB=1e-2*3.5e-3
	x1,y1=extract_data(fname,xcol=0,ycol=1)
	x2,y2=extract_data(fname,xcol=2,ycol=3)
	x3,y3=extract_data(fname,xcol=4,ycol=5)
	m1=hist_mean(x1,y1)
	m2=hist_mean(x2,y2)
	ratio=dB/abs(m2-m1)
	print(ratio)
	x1=x1*ratio*1e6
	x2=x2*ratio*1e6
	# y3=y3*ratio*1e6
	sigma=hist_sigma(x1,y1)
	print(sigma*1e-6*np.sqrt(0.006))
	ax1.plot(x1,y1,'o',markerfacecolor="None",mew=0.7*scale,ms=4*scale,color=color(0))
	popt,yfit,pcov=gauss_fit(x1,y1,err=True)
	print(popt)
	print(np.sqrt(pcov))
	plt.plot(x1,yfit,color=color(1),lw=1.5*scale)
	ax1.plot(x2,y2,'o',markerfacecolor="None",mew=0.7*scale,ms=4*scale,color=color(0))
	popt,yfit=gauss_fit(x2,y2)
	print(popt)
	plt.plot(x2,yfit,color=color(1),lw=1.5*scale)
	ax2.plot(x3,y3,lw=0.7*scale)
	ax1.tick_params(labelsize=16)
	ax1.set_ylabel(r'Histogram (counts)',fontsize=20)
	ax1.set_xlabel(r'Measured magnetic field ($\mu$T)' ,fontsize=20)
	ax2.tick_params(labelsize=16)
	ax2.set_xlabel(r'time (s)',fontsize=20)
	ax2.set_ylabel(r'Measured magnetic field ($\mu$T)' ,fontsize=20)
	ax2.set_ylim([-0.8,0.5])
	plt.show()

# plot_sensi_alternee()


def plot_scan():
	fname='scan 100 20 deg from 100'
	x,y=extract_data(fname,ycol=3)
	y=y/max(y)
	x=x*65/2
	x=x+0.35-7.91
	# plt.plot(x,y,'o-',lw=1.5,markerfacecolor='None')
	plt.plot(x,y,lw=1.5,label=r'$B \nparallel [100]$',color=color(1))
	
	
	fname='scan 100'
	x,y=extract_data(fname,ycol=3)
	y=y/max(y)
	x=x*65/2
	x=x-7.91
	# plt.plot(x,y,'s-',lw=1.5,markerfacecolor='None')
	plt.plot(x,y,lw=1.5,label=r'$B \parallel [100]$',color=color(0))

	plt.legend()

# plot_scan()


def plot_T1_exp():
	fname='T1 0B nuit'
	nmax=100
	x,y=extract_data(fname,ycol=5)
	x=x*1e3
	y=y/max(y)
	plt.plot(x[:nmax],y[:nmax],'x',markerfacecolor="None",ms=7,mew=1.5,label='Experimental Data',color=color(0))
	popt,yfit,pcov=exp_fit_zero(x,y,err=True)
	print(popt)
	print(np.sqrt(pcov))
	plt.plot(x[:nmax],yfit[:nmax],lw=3,label=r'exp($-t/\tau$)',color=color(1))
	popt,yfit,pcov=stretch_exp_fit_zero(x,y,err=True)
	print(popt)
	print(np.sqrt(pcov))
	plt.plot(x[:nmax],yfit[:nmax],lw=3,label=r'exp($-\sqrt{t/\tau}$)',color=color(2))
	# plt.yscale('log')
	# plt.xscale('log')
	plt.legend()

# plot_T1_exp()

def plot_ESR_OB():
	x,y=extract_data('ESR 0B')
	# y=y/max(y)
	plt.plot(x[35:265],y[35:265])

plot_ESR_OB()
plt.show()