import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

data=[]
with open('input','r') as f :
	for line in f :
		data+=[float(line)]


data=np.array(data)
data=data[0:-2]+data[1:-1:]+data[2:]
ctr=0
for i in range(1,len(data)):
	if data[i] > data[i-1]:
		ctr+=1

print(ctr)
print(len(data))

