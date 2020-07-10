import numpy as np 
import matplotlib.pyplot as plt
from numpy.random import random as rd

thetas=[]
for truc in range(100000) :
	x=rd()
	if rd() > 0.5 :
		x=-x
	y=rd()
	if rd() > 0.5 :
		y=-y
	z=rd()
	if rd() > 0.5 :
		z=-z
	if x**2+y**2+z**2 < 1 :
		thetas+=[np.arccos(z/(x**2+y**2+z**2))]

plt.hist(thetas,20)
plt.show()

#On va conclure que Wolfram a raison, et que la distribution en theta est P(theta)=1/2*sin(theta) entre 0 et pi

