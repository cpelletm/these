import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


x,y=extract_data('V=0.800000')
cs=find_ESR_peaks(x,y,threshold=0.3)
print(cs)