import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


def plot_NRJ():
	plt.figure(num=1,figsize=(3,2),dpi=80)
	plt.xticks(fontsize=11)
	plt.yticks(fontsize=12)

	n=200
	levels=np.zeros((n,3))
	Bs=np.linspace(0,200,n)
	DeltaE=np.zeros(n)
	DeltaVect=np.zeros(n)
	DeltaVect2=np.zeros(n)




	for i in range(n):
		theta=90*pi/180
		B=Bs[i]
		H=NVHamiltonian(B=[B*sin(theta),0,B*cos(theta)],c=5)
		E=H.egval()
		V=H.egvect()
		levels[i,:]=E
		DeltaE[i]=E[2]-E[1]
		DeltaVect[i]=(V[2].dot([1/sqrt(2),0,1/sqrt(2)]))**2
		DeltaVect2[i]=(V[0].dot([0,1,0]))**2
		
		# DeltaVect[i]=abs(V[2].dot([0,1,0]))
		# DeltaVect[i]=abs(V[0].dot([0,1,0]))


	# f,(ax,ax2)=plt.subplots(2,1,sharex=True)

	# f.set_size_inches((3,2))

	# ax2.plot(Bs,levels[:,0],color=color(0))
	# ax.plot(Bs,levels[:,1],color=color(0))
	# ax.plot(Bs,levels[:,2],color=color(0))

	# ax.spines['bottom'].set_visible(False)
	# ax2.spines['top'].set_visible(False)
	# ax.xaxis.tick_top()
	# ax.tick_params(labeltop=False)  # don't put tick labels at the top
	# ax2.xaxis.tick_bottom()

	# plt.xlabel('Magnetic Field (G)',fontsize=15)



	ax1=plt.gca()
	ax2=ax1.twinx()
	ax1.plot(Bs,DeltaE,'--',lw=2)
	ax1.set_ylabel(r'$E_e - E_d$ (MHz)')
	ax1.set_ylim(0,max(DeltaE)*1.05)
	ax2.plot(Bs,DeltaVect,lw=2,color='r')
	ax2.set_ylim(0.9,1.005)
	ax2.tick_params(labelsize=12)
	plt.show()

# plot_NRJ()

# H=NVHamiltonian(B=[120,0,0],c=5)
# E=H.egval()
# V=H.egvect()
# print(V[0].dot([0,1,0]))
# print(E[2]-E[1])

def plot_map_etats():
	n=100
	Bs=np.linspace(0,50,n)
	thetas=np.linspace(0,180,n)
	data=np.zeros((n,n))
	for i in range(n) :
		for j in range(n):
			B=Bs[i]
			theta=thetas[j]*pi/180
			phi=90*pi/180
			H=NVHamiltonian(B=[B*sin(theta)*cos(phi),B*sin(phi),B*cos(theta)],c=5)
			E=H.egval()
			V=H.egvect()
			if theta < pi/2 :
				mag=abs(V[2].dot([1,0,0]))
				elec=abs(V[2].dot([1/sqrt(2),0,1/sqrt(2)]))
				t=(mag-elec)#/(1-1/sqrt(2))
			else :
				mag=abs(V[2].dot([0,0,1]))
				elec=abs(V[2].dot([1/sqrt(2),0,1/sqrt(2)]))
				t=(mag-elec)#/(1-1/sqrt(2))
			data[i,j]=t

	print_map_2(data,Bs,thetas)

# plot_map_etats()

B=[0,10,0]
H=NVHamiltonian(B=B,c=5,E=4)
V=H.egvect()
print(V)