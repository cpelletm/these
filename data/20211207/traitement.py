import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('D:\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


xmin=500
# x,y=extract_data('spectre (0,0) pleine puissance avec filtre')
# x=x[xmin:]
# y=y[xmin:]
# # y=y-min(y)
# # y=y/max(y)
# plt.plot(x,y,label='(0,0)')

x,y=extract_data('spectre (0,3) pleine puissance avec filtre')
x=x[xmin:]
y=y[xmin:]
plt.plot(x,y,label='filter')

x,y=extract_data('spectre (0,3) pleine puissance sans filtre')
x=x[xmin:]
y=y[xmin:]
plt.plot(x,y,label='no filter')
plt.legend()
plt.show()

