import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('D:\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

with open('spectre (0,3) pleine puissance sans filtre.asc') as f :
	for line in f:
		print(line)
