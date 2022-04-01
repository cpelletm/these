import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


fnames,fval=extract_glob('ESR')
n=len(fnames)
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

nmin=40
nmax=60

absc=fval[:nmin]+fval[nmax:]
transi1=list(transis[:nmin,0])+list(transis[nmax:,1])
transi2=list(transis[:nmin,1])+list(transis[nmax:,0])
plt.plot(absc,transi1,'x')
plt.plot(absc,transi2,'x')

x=np.array(fval)
popt,yfit=lin_fit(absc,transi1)
print(popt)
E1=popt[0]*x+popt[1]
plt.plot(x,E1)

popt,yfit=lin_fit(absc,transi2)
print(popt)
E2=popt[0]*x+popt[1]
plt.plot(x,E2)

# popt,yfit=fit_ordre_4(absc,transi1)
# x=np.array(fval)
# E1=sum(popt[-i-1]*x**i for i in range(len(popt)))
# plt.plot(x,E1)

# popt,yfit=fit_ordre_4(absc,transi2)
# x=np.array(fval)
# E2=sum(popt[-i-1]*x**i for i in range(len(popt)))
# plt.plot(x,E2)


# fnames,fval=extract_glob('T1')
# n=len(fnames)
# taus=np.zeros(n)
# for i in range(n):
# 	fname=fnames[i]
# 	x,y=extract_data(fname,ycol=5)
# 	T1ph=0.003626
# 	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
# 	taus[i]=popt[1]

# ax1=plt.gca()
# ax1.plot((E2-E1),1/taus)
# ax2=ax1.twinx()

# x,y=extract_data('ESR 1 classe pas loin 111')
# y=y/max(y)
# x=x-2740
# x=x*sqrt(2)
# ax2.plot(x,y,color='orange')

plt.show()

