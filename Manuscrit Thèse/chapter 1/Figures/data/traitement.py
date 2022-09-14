import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *



plt.figure(num=1,figsize=(4.5,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)



# fname='T1 rose direct (20191106)'
# x,y=extract_data(fname)
# y=y/max(y)
# plt.plot(x,y,'o',markerfacecolor='None')
# popt,yfit=exp_fit(x,y)
# plt.plot(x,yfit,lw=2)
# print(popt)

# fname='T1 rose soustraction (20220221)'
# x,y=extract_data(fname,ycol=5)
# y=y/max(y)
# x=x*1e3
# # plt.plot(x,y,'o',markerfacecolor='None')
# x=average(x,3)
# y=average(y,3)
# plt.plot(x,y,'o',markerfacecolor='None')
# popt,yfit=exp_fit_zero(x,y)
# plt.plot(x,yfit,lw=2)
# print(popt)

fname='T1 rose soustraction (20220221)'
x,y=extract_data(fname,ycol=1)
x=x*1e3
plt.plot(x,y,label=r'$S_1$')
x,y=extract_data(fname,ycol=3)
x=x*1e3
plt.plot(x,y,label=r'$S_2$')
plt.legend()


plt.show()
