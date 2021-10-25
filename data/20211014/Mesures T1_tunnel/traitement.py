import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


fname="T1_tunnel_adamas3_expVsStretch incroyable"
# fname='pola_laser_rouge'
x,y=extract_data(fname)
y0=0.05847272
# y=y-y0
# y=-y/max(-y)
y=y[1:]
x=x[1:]
# y=np.log(-np.log(y))
# x=np.log(x)
plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2,label='T1')
popt,yfit=lin_fit(x[:10],y[:10])
a=popt[0]
b=popt[1]
plt.plot(x,a*x+b)
print(popt[0],np.exp(-popt[1]/popt[0]))

# plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2,label='T1')
# popt,yfit=stretch_arb_exp_fit(x,y)
# plt.plot(x,yfit,lw=2,label='stretch, tau=%e,alpha=%e'%(popt[2],popt[3]))
# print(popt)
plt.legend()
plt.show()