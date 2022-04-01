import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


# fnames,fval=extract_glob('ESR')
# n=67
# fval=fval[:n]
# transis=np.zeros((n,2))
# for i in range(n):
# 	fname=fnames[i]
# 	x,y=extract_data(fname)
# 	cs=find_ESR_peaks(x,y,threshold=0.5)
# 	if len(cs)==2 :
# 		cs=find_ESR_peaks(x,y,threshold=0.5,precise=True)
# 		transis[i,:]=cs
# 	else :
# 		transis[i,:]=[np.nan,np.nan]

# # plt.plot(transis,'x')

# nbeg=25

# nmin=38
# nmax=51

# absc=fval[nbeg:nmin]+fval[nmax:]
# transi1=list(transis[nbeg:nmin,0])+list(transis[nmax:,1])
# transi2=list(transis[nbeg:nmin,1])+list(transis[nmax:,0])
# plt.plot(absc,transi1,'x')
# plt.plot(absc,transi2,'x')

# x=np.array(fval)
# popt,yfit=lin_fit(absc,transi1)
# print(popt)
# E1=popt[0]*x+popt[1]
# plt.plot(x,E1)

# popt,yfit=lin_fit(absc,transi2)
# print(popt)
# E2=popt[0]*x+popt[1]
# plt.plot(x,E2)



fnames,fval=extract_glob('T1')
n=67
nbeg=20
taus=np.zeros(n)
for i in range(n):
	fname=fnames[i]
	x,y=extract_data(fname,ycol=5)
	T1ph=0.003626
	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	taus[i]=popt[1]

x=np.array(fval[:n])
E1=2627.343809489154+24.662438765970307*x
E2=2961.07596941526-36.62612342543252*x


ax1=plt.gca()
x=(E1-E2)[nbeg:]
y=1/taus[nbeg:]
ax1.plot(x,y,'x',label='1/T1')
popt,yfit=lor_fit(x,y)
plt.plot(x,yfit,label='Lor fit HWHM=%.3f MHz'%popt[2])
print(popt)
ax2=ax1.twinx()




x,y=extract_data('ESR 1 classe pas loin 111')
y=y/max(y)
x=x-2740
x=x*sqrt(2)
ax2.plot(x,y,color='orange',label=r'ESR line$\times \sqrt{2}$')

ax1.legend(loc=2)
ax2.legend()
plt.show()

