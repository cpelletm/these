import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

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
taus=taus[:nmax]

plt.plot(deltaF,1/taus,'x')


gammaref=40
plt.plot(deltaF,[gammaref]*nmax,'--')
plt.show()