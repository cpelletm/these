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
# 	for k in range(n) :
# 		x,y=extract_data('x=%.6f,y=%.6f'%(xs[k],xs[j]))
# 		x2,y2=extract_data('x=%.6f,y=%.6f'%(xs[k],xs[j]),xcol=2,ycol=3)
# 		PL=sum(y2)/len(y2)
# 		C13=sum(y[341:384])-sum(y[163:221])
# 		DQ=sum(y[233:278])-sum(y[278:316])


# 		data[k,j]=C13

# print_map(data[:,:])

data=[]
for i in range(n) :
	x,y=extract_data('x=0,y=%.6f'%(xs[i]))
	x0=hist_mean(x,y)
	gamma=hist_sigma(x,y)
	data+=[x0]

plt.plot(xs,data)

# x,y=extract_data('x=0,y=%.6f'%(xs[0]))
# x0=hist_mean(x,y)
# gamma=hist_sigma(x,y)
# print(x0,gamma)

# x,y=extract_data('x=0,y=%.6f'%(xs[8]))
# y=y/sum(y)
# plt.plot(y,'x-')

# x,y=extract_data('x=0,y=%.6f'%(xs[29]))
# y=y/sum(y)
# plt.plot(y,'x-')


plt.show()
