import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

def lor(x,x0=0,sigma=1,norm=True):
	y=sigma**2/((x-x0)**2+sigma**2)
	if norm:
		return y/(pi*sigma)
	else :
		return y

def gauss(x,x0=0,sigma=1,norm=True):
	y=exp(-(x-x0)**2/(2*sigma**2))
	if norm:
		return y/(sqrt(2*pi)*sigma)
	else :
		return y
n=100
sigmas=np.linspace(10,100,n)
ints=np.zeros(n)

for i in range(n):
	x=np.linspace(-500,500,100000)
	y1=lor(x)
	y2=np.sqrt(lor(x,norm=False,sigma=sigmas[i]))
	y=y1*y2
	ints[i]=integration(x,y)**2
	# plt.plot(x,y)
	# print(integration(x,y)**2)

x,y=sigmas/(1+sigmas),ints
plt.plot(x,y)
plt.plot(x,x)
popt,yfit=lin_fit(x,y)
plt.plot(x,yfit)
print(popt)
# x=np.linspace(-50,50,10000)
# y=lor(x)
# print(integration(x,y))




plt.show()