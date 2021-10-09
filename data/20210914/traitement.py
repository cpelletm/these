import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from analyse import *


x,y=extract_data('t1_long')
# x=x[:100]
# y=y[:100]
plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2)
popt,yfit=stretch_exp_fit(x,y)
plt.plot(x,yfit,label='stretch')
print(popt[2])
# popt,yfit=exp_fit(x,y)
# plt.plot(x,yfit,label='exp')
popt,yfit=stretch_et_phonons(x,y,T1ph=5E-3)
plt.plot(x,yfit,label='stretch phonons')
print(popt[2])
# popt,yfit=stretch_arb_exp_fit(x,y)
# plt.plot(x,yfit)
# print(popt[3],popt[2])
plt.legend()
plt.show()