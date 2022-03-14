import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

x,y=extract_data('odmr 1 classe -20 dbm')

plt.plot(x,y,'x')
cs=[2708,2710,2712]
popt,yfit=ESR_fixed_amp_and_width(x,y,cs,typ='lor')
plt.plot(x,yfit,label='FWHM=%.3f'%(2*popt[2]))
print(popt)
plt.legend()
plt.show()