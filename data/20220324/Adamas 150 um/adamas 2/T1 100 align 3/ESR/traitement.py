import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


plt.figure(num=1,figsize=(3,2),dpi=80)
x,y=extract_data('V=2.000000')
y=y/max(y)
plt.plot(x,y)
plt.xticks(fontsize=11)
plt.yticks(fontsize=12)
# ax=plt.gca()
# ax.tick_params(labelsize=15)


plt.show()

