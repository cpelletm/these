import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

x,y=extract_data('mag sensitive',data='col')
plt.plot(x,y,label='magnetic sensitive')

x,y=extract_data('mag insen',data='col')
plt.plot(x,y,label='magnetic insensitive')

x,y=extract_data('bruit elec',data='col')
plt.plot(x,y,label='electronic noise')

plt.plot([0,10000],[-80.5,-80.5],'--',label='shot noise limit')
plt.legend()
plt.show()