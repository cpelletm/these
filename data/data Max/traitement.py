import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


x,y=extract_data('pos_14_5_delay_540mus')
plt.plot(x,y)
cs=[2670,2710,2750,2794]
popt,yfit=ESR_n_pics(x,y,cs,typ='lor')
plt.plot(x,yfit)
print(popt)
plt.show()

save_data(yfit)