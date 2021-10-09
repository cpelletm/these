import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from analyse import *


fnames=glob.glob('*.csv')
taus=[]
alphas=[]
vs=[]
for i in range(len(fnames)):
	if fnames[i][2]=='-' :
		v=-float(fnames[i][3:-7])
	else :
		v=float(fnames[i][2:-7])
	vs+=[v]
	x,y=extract_data(fnames[i])
	popt,yfit=stretch_exp_fit(x,y)
	# alphas+=[popt[3]]
	taus+=[popt[2]]



plt.plot(vs,taus,'o',markerfacecolor="None",ms=8,mew=2,label='T1')
plt.legend()
plt.show()