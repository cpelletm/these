import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


x,y=extract_data('Rabi2296MHzV2',decimalPoint=',')

print(x)
plt.plot(x,y)
plt.show()