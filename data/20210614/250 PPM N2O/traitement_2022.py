import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)


fname='T1 250 uW 2V random'
x,y=extract_data(fname)
x=x[1:]
y=y[1:]
plt.plot(x,y)
popt,yfit=exp_fit(x,y)
print(popt)
plt.plot(x,yfit)

plt.show()