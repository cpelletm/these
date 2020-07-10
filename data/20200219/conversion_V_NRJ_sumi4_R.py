import numpy as np
import matplotlib.pyplot as plt

u=np.array([0.35,0.45,0.85,0.95,1.05,1.15])
delta=np.array([-11,-8,10,15,18,23])

plt.plot(u,delta)

def lin_fit(x,y) :
	A=np.vstack([x,np.ones(len(x))]).T
	a,b = np.linalg.lstsq(A, y, rcond=None)[0]
	return(a,b)
a,b=lin_fit(u,delta)
plt.plot(u,a*u+b)
print(a,b)
plt.show()