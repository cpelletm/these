import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

# Pour la figure en fonction du décalage en fréquence, voir le traitement.py dans T1/


plt.figure(num=1,figsize=(4.5,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

def find_B():
	fnames,fval=extract_glob('ESR',LastValIndex=-5)
	n=len(fnames)
	x=np.linspace(0.8,5,n)
	freqp=2879.6100403000905-10.350382035600058*x+8.72563530864743*x**2-0.5448652051415266*x**3+0.008459469208990177*x**4
	freqm=2862.3732486672525+5.336405357793713*x+0.4892478887834715*x**2+0.4361255116793501*x**3-0.047696861387582994*x**4

	fps=[]
	fms=[]
	for i in range(n):
		x,y=extract_data(fnames[i])
		fp=x[find_local_max(x,y,freqp[i])]
		fm=x[find_local_max(x,y,freqm[i])]
		fps+=[fp]
		fms+=[fm]

	# plt.plot(fval,freqm)
	# plt.plot(fval,freqp)
	plt.plot(fval,fms,'x')
	plt.plot(fval,fps,'x')

	fps=[]
	fms=[]
	Bs=(np.array(fval)-0.17)*31
	for i in range(n):
		B=[Bs[i],0,0]
		H=NVHamiltonian(B=B,E=4,c=5)
		fp,fm=H.transitions()
		fps+=[fp]
		fms+=[fm]

	plt.plot(fval,fms)
	plt.plot(fval,fps)

# find_B()

def plot_ESR_freqs():
	fnames,fval=extract_glob('ESR',LastValIndex=-5)
	n=len(fnames)
	x=np.linspace(0.8,5,n)
	freqp=2879.6100403000905-10.350382035600058*x+8.72563530864743*x**2-0.5448652051415266*x**3+0.008459469208990177*x**4
	freqm=2862.3732486672525+5.336405357793713*x+0.4892478887834715*x**2+0.4361255116793501*x**3-0.047696861387582994*x**4

	fps=[]
	fms=[]
	for i in range(n):
		x,y=extract_data(fnames[i])
		fp=x[find_local_max(x,y,freqp[i])]
		fm=x[find_local_max(x,y,freqm[i])]
		fps+=[fp]
		fms+=[fm]

	# plt.plot(fval,freqm)
	# plt.plot(fval,freqp)
	Bs=(np.array(fval)-0.17)*31
	nmax=180
	plt.plot(Bs[:nmax],fms[:nmax],lw=2)
	plt.plot(Bs[:nmax],fps[:nmax],lw=2)

# plot_ESR_freqs()


def plot_T1_raw():
	fnames,fval=extract_glob('T1',LastValIndex=-5)
	n=len(fnames)
	taus=[]
	for i in range(n):
		x,y=extract_data(fnames[i],ycol=5)
		T1ph=0.003626
		popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
		taus+=[1/popt[1]]
	Bs=(np.array(fval)-0.17)*31
	nmax=180
	plt.plot(Bs[:nmax],taus[:nmax],'o',markerfacecolor='none',ms=3,mew=0.7)

# plot_T1_raw()

def fit_T1_1classe():
	x,y=extract_data('T1 1 classe condition série',ycol=5)
	x=x*1e3
	y=y/max(y)
	plt.plot(x,y,'x')
	# popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.8,fixed=False)
	# print(estim_error(y,yfit))
	# for T1ph in np.linspace(1e-3,5e-3,100):
	# 	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	# 	print('T1ph=%f,error=%f'%(T1ph,estim_error(y,yfit)))
	# T1ph=0.003626*1e3
	T1ph=5
	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	plt.plot(x,yfit,lw=2)
	print(popt,1/popt[1]*1e3)

# fit_T1_1classe()

def plot_ESR_0B():
	# x,y=extract_data('ESR 0B -20 et -30 dB',ycol=1)
	# y=y/max(y)
	# plt.plot(x,y)
	x,y=extract_data('ESR 0B -20 et -30 dB',ycol=5)
	y=y/max(y)
	plt.plot(x,y,color=color(3))

plot_ESR_0B()

def plot_ESR_1x4():
	x,y=extract_data('ESR/V=5.000000 V')
	nmin=300
	nmax=450
	plt.plot(x[nmin:nmax],y[nmin:nmax])
	# popt,yfit=gauss_fit(x[nmin:nmax],y[nmin:nmax])
	# plt.plot(x[nmin:nmax],yfit)
	# plt.plot(y)

# plot_ESR_1x4()

def plot_ESR_0B_Vs_1classe():
	x,y=extract_data('ESR 0B -20 et -30 dB',ycol=5)
	y=y/max(y)
	x=x-0
	plt.plot(x,y)
	x,y=extract_data('ESR 1 classe pas loin 111')
	y=y-min(y)
	y=y/max(y)
	x=x-2740+2865
	plt.plot(x,y)

# plot_ESR_0B_Vs_1classe()

plt.show()