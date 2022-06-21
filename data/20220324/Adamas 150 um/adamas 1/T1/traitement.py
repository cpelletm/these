import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(6,3),dpi=80)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

#les x et y sont inversés pour cette série
fnames=glob.glob('*.csv')
fval=[float(fnames[i][2:-5]) for i in range(len(fnames))] 
fnames=[s for _,s in sorted(zip(fval,fnames))]
fval=sorted(fval)

# fname=fnames[0]
# x,y=extract_data(fname,ycol=5)
# y=y/max(y)
# popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.8,fixed=True)
# plt.plot(x,y)
# plt.plot(x,yfit)

# fname=fnames[-1]
# x,y=extract_data(fname,ycol=5)
# y=y/max(y)
# popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.8,fixed=True)
# plt.plot(x,y)
# plt.plot(x,yfit)

n=len(fnames)

x=np.linspace(0.8,5,n)
freqp=2879.6100403000905-10.350382035600058*x+8.72563530864743*x**2-0.5448652051415266*x**3+0.008459469208990177*x**4
freqm=2862.3732486672525+5.336405357793713*x+0.4892478887834715*x**2+0.4361255116793501*x**3-0.047696861387582994*x**4
deltaF=freqp-freqm


taus=np.zeros(n)
for i in range(n):
	fname=fnames[i]
	x,y=extract_data(fname,ycol=5)
	T1ph=0.003626
	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	taus[i]=popt[1]

nmax=180 #Je sais pas ce qu'il se passe entre 180 et 200. Par ailleurs c'est sans doute une région qui commence à déconner vu que l'EM a chauffé et que je n'avais plus les bonnes valeurs des pics ESR pour la soustraction
deltaF=deltaF[:nmax]
Bs=((np.array(fval)-0.17)*31)[:nmax]
taus=taus[:nmax]


ax=plt.gca()
# ax2=ax.twiny()
# ax2.set_xlim(deltaF[0],deltaF[-1])

def inverse(x):
	[a,b,c,d,e]=[6.080677168884605e-08, -3.1647289853208374e-05, 0.008060166141532602, -0.4183988381154165, 14.803296667331745]
	return a*x**4+b*x**3+c*x**2+d*x+e


def forward(x):
	[a,b,c,d,e]=[-0.00010002528247366159, 0.012217576334451698, -0.5573193188732131, 13.253933094814867, -41.32960087823835]
	return a*x**4+b*x**3+c*x**2+d*x+e
	
# ax.set_xscale('function',functions=(forward, inverse))

def test_retour():
	nmin=30
	popt,yfit=fit_ordre_4(deltaF[nmin:],Bs[nmin:])
	[a,b,c,d,e]=popt
	#[-0.00010002528247366159, 0.012217576334451698, -0.5573193188732131, 13.253933094814867, -41.32960087823835]
	print(popt)
	x=deltaF
	yfit=a*x**4+b*x**3+c*x**2+d*x+e
	plt.plot(deltaF,Bs)
	plt.plot(x,yfit)

def test_aller():
	popt,yfit=fit_ordre_4(Bs,deltaF)
	[a,b,c,d,e]=popt
	#[6.080677168884605e-08, -3.1647289853208374e-05, 0.008060166141532602, -0.4183988381154165, 14.803296667331745]
	print(popt)
	x=Bs
	yfit=a*x**4+b*x**3+c*x**2+d*x+e
	plt.plot(Bs,deltaF)
	plt.plot(x,yfit)



x=Bs
y=1/taus
plt.plot(x,y,'o',markerfacecolor='none',ms=5,mew=0.7)

# popt,yfit=lor_fit_fixed(x,y,x0=0,sigma=8)
# print(popt)
# plt.plot(x,yfit,lw=2)

gammaref=25.5
bsup=[gammaref+5]*nmax
binf=[gammaref-5]*nmax
ax.fill_between(x,binf,bsup,alpha=0.3,color='red')
plt.plot(x,bsup,'-',lw=1,color='black')
plt.plot(x,binf,'-',lw=1,color='black')

# plt.plot(x,[gammaref]*nmax,'-',lw=2,color=color(3))
ylims=ax.get_ylim()
ax.set_ylim([0,ylims[1]])
plt.show()