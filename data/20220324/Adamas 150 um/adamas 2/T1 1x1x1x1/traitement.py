import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


# fnames,fval=extract_glob('ESR')
# n=len(fval)
# transis=np.zeros((n,8))
# for i in range(n):
# 	fname=fnames[i]
# 	x,y=extract_data(fname)
# 	cs=find_ESR_peaks(x,y,threshold=0.3)
# 	if len(cs)==8 :
# 		cs=find_ESR_peaks(x,y,threshold=0.3,precise=True)
# 		transis[i,:]=cs
# 	else :
# 		transis[i,:]=[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]

# # for j in range(8):
# # 	plt.plot(transis[:,j])

# y=list(transis[:35,0])+list(transis[65:,7])
# x=fval[:35]+fval[65:]


# plt.plot(x,y,'x')
# popt,yfit=fit_ordre_4(x,y)
# x=np.array(x)

# yfit=sum((x**i)*popt[-i-1] for i in range(len(popt)))
# plt.plot(x,yfit)
# print(popt)



fnames,fval=extract_glob('T1')
n=len(fval)
taus=np.zeros(n)

# fname=fnames[-1]
# x,y=extract_data(fname,ycol=5)
# T1ph=0.003626
# # T1ph=0.00277119
# popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph,fixed=False)
# print(popt)
# plt.plot(x,y,'x')
# plt.plot(x,yfit)
# popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph,fixed=True)
# plt.plot(x,yfit)


for i in range(n):
	fname=fnames[i]
	x,y=extract_data(fname,ycol=5)
	T1ph=T1ph=0.003626
	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	taus[i]=popt[1]

plt.plot(fval,1/taus)

# x,y=extract_data('T1 3 V bien aligné',ycol=5)
# x=x[:nmax]
# y=y[:nmax]
# T1ph=0.00277119
# popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
# y=[1/popt[1]]*len(fval)

# plt.plot(fval,y,'--')

# x=np.array(fval[:n])
# E1=2627.343809489154+24.662438765970307*x
# E2=2961.07596941526-36.62612342543252*x


# ax1=plt.gca()
# x=(E1-E2)[nbeg:]
# y=1/taus[nbeg:]
# ax1.plot(x,y,'x',label='1/T1')
# popt,yfit=lor_fit(x,y)
# plt.plot(x,yfit,label='Lor fit HWHM=%.3f MHz'%popt[2])
# ax2=ax1.twinx()




# x,y=extract_data('ESR 1 classe pas loin 111')
# y=y/max(y)
# x=x-2740
# x=x*sqrt(2)
# ax2.plot(x,y,color='orange',label=r'ESR line$\times \sqrt{2}$')

# ax1.legend(loc=2)
# ax2.legend()
plt.show()

