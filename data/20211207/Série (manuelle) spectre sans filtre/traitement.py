import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('D:\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


files=glob.glob('*.asc')


data=[]
xs=[]
for i in range(len(files)) :
	file=files[i]
	x,y=extract_data(file)
	y=y-210
	y=y/sum(y)
	data+=[sum(y[580:680])]
	xs+=[float(file[:-4])]


data=[e for _, e in sorted(zip(x, data))]
xs=sorted(xs)
plt.plot(xs,data)
plt.show()

