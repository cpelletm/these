import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


fname="T1 orange,vert=121 rouge =22 bleu =1x"
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

