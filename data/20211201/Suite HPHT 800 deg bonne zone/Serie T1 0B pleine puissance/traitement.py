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
	x,y=extract_data('x=0,y=%.6f'%(xs[i]),xcol=4,ycol=5)
	popt,yfit=stretch_arb_exp_fit_zero(x,y)
	data+=[popt[1]]
	print(popt[1])

plt.plot(xs,data)

# x,y=extract_data('x=0,y=%.6f'%(xs[0]),xcol=4,ycol=5)
# y=y/max(y)
# plt.plot(y,'x-')



# x,y=extract_data('x=0,y=%.6f'%(xs[8]),xcol=4,ycol=5)
# y=y/max(y)
# plt.plot(x,y,'x-')
# popt,yfit=exp_fit_zero(x,y)
# plt.plot(x,yfit)
# popt,yfit=stretch_exp_fit_zero(x,y)
# plt.plot(x,yfit)
# popt,yfit=stretch_arb_exp_fit_zero(x,y)
# plt.plot(x,yfit)
# print(popt)

# x,y=extract_data('x=0,y=%.6f'%(xs[15]),xcol=4,ycol=5)
# y=y/max(y)
# plt.plot(y,'x-')

# x,y=extract_data('x=0,y=%.6f'%(xs[29]),xcol=4,ycol=5)
# y=y/max(y)
# plt.plot(y,'x-')

plt.show()
