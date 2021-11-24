import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


xmin=241
xmax=268
n=30
xs=np.linspace(0,10,n)

data=np.zeros(n)
j=0
for i in range(n) :
	x,y=extract_data('x=%.6f,y=%.6f'%(xs[i],xs[j]))
	y=y/max(y)
	dx=x[1]-x[0]
	x=x[xmin:xmax]
	y=y[xmin:xmax]
	popt,yfit=parabola_fit(x,y)
	c=popt[1]
	# if i==0 and j==0 :
	# 	c=c-dx
	# elif i!=0 :
	# 	if abs(data[i-1,j]-c)>0.5*dx :
	# 		c=c-dx
	# else :
	# 	if abs(data[i,j-1]-c)>0.5*dx :
	# 		c=c-dx
	data[i]=c


plt.plot(data,'-x')
plt.show()

# x,y=extract_data('x=%.6f,y=%.6f'%(xs[29],xs[0]))
# plt.plot(x,y,'x-')
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# popt,yfit=parabola_fit(x,y)
# plt.plot(x,yfit)
# print(popt[1])
# plt.show()

# x,y=extract_data('x=%.6f,y=%.6f'%(xs[29],xs[0]))
# plt.plot(x,y,'x-')
#[9.13577147e-03 2.73857209e+03 3.08304494e+00 2.34489100e-04]

# x,y=extract_data('x=%i.000000,y=%i.000000'%(10,0))
# y=y/sum(y)
# plt.plot(x,y,'x-')


