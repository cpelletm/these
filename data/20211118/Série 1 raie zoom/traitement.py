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
		popt,yfit=gauss_fit(x,y)
		data[i,j]=1/popt[2]
print_map(data)


x,y=extract_data('x=%i.000000,y=%i.000000'%(0,10))
y=y/sum(y)
plt.plot(x,y,'x-')
popt,yfit=gauss_fit(x,y)
print(popt)
plt.plot(x,yfit)

#[9.13577147e-03 2.73857209e+03 3.08304494e+00 2.34489100e-04]

# x,y=extract_data('x=%i.000000,y=%i.000000'%(10,0))
# y=y/sum(y)
# plt.plot(x,y,'x-')

# plt.show()
