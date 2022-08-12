import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

H=NVHamiltonian([0,0,0],c=1,order='traditionnal')
Sz=H.Sz
Sx=H.Sx
Sy=H.Sy
Sz2=H.Sz2

basis=[]
for i in ['-1','0','1']:
	for j in ['-1','0','1']:
		basis+=[i+';'+j]


B=[0,0,0]
HNV=NVHamiltonian(B,c=5,E=4j).H
# print(HNV)
egval,egvect=np.linalg.eigh(HNV)
print(egvect)
print(np.absolute(egvect))

Q=-4.945
# HN=np.array([[-Q,0,0],[0,0,0],[0,0,-Q]])
HN=NVHamiltonian(B,c=5,D=Q,E=0,gamma_e=3e-4).H

Id=np.identity(3)

HNV=convolution(HNV,Id)
HN=convolution(Id,HN)

Azz=-2.162
Axx=-2.62
Ayy=Axx
Hc=Azz*convolution(Sz,Sz)+Axx*convolution(Sx,Sx)+Ayy*convolution(Sy,Sy)
H=HNV+HN+Hc

print_matrix(H,bname=basis)

egval,egvect=np.linalg.eigh(H)
print(egval)
# transism=[egval[3]-egval[0],egval[5]-egval[2],egval[4]-egval[1]]
# transisp=[egval[6]-egval[1],egval[8]-egval[2],egval[7]-egval[0]]
# print(transism,transisp)

# egval=[-4.97764527e+00 -4.91717578e+00 -4.83429122e-03  2.58283465e+03
#   2.58722086e+03  2.58997408e+03  3.14295179e+03  3.14721753e+03
#   3.15003075e+03]