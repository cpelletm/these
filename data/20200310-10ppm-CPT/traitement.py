import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


fname="Rabi_probe_2.64055_-10dBm_with-pump_2.62_10dBm"
x,y=extract_data(fname)
y=y/max(y)
plt.figure(num=1,figsize=(9,6),dpi=80) #à écrire au début a priori
ax=plt.gca()
ax.tick_params(labelsize=15)
ax.set_xlabel(r'microwave pulse ($\mu$s)',fontsize=20)
ax.set_ylabel(r'Photoluminescence (AU)' ,fontsize=20)
plt.plot(x,y,'o',markerfacecolor="None",ms=12,mew=3)
popt,yfit=Rabi_fit(x,y)
plt.plot(x,yfit,lw=2)
plt.show()
