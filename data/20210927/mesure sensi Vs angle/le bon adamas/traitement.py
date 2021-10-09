import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from analyse import *


fname="T1 100 3V pulse début read"
x,y=extract_data(fname,xcol=0,ycol=5)
popt,yfit=exp_fit(x,y)
plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2,label='T1')
plt.plot(x,yfit)
plt.legend()
plt.show()