import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from analyse import *


fname="pola_laser_rouge"
x,y=extract_data(fname)
plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2,label='T1')
popt,yfit=stretch_arb_exp_fit(x,y)
plt.plot(x,yfit,lw=2,label='stretch, tau=%e,alpha=%e'%(popt[2],popt[3]))
plt.legend()
plt.show()