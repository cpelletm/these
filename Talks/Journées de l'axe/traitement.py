import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.xticks(fontsize=13)
plt.yticks(fontsize=13)


# fname='50 PPM N2'
# x,y=extract_data(fname)
# xmin=20
# xmax=(len(x)//3)*2
# x=x[xmin:xmax]
# y=y[xmin:xmax]

# popt,yfit=exp_fit(x,y)
# print(popt)
# y=y-popt[1]
# y=y/popt[0]
# x=x*1e3
# plt.plot(x,y)
# # popt,yfit=exp_fit_zero(x,y)
# # plt.plot(x,yfit)

fname='T1 orange,vert=121 rouge =22 bleu =1x'
x,y=extract_data(fname,ycol=5)
x=x*1e3
y=y/max(y)
popt,yfit=exp_fit_zero(x,y)
print(popt)
plt.plot(x,y,label='Low NV density')

fname='T1 0B'
x,y=extract_data(fname,ycol=5)
x=x*1e3
y=y/max(y)
plt.plot(x,y,label='High NV density')

plt.legend()
plt.show()