import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

x,y=extract_data('scan EM random dir',ycol=3)
y=y/max(y)
x=x*3.5
fig,ax=plt.subplots()
ax.plot(x,y,'-o',markerfacecolor='None')
T1=5e-3
t=ax.text(x=10,y=0.999,s=r'$T_1$=%.3e'%T1,fontsize=15,fontweight='bold')
T1=2E-3
t.set_text(r'$T_1$=%.3e'%T1)
plt.show()


