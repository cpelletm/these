import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from PyQt5.QtWidgets import QApplication,QFileDialog

def lin_fit(x,y) :
	A=np.vstack([x,np.ones(len(x))]).T
	a,b = np.linalg.lstsq(A, y, rcond=None)[0]
	return(a,b,a*x+b)


xs=[1.599,0.956,0.722]
ys=[80.71,44.62,31.04]
xs=np.array(xs)
ys=np.array(ys)


a,b,yfit=lin_fit(xs,ys)
print(a,b)
plt.plot(xs,ys,'x')
plt.plot(xs,yfit)
plt.show()