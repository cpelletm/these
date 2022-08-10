import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
import matplotlib.animation as animation
from analyse import *

fnames=['tdv_1x1x1x1.txt','tdv_1x2x1.txt', 'tdv_2x2.txt', 'tdv_4x.txt' ]


T1ph=5
x,y=extract_data(fnames[0])
y=y/max(y)
plt.plot(x,y)
popt,yfit=stretch_et_phonons_non_zero(x,y,T1ph=T1ph,fixed=True)
plt.plot(x,yfit)
print(popt[2])
vRef=popt[2]

for fname in fnames[1:]:
	x,y=extract_data(fname)
	y=y/max(y)
	plt.plot(x,y)
	popt,yfit=stretch_et_phonons_non_zero(x,y,T1ph=T1ph,fixed=True)
	plt.plot(x,yfit)
	print(vRef/popt[2])

plt.show()