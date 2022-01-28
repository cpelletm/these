import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

x,y=extract_data('test')
plt.plot(x,y,'x')
print(len(x))

plt.show()