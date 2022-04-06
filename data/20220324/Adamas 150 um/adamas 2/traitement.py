import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


x,y=extract_data('ESR plus ou moins 3 V')
for i in range(len(x)):
	print(i,x[i])


# plt.plot()
# plt.show()
