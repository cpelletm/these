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
gammas=[]
for i in range(n) :
	x,y=extract_data('ESR 0B en fonction de la puissance (0,3) densité x10\\p=%f'%(Ps[i]))
	PL=sum(y[800:])/len(y[800:])
	y=(PL-y)/PL
	cP1=sum(y[630:730])/len(y[630:730])
	y=y[400:500]
	x=x[400:500]
	x0=hist_mean(x,y)
	gamma=hist_sigma(x,y)
	gammas+=[gamma]
	data+=[cP1]
plt.plot(gammas,data,label='(0,3)')

data=[]
gammas=[]
for i in range(n) :
	x,y=extract_data('ESR 0B en fonction de la puissance (0,7) densité x10\\p=%f'%(Ps[i]))
	PL=sum(y[800:])/len(y[800:])
	y=(PL-y)/PL
	cP1=sum(y[630:730])/len(y[630:730])
	x=x[400:500]
	y=y[400:500]
	x0=hist_mean(x,y)
	gamma=hist_sigma(x,y)
	gammas+=[gamma]
	data+=[cP1]
plt.plot(gammas,data,label='(0,7)')


# x,y=extract_data('ESR 0B en fonction de la puissance (0,7) densité x10\\p=%f'%(Ps[-1]))
# PL=sum(y[800:])/len(y[800:])
# y=(PL-y)/PL
# plt.plot(y,'x')



plt.legend()
plt.show()
