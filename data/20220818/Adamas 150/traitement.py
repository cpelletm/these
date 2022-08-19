import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

fnames=['ESR 03V champ transverse.csv', 'ESR 1 raie.csv', 'ESR raie champ transverse 0.3 V zoom.csv', 'ESR 1V.csv', 'ESR 1 raie champ transverse.csv', 'ESR 3V.csv', 'ESR raie champ transverse 0.5 V zoom.csv', 'ESR 0B.csv', 'ESR raie champ transverse 1 V zoom.csv']

f0=[0,2705,0,0,2905,0,0,2870,0]

plt.figure(num=1,figsize=(2,4),dpi=80)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.locator_params(axis='x', nbins=2)

i=7
xmin=100
xmax=400
x,y=extract_data(fnames[i])
y=y-min(y)
y=y/max(y)
x=x-f0[i]
plt.plot(x[xmin:xmax],y[xmin:xmax])



plt.show()
