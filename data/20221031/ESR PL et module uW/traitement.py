import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

x,y=extract_data('ESR PL + shift B',ycol=3)
y=y/max(y)
plt.plot(x,y)

# x,y=extract_data('ESR modul f + shift B',ycol=5)
# y=y/max(y)
# plt.plot(x,y,label=r'$B=B_0$')
# x,y=extract_data('ESR modul f + shift B',ycol=1)
# y=y/max(y)
# plt.plot(x,y,'--',label=r'$B=B_0+1$ G')
# x,y=extract_data('ESR modul f + shift B',ycol=3)
# y=y/max(y)
# plt.plot(x,y,'--',label=r'$B=B_0-1$ G')
# plt.legend()
plt.show()