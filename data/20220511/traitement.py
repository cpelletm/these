import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

fs=[1000,1500,1600,1700,1800,1900,2000]
Vs=[1.45,3.43,3.89,4.52,4.92,5.71,6.52]

# plt.plot(Vs,fs)
# plt.show()
def omega(H):
	# return np.sqrt(H*(H+1760))*1.76e7/(2*np.pi*1e9) #couche mince
	return (H-100)*1.76e7/(2*np.pi*1e9) #bulk Jamal

print(omega(600))