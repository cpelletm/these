import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

polas=[0,20,40,60,80,100]
for p in polas :
	x,y=extract_data('scan pola %i deg'%p,ycol=1)
	# y=y/max(y)
	x=x*30+4.2
	plt.plot(x,y,label='%i °'%p)
	plt.legend()

def find_B():
	x,y=extract_data('ESR -2V 0 deg')
	peaks=find_ESR_peaks(x,y)
	print(peaks)
	B=find_B_cartesian_mesh(peaks)
	print(B, B.amp, B.transitions4Classes())

plt.show()