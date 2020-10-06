import numpy as np 
import matplotlib.pyplot as plt
from numpy.random import random as rd
from datetime import date

x=np.linspace(0,2,200)
y=np.arctan(np.tan(np.pi/2*x))

plt.plot(x,y,label='arctan(tan(pi/2*x))')
ax=plt.gca()
ylim=ax.get_ylim()
xlim=ax.get_xlim()
plt.plot([-1,3],[0,0],linewidth=3,color='r')
plt.plot([3/2,3/2],[-2,2],ls='--',color='r')
ax.set_xlim(xlim)
ax.set_ylim(ylim)
plt.grid()
plt.legend()
plt.show()
