import matplotlib.pyplot as plt
import numpy as np

files=["scan_p_135uW.txt","scan_p_600uW.txt","scan_p_1350uW.txt"]
puiss=[135,600,1350]
contraste=[]
for i in range(len(files)) :
	x=[]
	y=[]
	with open(files[i]) as f :
		for line in f :
			line=line.split()
			x+=[float(line[0])]
			y+=[float(line[1])]

	avg=sum(y[:50])/len(y[:50])
	y=[v/avg for v in y]
	contraste+=[(1-min(y))*100]
	plt.plot(x,y,label="%i uW" % puiss[i])
plt.legend()
plt.show()

with open("contraste.txt",'w') as f :
	for i in range(len(puiss)) :
		f.write("Puissance (uW) \t contraste (%) \n")
		f.write("%i \t %4.3f \n" %(puiss[i],contraste[i]))

#plt.plot(puiss,contraste,'x')
#plt.show()
