import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('C:\\Users\\cleme\\OneDrive\\Documents\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *




def plot_sensi_P1():
	plt.figure(num=1,figsize=(4,3),dpi=80)
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)
	plt.locator_params(axis='x', nbins=5)
	plt.locator_params(axis='y', nbins=5)
	x=np.logspace(-3,3,300)
	DeltaNu=160+16*x

	N=1e-12*1.75e23*1e-6*1e-1*x

	hbar=1.05e-34
	g=2
	muB=9.27e-24
	C=1e-3

	eta=hbar/(g*muB*C)*sqrt(DeltaNu/N)
	eta=eta*1e9

	plt.plot(x,eta)
	plt.yscale('log')
	plt.xscale('log')
	plt.show()

def max_sensi_single_spin():
	DeltaNu=100

	N=1

	hbar=1.05e-34
	g=2
	muB=9.27e-24
	C=1e-2
	eta=hbar/(g*muB*C)*sqrt(DeltaNu/N)
	eta=eta*1e9
	print(eta)

max_sensi_single_spin()

def plot_PL_CR_simu():
	plt.figure(num=1,figsize=(4,3),dpi=80)
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)
	# plt.locator_params(axis='x', nbins=5)
	# plt.locator_params(axis='y', nbins=5)
	x=np.logspace(-3,3,300)
	x=np.linspace(0,200,201)
	y=1-0.05*lor(x,x0=100,sigma=5,norm=False)
	plt.plot(x,y)
	plt.show()

# plot_PL_CR_simu()