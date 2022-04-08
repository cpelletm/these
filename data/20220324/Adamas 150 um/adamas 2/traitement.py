import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *





fnames,fval=extract_glob('T1 1x1x1x1/T1')
n=len(fval)
taus=np.zeros(n)

Bs=[np.array([78.55,31.8,16.86])*(x-0.17)/2.8 for x in fval]

Bamps=np.array([norm(B)*np.sign(B[0]) for B in Bs])

for i in range(n):
	fname=fnames[i]
	x,y=extract_data(fname,ycol=5)
	T1ph=T1ph=0.003626
	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	taus[i]=popt[1]

nmin=106
x=Bamps[nmin:]

y=1/taus[nmin:]



plt.plot(x,y)
popt,yfit=lor_fit(x,y,x0=0.00001,amp=1600,ss=50,sigma=6) #Ok je fais full merde
print(popt)


plt.plot(x,yfit)

fnames,fval=extract_glob('T1 100 align 3/T1')
fval.remove(fval[194])
fnames.remove(fnames[194])
fval.remove(fval[178])
fnames.remove(fnames[178])
n=len(fval)
taus=np.zeros(n)
Bs=(np.array(fval)-0.16)*29


nmax=107
for i in range(n):
	fname=fnames[i]
	x,y=extract_data(fname,ycol=5)
	T1ph=0.003626
	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	taus[i]=popt[1]

x=-Bs[:nmax]
y=1/taus[:nmax]
plt.plot(x,y)

popt,yfit=lor_fit(x,y,x0=0.00001)
print(popt)
plt.plot(x,yfit)

plt.show()

