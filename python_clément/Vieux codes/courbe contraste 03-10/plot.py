import numpy as np
import matplotlib.pyplot as plt

with open ("data.txt",'r') as f :
	data=[]
	for line in f:
		line=line.split()
		dataline=[]
		for elem in line :
			dataline+=[float(elem)]
		data+=[dataline]

data=np.array(data)

contraste=abs(data[:,2]-data[:,1])/data[:,2]

fig=plt.plot(data[:,0],contraste, 'x-')

plt.xlabel("Puissance (uW)")
plt.ylabel("Contraste")
plt.show()