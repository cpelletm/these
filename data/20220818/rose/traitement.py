import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(4.5,3),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=5)

x,y=extract_data('ESR 1 raie')

plt.plot(x,y,'x')
cs=[2726,2728,2730]
# popt,yfit=ESR_fixed_amp_and_width(x,y,cs,typ='lor')
popt,yfit=ESR_n_pics(x,y,cs,width=0.5,typ='lor')
print('T2*=%f'%(1/(2*pi*sum(popt[2])/3)))
plt.plot(x,yfit,lw=2)#,label='FWHM=%.3f'%(2*popt[2]))
print(popt)
# plt.legend()
plt.show()