import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


data=np.zeros((11,11))
for i in range(11) :
	for j in range(11) :
		x,y=extract_data('x=%i.000000,y=%i.000000'%(i,j))
		data[i,j]=sum(y[257:270])
		# x,y=extract_data('x=%i.000000,y=%i.000000'%(i,j),xcol=2,ycol=3)
		# data[i,j]=y[261]/sum(y)

print_map(data)

# x,y=extract_data('x=%i.000000,y=%i.000000'%(0,0))
# plt.plot(y,'-x')
plt.show()