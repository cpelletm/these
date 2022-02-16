import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

Cs=[]
for i in [-1,1]:
	for j in [-1,1]:
		for k in [-1,1]:
			Cs+=[[i,j,k]]

def line_coord(v1,v2):
	return([v1[0],v2[0]],[v1[1],v2[1]],[v1[2],v2[2]])

# for i in range(8):
# 	for j in range(i,8):
# 		if j-i==1 or j-i==2 or j-i==4 :
# 			ax.plot([Cs[i][0],Cs[j][0]],[Cs[i][1],Cs[j][1]],[Cs[i][2],Cs[j][2]])

for (i,j) in [(0,1),(1,3),(3,2),(2,0),(0,4),(1,5),(2,6),(3,7),(4,5),(5,7),(7,6),(6,4)]:
	ax.plot(*line_coord(Cs[i],Cs[j]),color='blue',ls='dashed')

for i in {0,1,7}:
	ax.plot(*line_coord(Cs[i],[0,0,0]),color='red')


plt.show()