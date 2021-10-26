import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from analyse import *
from scipy.signal import find_peaks




fname='ESR 1 raie clean'
x,y=extract_data(fname)
plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=1)
cs=find_ESR_peaks(x,y,width=2,threshold=0.7)
print(cs)
popt,yfit=ESR_fixed_amp_and_width(x,y,cs,width=1,typ='lor')
plt.plot(x,yfit,lw=2,label='width=%4.3f MHz'%popt[2])
print(popt)
plt.legend()
plt.show()

