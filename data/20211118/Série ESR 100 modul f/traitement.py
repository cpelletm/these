import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *




data=np.zeros((11,11))
for i in range(11) :
	for j in range(11) :
		x,y=extract_data('x=%i.000000,y=%i.000000'%(i,j))
		data[i,j]=max(y)
		xmin=73
		xmax=85
		x=x[xmin:xmax]
		y=y[xmin:xmax]
		[a,b],yfit=lin_fit(x,y)



data[10,10]=np.NaN		
print_map(data)



# x,y=extract_data('x=%i.000000,y=%i.000000'%(0,0))
# plt.plot(x,y,'x-')

# xmin=73
# xmax=85
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# [a,b],yfit=lin_fit(x,y)
# print(-b/a,a)
# plt.plot(x,yfit)

# xmin=437
# xmax=449
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# [a,b],yfit=lin_fit(x,y)
# print(-b/a,a)
# plt.plot(x,yfit)

# x,y=extract_data('x=%i.000000,y=%i.000000'%(1,0))
# plt.plot(x,y,'x-')

plt.show()
