import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

scale=1.3
plt.figure(num=1,figsize=(3*scale,2*scale),dpi=80)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)

# fname='T1 NV-C13 100 3 V'
# x,y=extract_data(fname,xcol=4,ycol=5)
# plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2)
# popt,yfit=stretch_arb_exp_fit(x,y,alpha=0.5,fixed=True)
# plt.plot(x,yfit)
# print(popt[2])
# plt.show()



# fname='Vrai ESR 111'
# fname='ESR 111 et C13'
# cs=[2980.375, 2817.625, 3115.125, 2629.5]
# x,y=extract_data(fname)
# plt.plot(x,y)
# popt,yfit=ESR_n_pics_auto(x,y)
# plt.plot(x,yfit)
# print(popt)
# plt.show()

fname='Vrai ESR 100'
x,y=extract_data(fname)
plt.plot(x,y)

plt.show()