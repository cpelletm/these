import numpy as np
import matplotlib.pyplot as plt

#Bien essayé mais c'est non la tf
N=197
file='13.txt'

for file in ['13.txt','23.txt','33.txt','43.txt'] :
	x=np.zeros(N)
	y=np.zeros(N)
	with open(file,'r') as f:
		f.readline()
		f.readline()
		for i in range(N):
			line=f.readline()
			line=line.split()
			x[i]=float(line[0])
			y[i]=float(line[1])

	y_avg=sum(y[100:])/len(y[100:])
	y_plt=np.log(-y[:75]+y_avg)
	x_plt=x[:75]


	plt.plot(x_plt,y_plt)

	
plt.show()