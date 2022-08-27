import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


# x,y=extract_data('Mesure près V=0 plus')
# s=sigma(y)
# print(s,s*0.06/3*35*1e-4)


def plot_allan_dev(sensimag=True):
	import allantools
	plt.yscale('log')
	plt.xscale('log')
	plt.figure(num=1,figsize=(6,4),dpi=80)
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)
	# plt.locator_params(axis='x', nbins=5)

	nmin=15
	nmax=-100

	t,data=extract_data('Mesure près V=0 plus')
	N=len(t)
	dt=t[1]-t[0]
	f=1/dt
	tmax=t[-1]
	conv0=0.06/3*35*1e-4
	if sensimag :
		data=data*conv0
	taus2, ad, ade, ns=allantools.oadev(data, rate=f, data_type='phase', taus='all')
	print(len(ad))
	y=np.sqrt(ad)
	plt.plot(taus2[nmin:nmax],y[nmin:nmax], label='0B slope')

	t,data=extract_data('Mesure sur pente microonde')
	N=len(t)
	dt=t[1]-t[0]
	f=1/dt
	tmax=t[-1]
	convmW=0.04/4.8*35*1e-4
	if sensimag :
		data=data*convmW
	taus2, ad, ade, ns=allantools.oadev(data, rate=f, data_type='phase', taus='all')
	print(len(ad))
	y=np.sqrt(ad)
	plt.plot(taus2[nmin:nmax],y[nmin:nmax],label='MW slope')

	plt.legend()
	plt.show()

# plot_allan_dev()

def plot_data_raw():
	plt.figure(num=1,figsize=(6,4),dpi=80)
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)

	t,data=extract_data('Mesure près V=0 plus')
	conv0=0.06/3*35*1e-4*1e6
	data=data*conv0
	plt.plot(t,data,label='0B slope')

	t,data=extract_data('Mesure sur pente microonde')
	convmW=0.04/4.8*35*1e-4*1e6
	data=data*convmW
	plt.plot(t,data,label='MW slope')

	plt.legend()
	plt.show()


plot_data_raw()