import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


H=NVHamiltonian([0,0,0],c=1,order='traditionnal')
Sz=H.Sz
Sx=H.Sx
Sy=H.Sy
Sz2=H.Sz2

basis=['-1','0','+1']

# print_matrix(Sx.dot(Sz)+Sz.dot(Sx)) #{Sx,Sz}

# print_matrix(Sy.dot(Sz)+Sz.dot(Sy)) #{Sy,Sz}

# print_matrix(Sy.dot(Sy)-Sx.dot(Sx)) #(Sy^2 -Sx^2)

print_matrix(Sx.dot(Sy)+Sy.dot(Sx)) #{Sx,Sy}