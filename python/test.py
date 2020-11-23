import numpy as np 
from numpy import cos,sin,exp,sqrt,pi
import matplotlib.pyplot as plt

x=np.linspace(-10,10,1000)
ytrap=(x*5)**2
ytorque=-50*x+25

y=ytrap+ytorque
plt.xlim(-10,10)
plt.ylim(-100,500)
plt.plot(x,ytrap,lw=3)
plt.plot(x,ytorque,lw=3)
plt.plot(x,y,lw=3)
plt.show()