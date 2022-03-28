import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

#les x et y sont inversés pour cette série

n=30
xs=np.linspace(0,10,n)

# i=12
# x,y=extract_data('x=0,y=%.6f'%(xs[i]),xcol=2,ycol=3)
# PL=sum(y)
# x,y=extract_data('x=0,y=%.6f'%(xs[i]),xcol=2,ycol=1)
# y=y/PL
# popt,yfit=gauss_derivative_fit(x,y)
# plt.plot(x,yfit)
# print(popt)
# plt.plot(x,y,'x')

# i=24
# x,y=extract_data('x=0,y=%.6f'%(xs[i]),xcol=2,ycol=3)
# PL=sum(y)
# x,y=extract_data('x=0,y=%.6f'%(xs[i]),xcol=2,ycol=1)
# y=y/PL
# popt,yfit=gauss_derivative_fit(x,y)
# plt.plot(x,yfit)
# print(popt)
# plt.plot(x,y,'x')

data=[]
for i in range(n) :
	x,y=extract_data('x=0,y=%.6f'%(xs[i]),xcol=2,ycol=3)
	PL=sum(y)
	x,y=extract_data('x=0,y=%.6f'%(xs[i]),xcol=2,ycol=1)
	y=y/PL
	# data+=[sum(y[:208])-sum(y[208:])] #Contraste
	popt,yfit=gauss_derivative_fit(x,y) #Largeur
	data+=[popt[2]]

plt.plot(xs,data)


plt.show()
