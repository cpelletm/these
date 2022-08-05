import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.locator_params(axis='x', nbins=5)





fnames,fval=extract_glob('ESR')
# x,y=extract_data(fnames[20])
# plt.plot(x,y)

n=67
fval=fval[:n]
transis=np.zeros((n,2))
for i in range(n):
	fname=fnames[i]
	x,y=extract_data(fname)
	cs=find_ESR_peaks(x,y,threshold=0.5)
	if len(cs)==2 :
		cs=find_ESR_peaks(x,y,threshold=0.5,precise=True)
		transis[i,:]=cs
	else :
		transis[i,:]=[np.nan,np.nan]

# plt.plot(transis,'x')

nbeg=20

nmin=38
nmax=51

absc=fval[nbeg:nmin]+fval[nmax:]
transi1=list(transis[nbeg:nmin,0])+list(transis[nmax:,1])
transi2=list(transis[nbeg:nmin,1])+list(transis[nmax:,0])
plt.plot(absc,transi1,'x')
plt.plot(absc,transi2,'x')

x=np.array(fval[nbeg:])
popt,yfit=lin_fit(absc,transi1)
print(popt)
E1=popt[0]*x+popt[1]
plt.plot(x,E1)

popt,yfit=lin_fit(absc,transi2)
print(popt)
E2=popt[0]*x+popt[1]
plt.plot(x,E2)


def plot_single_T1(i=54):
	fnames,fval=extract_glob('T1')
	x,y=extract_data(fnames[i],ycol=5)
	y=y/max(y)
	plt.plot(x,y,'x',label='i=%i'%i)
	T1ph=0.005
	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	plt.plot(x,yfit)

	plt.legend()


# plot_single_T1(44)
# plot_single_T1(14)

def get_T1_croisement():
	fnames,fval=extract_glob('T1')
	n=67
	nbeg=20
	taus=np.zeros(n)
	for i in range(n):
		fname=fnames[i]
		x,y=extract_data(fname,ycol=5)
		# T1ph=0.003626
		T1ph=0.005
		popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
		taus[i]=popt[1]

	x=np.array(fval[:n])
	E1=2627.343809489154+24.662438765970307*x
	E2=2961.07596941526-36.62612342543252*x

	x=(E1-E2)[nbeg:]
	y=1/taus[nbeg:]
	return(x,y)

# x,y=extract_data('ESR 1 classe pas loin 111')
# plt.plot(x,y)
# psd(x,y,plot=True)


def plot_T1_fluct_lw():
	x,y=get_T1_croisement()

	ax1=plt.gca()

	ax1.plot(x,y,'o',markerfacecolor='none',label=r'Experiment')
	popt,yfit=lor_fit(x,y)
	plt.plot(x,yfit,lw=2,label='Lorentzian fit'%popt[2])

	ax2=ax1.twinx()
	x,y=extract_data('ESR 1 classe pas loin 111')
	y=y/max(y)
	c=hist_mean(x,y)
	x=x-2740
	ax2.plot(x,y,'--',color=color(2),label=r'ESR line',mew=0.5,ms=3)
	# x=x*sqrt(2)
	# ax2.plot(x,y,'--',color=color(3),label=r'ESR line$\times \sqrt{2}$',mew=0.5,ms=3)
	# x=x*sqrt(2)
	# n=len(x)
	# x=x[n//5:n-n//5]
	# y=y[n//5:n-n//5]
	# ax2.plot(x,y,'--',color=color(4),label=r'ESR line$\times 2$',mew=0.5,ms=3)

	ax2.tick_params(labelsize=15)

	ax1.legend(loc=2)
	ax2.legend()
	
# plot_T1_fluct_lw()


plt.show()