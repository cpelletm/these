import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *



xmin=245
xmax=271

n=30
xs=np.linspace(0,10,n)

data=np.zeros((n,3))
for j in range(3) :
	print(j)
	for i in range(n) :
		x,y=extract_data('x=%.6f,y=%.6f'%(xs[i],xs[j]))
		x=x[xmin:xmax]
		y=y[xmin:xmax]
		popt,yfit=parabola_fit(x,y)
		print(popt[1])
		data[i,j]=popt[1]
print_map(data)



# x,y=extract_data('x=%.6f,y=%.6f'%(xs[29],xs[0]))
# plt.plot(x,y,'x-')
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# popt,yfit=parabola_fit(x,y)
# print(popt)
# plt.plot(x,yfit)

# x,y=extract_data('x=%.6f,y=%.6f'%(xs[0],xs[0]))
# plt.plot(x,y,'x-')
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# popt,yfit=parabola_fit(x,y)
# print(popt)
# plt.plot(x,yfit)


plt.show()