import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


plt.figure(num=1,figsize=(3,2),dpi=80)

# fnames,fval=extract_glob('ESR')
# fval.remove(fval[194])
# fnames.remove(fnames[194])
# fval.remove(fval[178])
# fnames.remove(fnames[178])
# n=len(fval)
# ms=np.zeros(n)
# Ms=np.zeros(n)
# Bs=np.zeros(n)
# for i in range(n):
# 	# print(i)
# 	fname=fnames[i]
# 	x,y=extract_data(fname)
# 	k=find_elem(2870,x)
# 	m=find_elem(max(y[:k]),y)
# 	M=find_elem(max(y[k:]),y)
# 	ms[i]=x[m]
# 	Ms[i]=x[M]
# 	# E=3
# 	# D=2870
# 	# Bs[i]=0.5*(find_B_100(ms[i],transi='-',B_max=100,E=E,D=D)+find_B_100(Ms[0],transi='+',B_max=100,E=E,D=D))




# plt.plot(fval,ms)
# plt.plot(fval,Ms)

# Bs=(np.array(fval)-0.16)*29
# transis=np.zeros((n,2))
# for i in range(n):
# 	B=[Bs[i],0,0]
# 	H=NVHamiltonian(B,c=1,E=4)
# 	transis[i,:]=H.transitions()


# plt.plot(fval,transis[:,0])
# plt.plot(fval,transis[:,1])

# plt.show()



fnames,fval=extract_glob('T1')
fval.remove(fval[194])
fnames.remove(fnames[194])
fval.remove(fval[178])
fnames.remove(fnames[178])
n=len(fval)
taus=np.zeros(n)
Bs=(np.array(fval)-0.16)*29

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

nmax=110

for i in range(n):
	fname=fnames[i]
	x,y=extract_data(fname,ycol=5)
	T1ph=0.003626
	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	taus[i]=popt[1]

Bs=Bs[:nmax]
taus=taus[:nmax]
plt.plot(-Bs,1/taus)

# x,y=extract_data('T1 3 V bien aligné',ycol=5)
# x=x[:nmax]
# y=y[:nmax]
# T1ph=0.00277119
# popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
# y=[1/popt[1]]*len(fval)

# plt.plot(fval,y,'--')


plt.show()

