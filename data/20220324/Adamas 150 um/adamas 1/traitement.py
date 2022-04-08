import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

x,y=extract_data('T1 1 classe 111',ycol=5)
plt.plot(x,y,'x')
# popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.8,fixed=False)
# print(estim_error(y,yfit))
# for T1ph in np.linspace(1e-3,5e-3,100):
# 	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
# 	print('T1ph=%f,error=%f'%(T1ph,estim_error(y,yfit)))
T1ph=0.003626
popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
plt.plot(x,yfit)
print(popt,1/popt[1])
plt.show()