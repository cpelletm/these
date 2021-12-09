import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

#les x et y sont inversés pour cette série

x,y=extract_data('ESR micro onde a fond laser à fond bleu=0,10 ; orange=0,3')
y=y-min(y)
y=y/max(y)
plt.plot(x,y,label='0,10')

x,y=extract_data('ESR micro onde a fond laser à fond bleu=0,10 ; orange=0,3',xcol=2,ycol=3)
y=y-min(y)
y=y/max(y)
plt.plot(x,y,label='0,3')
plt.legend()
plt.show()
