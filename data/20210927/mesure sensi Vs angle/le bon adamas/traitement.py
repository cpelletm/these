import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


# fname="T1 100 3V pulse début read"
# x,y=extract_data(fname,xcol=0,ycol=5)
# popt,yfit=exp_fit(x,y)
# plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2,label='T1')
# plt.plot(x,yfit)
# plt.legend()
# plt.show()



# fname="ESR 1x1x1x1"
# x,y=extract_data(fname)
# plt.figure(num=1,figsize=(9,6),dpi=80) #à écrire au début a priori
# ESR_peaks=[2654,2737,2789,2860,2961,3021,3061,3116]
# # popt,yfit=ESR_n_pics(x,y,ESR_peaks)
# popt,yfit=find_nearest_ESR(x,y,ESR_peaks,TrueAngles=True)
# print(popt)
# plt.plot(x,yfit,lw=2)
# ax=plt.gca()
# ax.tick_params(labelsize=15)
# ax.set_xlabel(r'Microwave frequency (MHz)',fontsize=20)
# ax.set_ylabel(r'Demodulated PL (AU)' ,fontsize=20)
# plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2)
# plt.show()

#B=[95.82988692567591, 0.5359208817686791, 0.4420246182728666]
# transis=[]
# Amps=np.linspace(0,100,100)
# for amp in Amps:
# 	B=magneticField(amp=amp,theta=0.5359208817686791,phi=0.4420246182728666)
# 	transis+=[B.transitions4Classes()]

# transis=np.array(transis)
# plt.figure(num=1,figsize=(9,6),dpi=80) #à écrire au début a priori
# for i in range(8) :
# 	plt.plot(Amps,transis[:,i],lw=2)
# ax=plt.gca()
# ax.tick_params(labelsize=15)
# ax.set_xlabel(r'Magnetic field amplitude (G)',fontsize=20)
# ax.set_ylabel(r'Transition frequencies (MHz)' ,fontsize=20)
# plt.show()

# fname='sensi joli gaussiennes'
# fig,ax=plt.subplots(2,figsize=(9,12),dpi=80)
# ax1=ax[1]
# ax2=ax[0]
# dB=1e-2*3.5e-3
# x1,y1=extract_data(fname,xcol=0,ycol=1)
# x2,y2=extract_data(fname,xcol=2,ycol=3)
# x3,y3=extract_data(fname,xcol=4,ycol=5)
# m1=hist_mean(x1,y1)
# m2=hist_mean(x2,y2)
# ratio=dB/abs(m2-m1)
# x1=x1*ratio*1e6
# x2=x2*ratio*1e6
# y3=y3*ratio*1e6
# sigma=hist_sigma(x1,y1)
# print(sigma*1e-6*np.sqrt(0.003))
# ax1.plot(x1,y1,'o',markerfacecolor="None",ms=8,mew=2)
# ax1.plot(x2,y2,'o',markerfacecolor="None",ms=8,mew=2)
# ax2.plot(x3,y3,lw=2)
# ax1.tick_params(labelsize=15)
# ax1.set_ylabel(r'Histogram (counts)',fontsize=20)
# ax1.set_xlabel(r'Measured magnetic field ($\mu$T)' ,fontsize=20)
# ax2.tick_params(labelsize=15)
# ax2.set_xlabel(r'time (s)',fontsize=20)
# ax2.set_ylabel(r'Measured magnetic field ($\mu$T)' ,fontsize=20)
# plt.show()

fname='scan 100'
fig,ax=plt.subplots(2,figsize=(9,12),dpi=80)
ax1=ax[0]
ax2=ax[1]
dB=1e-2*3.5e-3
x1,y1=extract_data(fname,xcol=2,ycol=3)
x2,y2=extract_data(fname,xcol=0,ycol=1)
y1=y1/max(y1)
ratio=3.5*1e-3
x1=x1*ratio*1e3
x2=x2*ratio*1e3
ax1.plot(x1,y1,'o-',markerfacecolor="None",ms=8,mew=2)
ax2.plot(x2,y2,'o-',markerfacecolor="None",ms=8,mew=2)
ax1.tick_params(labelsize=15)
ax1.set_ylabel(r'Photoluminescence (AU)',fontsize=20)
ax2.tick_params(labelsize=15)
ax2.set_xlabel(r'magnetic field (mT)',fontsize=20)
ax2.set_ylabel(r'Demodulated PL (AU)' ,fontsize=20)
plt.show()