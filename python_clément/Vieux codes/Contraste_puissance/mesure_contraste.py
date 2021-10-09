import matplotlib.pyplot as plt
import numpy as np

files=["25uW.txt","50uW.txt","0-100mW.txt","0-25mW.txt","0-50mW.txt","0-74mW.txt","0-99mW.txt","1-55mW_plus_de_coups.txt"]
puiss=[25,50,100,250,500,740,990,1550]
contraste=[]
for i in range(len(files)) :
	x=[]
	y=[]
	with open(files[i]) as f :
		for line in f :
			line=line.split()
			x+=[float(line[0])]
			y+=[float(line[1])]

	avg=sum(y[150:])/len(y[150:])
	y=[v/avg for v in y]
	contraste+=[(1-min(y))*100]
	#plt.plot(x,y,label="%i uW" % puiss[i])
#plt.legend()
#plt.show()

with open("contraste.txt",'w') as f :
	for i in range(len(puiss)) :
		f.write("Puissance (uW) \t contraste (%) \n")
		f.write("%i \t %4.3f \n" %(puiss[i],contraste[i]))

plt.plot(puiss,contraste,'x')
plt.show()
