import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

x=np.linspace(0,10,200)
y1=np.exp(-x/3)
y2=np.exp(-x/2)

plt.plot(x,y1,label=r'$T_1$ for $\Gamma_1$')
plt.plot(x,y2,label=r'$T_1$ for $\Gamma_1 + \delta \Gamma$')
plt.legend()
plt.show()