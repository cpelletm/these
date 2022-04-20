import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *



plt.figure(num=1,figsize=(3,2),dpi=80)
plt.xticks(fontsize=11)
plt.yticks(fontsize=12)



def plot_ESR_1x1x1x1():
	x,y=extract_data('T1 1x1x1x1/ESR 3V')
	n=len(x)//2
	x=x[:n]
	y=y[:n]
	y=y/max(y)
	plt.plot(x,y)


def plot_T1_fit():
	fnames,fval=extract_glob('T1 1x1x1x1/T1')
	i=100
	x,y=extract_data(fnames[i],ycol=5)
	y=y*100
	x=x*1e3
	plt.plot(x,y,'o',markerfacecolor='None',mew=0.8,ms=5)
	# popt,yfit=exp_fit_zero(x,y)
	# plt.plot(x,yfit)
	# popt,yfit=stretch_exp_fit_zero(x,y)
	# plt.plot(x,yfit)
	T1ph=0.003626*1e3
	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	plt.plot(x,yfit,lw=2)

plot_T1_fit()

def plot_PL_1x1x1x1():
	x,y=extract_data('T1 1x1x1x1/scan 1x1x1x1',ycol=3)
	# x,y=extract_data('scan align random',ycol=3)


	B=(x+0.17)*86.4/3
	i0=find_elem(-0.17,x)
	i2=find_elem(2,x)



	# y=y[i2:i0]
	# B=B[i2:i0]
	y=y/max(y)

	plt.plot(B,y)


# plot_PL_1x1x1x1()

def plot_T1_1x1x1() :

	fnames,fval=extract_glob('T1 1x1x1x1/T1')
	n=len(fval)
	taus=np.zeros(n)

	Bs=[np.array([78.55,31.8,16.86])*(x-0.17)/2.8 for x in fval]

	Bamps=np.array([norm(B)*np.sign(B[0]) for B in Bs])

	for i in range(n):
		fname=fnames[i]
		x,y=extract_data(fname,ycol=5)
		T1ph=0.003626
		popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
		taus[i]=popt[1]

	nmin=106
	nmax=173
	x=Bamps[nmin:nmax]

	y=1/taus[nmin:nmax]



	plt.plot(x,y)
	# popt,yfit=lor_fit(x,y,x0=0.00001,amp=1600,ss=50,sigma=6) #Ok je fais full merde
	# print(popt)
	# plt.plot(x,yfit)


# plot_T1_1x1x1()

def plot_T1_100() :
	fnames,fval=extract_glob('T1 100 align 3/T1')
	fval.remove(fval[194])
	fnames.remove(fnames[194])
	fval.remove(fval[178])
	fnames.remove(fnames[178])
	n=len(fval)
	taus=np.zeros(n)
	Bs=(np.array(fval)-0.16)*29


	nmax=107
	for i in range(n):
		fname=fnames[i]
		x,y=extract_data(fname,ycol=5)
		T1ph=0.003626
		popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
		taus[i]=popt[1]

	x=-Bs[:nmax]
	y=1/taus[:nmax]
	# y=y-y[-1]
	# y=y/max(y)
	# plt.plot(x,y)

	# popt,yfit=lor_fit(x,y,x0=0.00001)
	# print(popt)
	# plt.plot(x,yfit)


def plot_PL_100():
	x,y=extract_data('T1 100 align 3/scan EM',ycol=3)
	B=(x+0.16)*29
	i0=find_elem(-0.12,x)
	i2=find_elem(2,x)



	y=y[i2:i0]
	x=B[i2:i0]
	y=y/max(y)

	plt.plot(x,y)

plt.show()

