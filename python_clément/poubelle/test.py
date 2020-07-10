import numpy as np
import matplotlib.pyplot as plt

x=np.linspace(0,10,100)

y1=1-np.exp(-x)
y2=0.05*x

plt.plot(x,y1)
plt.plot(x,y2)
plt.plot(x,y1+y2)

plt.show()