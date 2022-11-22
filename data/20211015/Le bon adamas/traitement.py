import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('C:\\Users\\cleme\\OneDrive\\Documents\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(4,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

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

# fname='ESR 0B zoom +10 dBm avec un T et 50 ohms'
fname='Vrai ESR 1x1x1x1'
x,y=extract_data(fname)
# plt.ylim(0.96,1.0015)
# cs=[2624,3141]
# popt,yfit=ESR_n_pics(x,y,cs)
# plt.plot(x,yfit)
plt.plot(x,y)

plt.show()