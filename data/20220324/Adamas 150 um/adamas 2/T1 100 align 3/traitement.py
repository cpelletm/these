import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


fnames,fval=extract_glob('ESR')
fval.remove(fval[194])
fnames.remove(fnames[194])
fval.remove(fval[178])
fnames.remove(fnames[178])
n=len(fval)
ms=np.zeros(n)
Ms=np.zeros(n)


for i in range(n):
	fname=fnames[i]
	x,y=extract_data(fname)
	k=find_elem(2870,x)
	m=find_elem(max(y[:k]),y)
	M=find_elem(max(y[k:]),y)
	ms[i]=m
	Ms[i]=M


plt.plot(ms)
plt.plot(Ms)
plt.show()



# fnames,fval=extract_glob('T1')
# fval.remove(fval[194])
# fnames.remove(fnames[194])
# fval.remove(fval[178])
# fnames.remove(fnames[178])
# n=len(fval)
# taus=np.zeros(n)

# # fname=fnames[0]
# # x,y=extract_data(fname,ycol=5)
# # T1ph=0.003626
# # # T1ph=0.00277119
# # popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph,fixed=False)
# # print(popt)
# # plt.plot(x,y,'x')
# # plt.plot(x,yfit)
# # popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph,fixed=True)
# # plt.plot(x,yfit)

# nmax=150

# for i in range(n):
# 	fname=fnames[i]
# 	x,y=extract_data(fname,ycol=5)
# 	x=x[:nmax]
# 	y=y[:nmax]
# 	T1ph=0.00277119
# 	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
# 	taus[i]=popt[1]

# plt.plot(fval,1/taus)

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

