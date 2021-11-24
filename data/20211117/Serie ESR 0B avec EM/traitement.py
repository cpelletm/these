import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


xmin=245
xmax=270

data=np.zeros((11,11))
for i in range(11) :
	for j in range(11) :
		x,y=extract_data('x=%i.000000,y=%i.000000'%(i,j))
		y=y/sum(y)
		x=x[xmin:xmax]
		y=y[xmin:xmax]
		popt,yfit=parabola_fit(x,y)
		data[i,j]=1/popt[2]
print_map(data)
print(data)

# x,y=extract_data('x=%i.000000,y=%i.000000'%(0,10))
# y=y/sum(y)
# plt.plot(x,y,'x-')
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# popt,yfit=parabola_fit(x,y)
# print(popt)
# plt.plot(x,yfit)


# x,y=extract_data('x=%i.000000,y=%i.000000'%(8,0))
# y=y/sum(y)
# plt.plot(x,y,'x-')
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# popt,yfit=parabola_fit(x,y)
# print(popt)
# plt.plot(x,yfit)
# plt.show()
