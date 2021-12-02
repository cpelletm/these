import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

#les x et y sont inversés pour cette série

n=11
xs=np.linspace(0,10,n)

data=np.zeros((n,n))
for j in range(n) :
	print(j)
	for k in range(n) :
		x,y=extract_data('x=%.6f,y=%.6f'%(xs[k],xs[j]))
		x2,y2=extract_data('x=%.6f,y=%.6f'%(xs[k],xs[j]),xcol=2,ycol=3)
		PL=sum(y2)/len(y2)

		i=list(y).index(max(y[108:228]))
		M=sum(y[i-10:i+10])
		i=list(y).index(min(y[108:228]))
		m=sum(y[i-10:i+10])
		VHm=(M-m)

		i=list(y).index(min(y[470:490]))
		m=sum(y[i-10:i+10])
		i=list(y).index(max(y[550:580]))
		M=sum(y[i-10:i+10])
		C13=(M-m)

		i=list(y).index(min(y[520:535]))
		m=sum(y[i-7:i+7])
		i=list(y).index(max(y[505:520]))
		M=sum(y[i-7:i+7])
		DQ=(M-m)

		data[k,j]=VHm/C13*PL

print_map(data[:,:])



# x,y=extract_data('x=%.6f,y=%.6f'%(xs[0],xs[0]))
# plt.plot(y,'x-')

# x,y=extract_data('x=%.6f,y=%.6f'%(xs[10],xs[0]))
# plt.plot(y,'x-')


# VHs=[]
# C13s=[]
# DQs=[]
# for i in range(n) :
# 	x,y=extract_data('x=%.6f,y=%.6f'%(xs[i],xs[0]))
# 	x2,y2=extract_data('x=%.6f,y=%.6f'%(xs[i],xs[0]),xcol=2,ycol=3)
# 	PL=sum(y2)/len(y2)

# 	i=list(y).index(max(y[108:228]))
# 	M=sum(y[i-10:i+10])
# 	i=list(y).index(min(y[108:228]))
# 	m=sum(y[i-10:i+10])
# 	VHm=(M-m)/PL
# 	VHs+=[VHm]

# 	i=list(y).index(min(y[470:490]))
# 	m=sum(y[i-10:i+10])
# 	i=list(y).index(max(y[550:580]))
# 	M=sum(y[i-10:i+10])
# 	C13=(M-m)/PL
# 	C13s+=[C13]

# 	i=list(y).index(min(y[520:535]))
# 	m=sum(y[i-7:i+7])
# 	i=list(y).index(max(y[505:520]))
# 	M=sum(y[i-7:i+7])
# 	DQ=(M-m)/PL
# 	DQs+=[DQ]

# plt.plot(xs,VHs)
# plt.plot(xs,C13s)
# plt.plot(xs,DQs)
plt.show()
