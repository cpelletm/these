import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

#les x et y sont inversés pour cette série

n=30
xs=np.linspace(0,10,n)

# data=np.zeros((n,n))
# for j in range(n) :
# 	print(j)
# 	for i in range(n) :
# 		x,y=extract_data('x=%.6f,y=%.6f'%(xs[i],xs[j]))
# 		x2,y2=extract_data('x=%.6f,y=%.6f'%(xs[i],xs[j]),xcol=2,ycol=3)
# 		# data[i,j]=(sum(y[256:264])-sum(y[264:271]))/sum(y2)
# 		data[i,j]=(max(y[10:70])-min(y[10:70]))/(max(y[280:295])-min(y[225:255]))
# data=data.T
# print_map(data[0:,0:])



x,y=extract_data('x=%.6f,y=%.6f'%(xs[1],xs[29]))
plt.plot(y,'x-')

# y[256:264]-y[264:271]
max(y[10:70])-min(y[10:70])
max(y[280:295])-min(y[225:255])
max(y[254:273])-min(y[254:273])
plt.show()
