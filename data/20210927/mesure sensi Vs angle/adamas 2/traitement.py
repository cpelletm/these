import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


# fname="T1 0B soustraction"
# x,y=extract_data(fname,xcol=0,ycol=5)
# plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2,label='T1')
# popt,yfit=exp_fit_zero(x,y)
# plt.plot(x,yfit,lw=2,label='exp, tau=%e'%popt[1])
# popt,yfit=stretch_exp_fit_zero(x,y)
# plt.plot(x,yfit,lw=2,label='stretch, tau=%e'%popt[1])
# plt.legend()
# plt.show()

fname="esr 100 +2V"
x,y=extract_data(fname)
y=y/max(y)
y=1-0.04*y
plt.figure(num=1,figsize=(9,6),dpi=80) #à écrire au début a priori
popt,yfit=ESR_n_pics(x,y,[2785,2982])
plt.plot(x,yfit,lw=2)
ax=plt.gca()
ax.tick_params(labelsize=15)
ax.set_xlabel(r'Microwave frequency (MHz)',fontsize=20)
ax.set_ylabel(r'Photoluminescence (AU)' ,fontsize=20)
plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2)
plt.show()