import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(4.5,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

def plot_simu_PL():

	def PL(T1):
		Gamma1=1/T1
		GammaLas=1e3
		rho0=(Gamma1+GammaLas)/(3*Gamma1+GammaLas)
		rh0pm=2*Gamma1/(3*Gamma1+GammaLas)
		PL=1*rho0+0.7*rh0pm
		return PL

	Bs=np.linspace(0,20,200)
	T1s=0.003-lor(Bs,x0=10,sigma=1,norm=False)*0.001
	ax1=plt.gca()
	ax2=ax1.twinx()
	l1=ax2.plot(Bs,PL(T1s),label=r'PL')

	l2=ax1.plot(Bs,1/T1s,color=color(3),label=r'1/$T_1$')
	lns = l1+l2
	labs = [l.get_label() for l in lns]
	ax1.legend(lns, labs, loc=0)
	plt.show()

def plot_T1():
	ts=np.linspace(0,10,200)
	plt.plot(ts,np.exp(-ts/2), label=r'$T_1$=2 ms')
	plt.plot(ts,np.exp(-ts/3), label=r'$T_1$=3 ms')
	plt.legend()
	plt.show()

plot_T1()