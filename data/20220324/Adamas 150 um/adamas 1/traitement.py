import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

# Pour la figure en fonction du décalage en fréquence, voir le traitement.py dans T1/

scale=1
plt.figure(num=1,figsize=(3*scale,2*scale),dpi=80)
plt.xticks(fontsize=10+1.5*scale)
plt.yticks(fontsize=10+1.5*scale)

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

plot_ESR_freqs()


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
	x,y=extract_data('T1 1 classe 111',ycol=5)
	plt.plot(x,y,'x')
	# popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.8,fixed=False)
	# print(estim_error(y,yfit))
	# for T1ph in np.linspace(1e-3,5e-3,100):
	# 	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	# 	print('T1ph=%f,error=%f'%(T1ph,estim_error(y,yfit)))
	T1ph=0.003626
	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	plt.plot(x,yfit)
	print(popt,1/popt[1])



plt.show()