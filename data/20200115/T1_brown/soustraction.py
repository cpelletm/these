import numpy as np
import matplotlib.pyplot as plt

nu=[]
pl=[]
pl2=[]
with open('T1chpnul_p2-mioff.txt') as f:
	c=f.read()
	c=c.split('\n')
	for line in c[2:]:
		line=line.split()
		if line != [] :
			nu+=[float(line[0])]
			pl+=[float(line[1])]

with open('T1chpnul_p2-mion.txt') as f:
	c=f.read()
	c=c.split('\n')
	for line in c[2:]:
		line=line.split()
		if line != [] :
			pl2+=[float(line[1])]

nu=np.array(nu)
pl=np.array(pl)
pl2=np.array(pl2)



with open('soustraction.txt', 'w') as f:
	for i in range(len(nu)):
		f.write('%6.5E \t %6.5E \n'%(nu[i],pl[i]-pl2[i]))

plt.plot(nu,pl-pl2)		
plt.show()