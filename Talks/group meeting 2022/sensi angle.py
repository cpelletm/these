import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *
angles=[2*i for i in range(16)]
sensis=[98.7,105,99.9,103,88.1,85.0,92.5,87.8,92.4,87.4,84.3,85.8,92.0,88.0,94.7,84.6]

plt.plot(angles,sensis,'x',ms=10)
plt.ylim(70,120)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()