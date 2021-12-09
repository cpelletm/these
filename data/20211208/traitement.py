import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('D:\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

x,y=extract_data('spectre z=0 y=3 0.085 mW')
m=min(y)
y=y-m
y=y/sum(y)
plt.plot(x,y,label='0.085 mW y= 3')

x,y=extract_data('spectre z=0 y=3 0.2 mW')
m=min(y)
y=y-m
y=y/sum(y)
plt.plot(x,y,label='0.2 mW y= 3')

x,y=extract_data('spectre z=0 y=3 0.5 mW')
m=min(y)
y=y-m
y=y/sum(y)
plt.plot(x,y,label='0.5 mW y= 3')

x,y=extract_data('spectre z=0 y=3 0.9 mW')
m=min(y)
y=y-m
y=y/sum(y)
plt.plot(x,y,label='0.9 mW y= 3')




x,y=extract_data('spectre z=0 y=6 0.085 mW')
m=min(y)
y=y-m
y=y/sum(y)
plt.plot(x,y,label='0.085 mW y= 6')

x,y=extract_data('spectre z=0 y=6 0.2 mW')
m=min(y)
y=y-m
y=y/sum(y)
plt.plot(x,y,label='0.2 mW y= 6')

x,y=extract_data('spectre z=0 y=6 0.5 mW')
m=min(y)
y=y-m
y=y/sum(y)
plt.plot(x,y,label='0.5 mW y= 6')

x,y=extract_data('spectre z=0 y=6 0.9 mW')
m=min(y)
y=y-m
y=y/sum(y)
plt.plot(x,y,label='0.9 mW y= 6')


plt.legend()
plt.show()

