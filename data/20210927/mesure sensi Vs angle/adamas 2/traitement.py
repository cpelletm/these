import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from analyse import *


fname="T1 0B soustraction"
x,y=extract_data(fname,xcol=0,ycol=5)
plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2,label='T1')
popt,yfit=exp_fit_zero(x,y)
plt.plot(x,yfit,lw=2,label='exp, tau=%e'%popt[1])
popt,yfit=stretch_exp_fit_zero(x,y)
plt.plot(x,yfit,lw=2,label='stretch, tau=%e'%popt[1])
plt.legend()
plt.show()