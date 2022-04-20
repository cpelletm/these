import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *





fnames,fval=extract_glob('Série 3/T1')
n=len(fval)
print(n)
taus=np.zeros(n)


for i in range(n):
	x,y=extract_data(fnames[i],ycol=5)
	# x2=lissage(x,7)
	# y2=lissage(y,7)
	popt,yfit=stretch_et_phonons(x,y,T1ph=0.003626)
	taus[i]=popt[1]


x=fval
y=1/taus
y=y-min(y)
y=y/max(y)
plt.plot(x,y)


x,y=extract_data('ESR série 3')
y=y/max(y)
plt.plot(x,y)


plt.show()

