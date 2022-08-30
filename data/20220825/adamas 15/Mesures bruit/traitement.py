import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


# x,y=extract_data('Mesure près V=0 plus')
# s=sigma(y)
# print(s,s*0.06/3*35*1e-4)


def allan_test():
	import allantools
	y = allantools.noise.white(10000)
	# x = np.linspace(1,10000,10000)
	# psd(x,y,plot=True)
	(taus, adevs, errors, ns) = allantools.oadev(y)
	# plt.plot(taus,adevs)
	# plt.yscale('log')
	# plt.xscale('log')
	# plt.show()

# allan_test()

def plot_allan_dev(sensimag=True):
	import allantools
	plt.yscale('log')
	plt.xscale('log')
	plt.figure(num=1,figsize=(4.5,3),dpi=80)
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
	conv0=0.06/3*35*1e-4*1e6
	data=data*conv0
	psd(t,data,plot=True)
	# if sensimag :
	# 	data=data*conv0
	# taus2, ad, ade, ns=allantools.oadev(data, rate=f, data_type='phase', taus='all')
	# print(len(ad))
	# y=ad
	# plt.plot(taus2[nmin:nmax],y[nmin:nmax], label='0B slope')

	# [a,b],yfit=lin_fit(log(taus2[nmin:nmax]),log(y[nmin:nmax]))
	# print(a,b)
	# yfit=exp(b)*(taus2[nmin:nmax]**(a))

	# plt.plot(taus2[nmin:nmax],yfit)


	# t,data=extract_data('mesure bruit 100 000 s')
	# t=t[12500:99500]
	# data=data[12500:99500]
	# N=len(t)
	# dt=t[1]-t[0]
	# f=1/dt
	# tmax=t[-1]
	# conv0=0.06/3*35*1e-4*1e6
	# if sensimag :
	# 	data=data*conv0
	# taus2, ad, ade, ns=allantools.oadev(data, rate=f, data_type='phase', taus='all')
	# print(len(ad))
	# y=np.sqrt(ad)
	# plt.plot(taus2[nmin:nmax],y[nmin:nmax], label='0B slope')



	t,data=extract_data('Mesure sur pente microonde')
	N=len(t)
	dt=t[1]-t[0]
	f=1/dt
	tmax=t[-1]
	convmW=0.04/4.8*35*1e-4
	# data=data*conv0
	# psd(t,data,plot=True)
	# if sensimag :
	# 	data=data*convmW
	# taus2, ad, ade, ns=allantools.oadev(data, rate=f, data_type='phase', taus='all')
	# print(len(ad))
	# y=np.sqrt(ad)
	# plt.plot(taus2[nmin:nmax],y[nmin:nmax],label='MW slope')

	# plt.legend()
	plt.show()

# plot_allan_dev()

def plot_SNR():
	plt.figure(num=1,figsize=(4.5,3),dpi=80)
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)
	plt.yscale('log')
	plt.xscale('log')

	


	t,y=extract_data('Mesure près V=0 plus')
	N=len(t)
	signal=0.1 #\muT
	conv0=0.06/3*35*1e-4*1e6
	y=y*conv0

	dt=t[1]-t[0]
	Tmax=t[-1]-t[0]
	t_lowpass=(3*2)*1e-3
	nbins=100
	taus=np.geomspace(5e-2,Tmax/2,nbins)
	n_taus=np.floor(taus/dt)
	SNRs=np.zeros(nbins)

	for i in range(nbins):
		n=int(n_taus[i])
		k=int(N/n)
		SNR=0
		for j in range(k):
			data=y[j*n:(j+1)*n]
			dev=sigma(data)
			SNR+=signal*sqrt(taus[i]/t_lowpass)/dev
		SNR=SNR/k
		SNRs[i]=SNR
	plt.plot(taus,SNRs, label='0B slope')

	# t,y=extract_data('Mesure sur pente microonde')
	# convmW=0.04/4.8*35*1e-4*1e6
	# y=y*convmW
	# for i in range(nbins):
	# 	n=int(n_taus[i])
	# 	k=int(N/n)
	# 	SNR=0
	# 	for j in range(k):
	# 		data=y[j*n:(j+1)*n]
	# 		dev=sigma(data)
	# 		SNR+=signal*sqrt(taus[i]/t_lowpass)/dev
	# 	SNR=SNR/k
	# 	SNRs[i]=SNR
	# plt.plot(taus,SNRs,label='MW slope')

	# plt.legend()

	plt.plot(taus,np.sqrt(taus)/2)
	ylims=plt.ylim()	
	plt.ylim([ylims[0],10])
	plt.show()

plot_SNR()

def plot_data_raw():
	plt.figure(num=1,figsize=(4.5,3),dpi=80)
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)
	plt.locator_params(axis='x', nbins=5)
	plt.locator_params(axis='y', nbins=5)

	t,data=extract_data('Mesure près V=0 plus')
	conv0=0.06/3*35*1e-4*1e6
	data=data*conv0
	plt.plot(t,data,label='0B slope')

	# t,data=extract_data('Mesure sur pente microonde')
	# convmW=0.04/4.8*35*1e-4*1e6
	# data=data*convmW
	# plt.plot(t,data,label='MW slope')

	# plt.legend()
	plt.show()

# plot_data_raw()

# plot_data_raw()