import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

#les x et y sont inversés pour cette série

x,y=extract_data('ESR P1 0,3 et 0,7 avec densité x10')
y=y-min(y)
y=y/max(y)
plt.plot(x,y,label=(0,7))

x,y=extract_data('ESR P1 0,3 et 0,7 avec densité x10',xcol=2,ycol=3)
y=y-min(y)
y=y/max(y)
plt.plot(x,y,label=(0,3))
plt.legend()
plt.show()
