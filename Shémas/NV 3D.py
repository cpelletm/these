import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.axis('off')
ax.set_box_aspect([1,1,1])





ps_basis=[[0,0,0],[0,2,2],[2,0,2],[2,2,0],[3,3,3],[3,1,1],[1,3,1],[1,1,3]]
ps=ps_basis
ps+=[[p[0]-4,p[1],p[2]] for p in ps_basis]
ps+=[[p[0],p[1]-4,p[2]] for p in ps_basis]
ps+=[[p[0]-4,p[1]-4,p[2]] for p in ps_basis]
ps+=[[p[0],p[1],p[2]-4] for p in ps_basis]
ps+=[[p[0]-4,p[1],p[2]-4] for p in ps_basis]
ps+=[[p[0],p[1]-4,p[2]-4] for p in ps_basis]
ps+=[[p[0]-4,p[1]-4,p[2]-4] for p in ps_basis]

xbounds=[-2,2]
ybounds=xbounds
zbounds=xbounds

newps=[]
for p in ps:
	if p[0]>=xbounds[0] and p[0]<=xbounds[1] and p[1]>=ybounds[0] and p[1]<=ybounds[1] and p[2]>=zbounds[0] and p[2]<=zbounds[1]:
		newps+=[p]
ps=newps

nump_ps=np.array(ps)

xs=nump_ps[:,0]
ys=nump_ps[:,1]
zs=nump_ps[:,2]

ax.scatter(xs,ys,zs,marker='o',s=300,color='black')

for i in range(len(ps)):
	for j in range(i,len(ps)):
		p1=ps[i]
		p2=ps[j]
		if (p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2==3 :
			ax.plot([p1[0],p2[0]],[p1[1],p2[1]],[p1[2],p2[2]],color='red',ls='--')




ax.set_xlim3d(xbounds)
ax.set_ylim3d(ybounds)
ax.set_zlim3d(zbounds[0],zbounds[1])

plt.show()