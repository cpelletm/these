import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

# x,y=extract_data('T1 0B',ycol=5)
# x=x*1e3
# y=y/max(y)
# plt.plot(x,y,'o',markerfacecolor='None',label='B=0 mT')
# popt0B,yfit=exp_fit_zero(x,y)


# x,y=extract_data('T1 1 classe',ycol=5)
# x=x*1e3
# y=y/max(y)
# plt.plot(x,y,'o',markerfacecolor='None',label='B=5 mT')
# popt,yfit=exp_fit_zero(x,y)
# plt.plot(x,yfit,label='exp fit, tau=%.3f ms'%popt[1])
# x=np.array([0]+list(x))
# plt.plot(x,popt0B[0]*np.exp(-x/popt0B[1]),label='exp fit, tau=%.3f ms'%popt0B[1])
# plt.legend()
# plt.show()


x,y=extract_data('ESR 0B dezoom')
plt.plot(x,y,'-o',markerfacecolor='None')
plt.xlabel('Frequency (MHz)',fontsize=15)
plt.ylabel('Signal (A.U)',fontsize=15)
plt.show()