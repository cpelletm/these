import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


fname="T1 0B soustraction"
plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.locator_params(axis='x', nbins=5)
x,y=extract_data(fname,xcol=0,ycol=5)
x=x*1e3
y=y/max(y)
plt.plot(x,y,'o',markerfacecolor="None",ms=5,mew=1,label='Experimental Data')
popt,yfit=exp_fit_zero(x,y)
print(popt)
plt.plot(x,yfit,lw=3,label=r'exp($-t/\tau$)')
popt,yfit=stretch_exp_fit_zero(x,y)
print(popt)
plt.plot(x,yfit,lw=3,label=r'exp($-\sqrt{t/\tau}$)',color=color(2))
ax=plt.gca()
# ax.set_xlabel(r'Dark time (ms)',fontsize=20)
# ax.set_ylabel(r'Spin polarization (AU)' ,fontsize=20)
plt.legend(fontsize=15)
plt.show()

# fname="esr 100 +2V"
# x,y=extract_data(fname)
# y=y/max(y)
# y=1-0.04*y
# plt.figure(num=1,figsize=(9,6),dpi=80) #à écrire au début a priori
# popt,yfit=ESR_n_pics(x,y,[2785,2982])
# plt.plot(x,yfit,lw=2)
# ax=plt.gca()
# ax.tick_params(labelsize=15)
# ax.set_xlabel(r'Microwave frequency (MHz)',fontsize=20)
# ax.set_ylabel(r'Photoluminescence (AU)' ,fontsize=20)
# plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2)
# plt.show()

# fname="ESR splitté 2V"
# x,y=extract_data(fname)
# plt.figure(num=1,figsize=(9,6),dpi=80) #à écrire au début a priori
# # popt,yfit=ESR_n_pics(x,y,[2785,2982])
# # plt.plot(x,yfit,lw=2)
# ax=plt.gca()
# ax.tick_params(labelsize=15)
# ax.set_xlabel(r'Microwave frequency (MHz)',fontsize=20)
# ax.set_ylabel(r'Demodulated PL (AU)' ,fontsize=20)
# plt.plot(x,y,'-o',markerfacecolor="None",ms=8,mew=2)
# plt.show()

# fname="scan 100 j'ai compris l'astuce je suis trop refait"
# fig,ax=plt.subplots(2,figsize=(9,12),dpi=80)
# ax1=ax[0]
# ax2=ax[1]
# dB=1e-2*3.5e-3
# x1,y1=extract_data(fname,xcol=2,ycol=3)
# x2,y2=extract_data(fname,xcol=0,ycol=1)
# y1=y1/max(y1)
# ratio=3.5*1e-3
# x1=x1*ratio*1e3
# x2=x2*ratio*1e3
# ax1.plot(x1,y1,'o-',markerfacecolor="None",ms=8,mew=2)
# ax2.plot(x2,y2,'o-',markerfacecolor="None",ms=8,mew=2)
# ax1.tick_params(labelsize=15)
# ax1.set_ylabel(r'Photoluminescence (AU)',fontsize=20)
# ax2.tick_params(labelsize=15)
# ax2.set_xlabel(r'magnetic field (mT)',fontsize=20)
# ax2.set_ylabel(r'Demodulated PL (AU)' ,fontsize=20)
# plt.show()