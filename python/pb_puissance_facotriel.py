import numpy as np 
from numpy import cos,sin,exp,sqrt,pi

import matplotlib.pyplot as plt



def f(n) :
	i=1
	while i**n < np.math.factorial(n):
		i=i+1
	print(i,n)
	return(i)


ns=range(200)
ys=[]
for n in ns:
	print(n)
	print(type(n))
	ys+=[f(n)]

plt.plot(ns,ys,'o')
plt.show()


