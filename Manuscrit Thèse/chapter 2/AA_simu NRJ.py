import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *



def plot_NRJ_NV_VH_P1():
	n=500
	DVH=2526
	Brange=np.linspace(0,200,n)
	transi1=np.zeros(n)
	transi2=np.zeros(n)
	transi3=np.zeros(n)
	transi4=np.zeros(n)
	transi5=np.zeros(n)
	transi6=np.zeros(n)
	transi7=np.zeros(n)
	transi8=np.zeros(n)

	for i in range(n):
		B=magneticField(x=0,y=0,z=Brange[i])
		# B=magneticField(x=Brange[i]/sqrt(3),y=Brange[i]/sqrt(3),z=Brange[i]/sqrt(3))
		H=NVHamiltonian(B,c=2,E=3)
		transis=H.transitions()
		transi1[i]=transis[0]
		transi2[i]=transis[1]

		transiP1=2.8*Brange[i]

		H=NVHamiltonian(B,c=1,E=3)
		transis=H.transitions()
		transi3[i]=transis[0]
		transi4[i]=transis[1]

		# transi5[i]=transiP1

		H=NVHamiltonian(B,c=2,E=3,D=DVH)
		transis=H.transitions()
		transi5[i]=transis[0]
		transi6[i]=transis[1]


		H=NVHamiltonian(B,c=1,E=3,D=DVH)
		transis=H.transitions()
		transi7[i]=transis[0]
		transi8[i]=transis[1]

	plt.figure(num=1,figsize=(6,4),dpi=80)
	plt.xticks(fontsize=14)
	plt.yticks(fontsize=14)

	plt.plot(Brange,transi1,color=color(0),label=r'NV')
	plt.plot(Brange,transi2,color=color(0))
	# plt.plot(Brange,transi3,color=color(0),label=r'NV $\nparallel$ B',ls='--')
	# plt.plot(Brange,transi4,color=color(0),ls='--')

	# plt.plot(Brange,transi5,color=color(1),label=r'P1')

	plt.plot(Brange,transi5,color=color(1),label=r'VH')
	plt.plot(Brange,transi6,color=color(1))
	# plt.plot(Brange,transi7,color=color(1),label=r'VH $\nparallel$ B',ls='--')
	# plt.plot(Brange,transi8,color=color(1),ls='--')

	plt.legend()
	plt.show()

plot_NRJ_NV_VH_P1()

def plot_NRJ_NV_C13():
	n=500
	Brange=np.linspace(0,60,n)
	transiNV1=np.zeros((n,2))
	transiNV2=np.zeros((n,2))
	transiC131=np.zeros((n,8))
	transiC132=np.zeros((n,8))
	for i in range(n):
		B=magneticField(x=0,y=0,z=Brange[i])
		# B=magneticField(x=Brange[i]/sqrt(3),y=Brange[i]/sqrt(3),z=Brange[i]/sqrt(3))
		H=NVHamiltonian(B,c=1,E=3)
		transis=H.transitions()
		transiNV1[i,:]=transis

		H=NVHamiltonian(B,c=6,E=3)
		transis=H.transitions()
		transiNV2[i,:]=transis

		H=NV_C13_Hamiltonian(B,c=1,E=3)
		transis=H.transitions()
		transiC131[i,:]=transis

		H=NV_C13_Hamiltonian(B,c=6,E=3)
		transis=H.transitions()
		transiC132[i,:]=transis

	for i in range(len(transiNV1[0,:])):
		if i==0 :
			plt.plot(Brange,transiNV1[:,i],color=color(0),label=r'NV')
		else :
			plt.plot(Brange,transiNV1[:,i],color=color(0))

	for i in range(len(transiC131[0,:])):
		if i==0 :
			plt.plot(Brange,transiC131[:,i],color=color(1),label=r'$^{13}$C-NV')
		else :
			plt.plot(Brange,transiC131[:,i],color=color(1))

	# for i in range(len(transiNV2[0,:])):
	# 	if i==0 :
	# 		plt.plot(Brange,transiNV2[:,i],color=color(0),label=r'NV $\nparallel$ B',ls='--')
	# 	else :
	# 		plt.plot(Brange,transiNV2[:,i],color=color(0),ls='--')

	# for i in range(len(transiC132[0,:])):
	# 	if i==0 :
	# 		plt.plot(Brange,transiC132[:,i],color=color(1),label=r'$^{13}$C-NV $\nparallel$ B',ls='--')
	# 	else :
	# 		plt.plot(Brange,transiC132[:,i],color=color(1),ls='--')


	plt.figure(num=1,figsize=(6,4),dpi=80)
	plt.xticks(fontsize=15)
	plt.yticks(fontsize=15)
	plt.legend()
	plt.show()


# plot_NRJ_NV_C13()