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

def fit_exp_vs_stretch():
	# x,y=extract_data('T1 sur le rose, orange et vert=121 rouge =22 bleu =1x',ycol=5)
	# x,y=extract_data('T1 0B ADM 15 1',ycol=5)

	# x,y=extract_data('T1 ADM-15-4 1x1x1x1',ycol=5)	
	x,y=extract_data('T1 0B ADM-15-4',ycol=5)

	nmax=-1
	nmax=len(x)//4
	y=y/max(y)
	x=x*1e3
	x=x
	y=y
	plt.plot(x[:nmax],y[:nmax],'o',markerfacecolor='None',mew=0.8,ms=5,label='Experimental data')
	popt,yfit=exp_fit_zero(x,y)
	plt.plot(x[:nmax],yfit[:nmax],lw=2,label=r'exp(-$t/\tau$)')
	popt,yfit=stretch_exp_fit_zero(x,y)
	plt.plot(x[:nmax],yfit[:nmax],lw=2,label=r'exp(-$\sqrt{t/\tau}$)')

	plt.yscale('log')
	# plt.xscale('log')
fit_exp_vs_stretch()


def fit_0B_vs_pas0B():
	x,y=extract_data('T1 0B ADM-150-1',ycol=5)
	y=y/max(y)
	x=x*1e3
	plt.plot(x,y,'o',markerfacecolor='None',mew=0.8,ms=5,label=r'$B=0$')
	# popt,yfit=exp_fit_zero(x,y)
	popt,yfit=stretch_et_phonons(x,y,T1ph=5,fixed=True)
	print(1-R2(y,yfit))
	plt.plot(x,yfit,lw=2,color=color(1))

	x,y=extract_data('T1 1x1x1x1 avg ADM-150-1',ycol=1)
	y=y/max(y)
	plt.plot(x,y,'x',mew=0.8,ms=5,label=r'$B\neq0$',color=color(2))
	# popt,yfit=exp_fit_zero(x,y)
	popt,yfit=stretch_et_phonons(x,y,T1ph=5,fixed=True)
	print(1-R2(y,yfit))
	plt.plot(x,yfit,lw=2,color=color(1))


	plt.yscale('log')

# fit_0B_vs_pas0B()
plt.legend()
plt.show()