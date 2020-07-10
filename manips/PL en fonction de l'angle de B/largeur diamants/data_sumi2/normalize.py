import numpy as np
import matplotlib.pyplot as plt

def lin_fit(x,y) :
	A=np.vstack([x,np.ones(len(x))]).T
	a,b = np.linalg.lstsq(A, y, rcond=None)[0]
	return(a,b)

x=np.array([1.3,1.41,1.5,2,2.11,2.19,2.29])
y1=np.array([821,822,824,832,833,834,837])
y2=np.array([842,839,835,822,819,816,813])
y=(y1-y2)+2000

plt.plot(x,y)
a,b=lin_fit(x,y)
plt.plot(x,a*x+b,label='%f'%a)
plt.legend()
plt.show()