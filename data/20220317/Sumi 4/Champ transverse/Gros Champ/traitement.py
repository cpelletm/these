import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


def Bordel_de_fit_ESR_qui_marche_pas():
	x,y=extract_data('ESR 2V')
	transis=np.array([2689.02447582, 2761.97766014, 2825.9010151 , 2882.65492013,
	       2900.64102652, 2953.41963893, 3006.0502681 , 3059.22930437])
	Bmax=200
	for i in range(10):
		startingB=magneticField(*np.random.random(3)*Bmax)
		B=find_B_cartesian(transis,startingB=startingB,Bmax=Bmax)
		err=np.linalg.norm(transis-B.transitions4Classes())
		print(err)

def simu_champ_transverse():
	amps=np.linspace(0,200,200)
	transi1=[]
	transi2=[]

	for amp in amps:
		B=magneticField(theta=0,phi=np.pi/4,amp=amp)
		transi1+=[B.transitions4Classes()[2]]
		transi2+=[B.transitions4Classes()[4]]

	plt.plot(amps,transi1)
	plt.plot(amps,transi2)

	plt.show()

simu_champ_transverse()