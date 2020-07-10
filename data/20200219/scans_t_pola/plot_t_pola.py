import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


voltage=np.arange(0.30,0.84,0.02)
N=197

files=['%3i.txt'% (v*100) for v in voltage]
t_pola=np.zeros(len(voltage))

def func(x,A,B,tau):
    return B+A*np.exp(-x/tau)

As=[]
Bs=[]
taus=[]

for file in files :
	x=np.zeros(N)
	y=np.zeros(N)
	with open(file,'r') as f:
		f.readline()
		f.readline()
		for i in range(N):
			line=f.readline()
			line=line.split()
			x[i]=float(line[0])
			y[i]=float(line[1])
	A=y[0]-y[-1]
	B=y[-1]
	tau=x[-1]/5
	p0=[A,B,tau]
	popt, pcov = curve_fit(func, x, y, p0)
	A=popt[0]
	B=popt[1]
	C=popt[2]
	As+=[A]
	Bs+=[B]
	taus+=[C]

fig,ax=plt.subplots(3)

ax[0].plot(voltage,As)
ax[1].plot(voltage,Bs)
ax[2].plot(voltage,taus)


plt.show()
