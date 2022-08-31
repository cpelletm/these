import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *
# print(glob.glob('*.csv'))
plt.figure(num=1,figsize=(4.5,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

x,y=extract_data('2600 MHz 20 dB avec ampli.csv')
x=(x*35)+8
plt.plot(x,y,)

plt.show()