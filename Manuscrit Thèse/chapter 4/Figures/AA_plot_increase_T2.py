import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(3,2),dpi=80)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.locator_params(axis='x', nbins=5)

n=500
x=np.linspace(-10,10,n)

y1=lor(x,sigma=2,norm=False)
y2=lor(x,sigma=1,norm=False)

plt.plot(x,y1,label=r'$B \neq 0$')
plt.plot(x,y2,label='B=0')
plt.legend()
plt.show()