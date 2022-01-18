import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

#les x et y sont inversés pour cette série

n=30
xs=np.linspace(0,10,n)
zs=np.linspace(-5,5,n)


# data=np.zeros((n,n))
# for j in range(n) :
# 	print(j)
# 	for k in range(n) :
# 		x,y=extract_data('z=%.6f,y=%.6f'%(zs[k],xs[j]),xcol=2,ycol=3)
# 		PL=sum(y)
# 		x,y=extract_data('z=%.6f,y=%.6f'%(zs[k],xs[j]))
# 		DQ=sum(y[234:271]-sum(y[271:306]))
# 		data[k,j]=-DQ

# print_map(data[:,:],xmin=-5,xmax=5,ymin=0,ymax=10)

Ps=np.linspace(-20,15,30)

data=[]
for i in range(n) :
	x,y=extract_data('p=%f'%(Ps[i]))
	x0=hist_mean(x,y)
	gamma=hist_sigma(x,y)
	data+=[gamma]

plt.plot(Ps,data)

# x,y=extract_data('p=%f'%(Ps[-1]))
# plt.plot(y,'x')


# x,y=extract_data('z=%.6f,y=%.6f'%(zs[15],xs[0]))
# y=y/max(y)
# plt.plot(x,y)


# x,y=extract_data('z=%.6f,y=%.6f'%(zs[29],xs[0]))
# y=y/max(y)
# plt.plot(x,y)



# x,y=extract_data('x=0,y=%.6f'%(xs[8]))
# y=y/sum(y)
# plt.plot(y,'x-')

# x,y=extract_data('x=0,y=%.6f'%(xs[29]))
# y=y/sum(y)
# plt.plot(y,'x-')


plt.show()
