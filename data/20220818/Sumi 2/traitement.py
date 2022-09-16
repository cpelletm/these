import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(4.5,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

x,y=extract_data('ESR 1 raie')

plt.plot(x,y,'x')
popt,yfit=gauss_fit(x,y)
plt.plot(x,yfit,lw=2)#
print(popt,popt[2]*1.18)
# plt.legend()
plt.show()