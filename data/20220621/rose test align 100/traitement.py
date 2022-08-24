import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

angle_str=['-3','-2','-1','0','1','2','3']
angle_str_legend=['-3','-2','-1','0','+1','+2','+3']
angle_val=[-3,-2,-1,0,1,2,3]

filenames=['align '+s+' deg' for s in angle_str]

Vm=-1.47 #V pour Vh- neg
Vp=1.35 #V pour Vh- pos
xmin=120
xmax=400

for i in range(7):
	f=filenames[i]
	x,y=extract_data(f,xcol=2,ycol=3)
	x=x*(112/(Vp-Vm))+(56-112/(Vp-Vm)*Vp) #fier de moi pour celui-la, j'avais pierre delezoide qui me regardait depuis la tombe
	y=y/max(y)
	x=x[xmin:xmax]
	y=y[xmin:xmax]
	plt.plot(x,y,label=angle_str_legend[i]+'°')

plt.legend()
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()