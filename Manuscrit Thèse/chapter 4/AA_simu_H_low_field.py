import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *
from numpy.random import normal


B=[0,0,0] #x,y,z ; z=axe NV
E=[1,1,1]
eps=np.ones((3,3))*1e-4

Sz=np.array([[-1,0,0],[0,0,0],[0,0,1]])
Sy=np.array([[0,1j,0],[-1j,0,1j],[0,-1j,0]])*1/np.sqrt(2)
Sx=np.array([[0,1,0],[1,0,1],[0,1,0]])*1/np.sqrt(2)

def H_base():
	D=2870 #MHz
	H=D*Sz.dot(Sz)
	return H

def H_mag(B):
	gamma_e=2.8 #MHz/G	
	Bx,By,Bz=B[0],B[1],B[2]
	H_B=gamma_e*(Bz*Sz+Bx*Sx+By*Sy)
	return H_B





def H_elec(E):
	dperp=17e-6 #MHz/(V/cm)
	dpar=0.35e-6
	Ex,Ey,Ez=E[0],E[1],E[2]
	H_E=dpar*Sz.dot(Sz)*Ez+dperp*((Sy.dot(Sy)-Sx.dot(Sx))*Ex+(Sx.dot(Sy)+Sy.dot(Sx))*Ey)
	return H_E

# B=[100,0,0]
# E=[0,1e5,0]
# # print_matrix(H_base()+H_mag(B))
# H=H_base()+H_mag(B)+H_elec(E)
# egval,egvec=np.linalg.eigh(H)
# print(egval)
# print_matrix(egvec)



def H_strain(eps):
	h43=2300 #MHz/strain (strain=tenseur de déformation = sans unité dx/x)
	h41=-6420
	h15=5700
	h16=19660
	exx,eyy,ezz,ezx,ezy,exy=eps[0,0],eps[1,1],eps[2,2],eps[0,2],eps[1,2],eps[0,1]
	H_S=(h41*(exx+eyy)+h43*ezz)*Sz.dot(Sz)+1/2*(h16*ezx-1/2*h15*(exx-eyy))*(Sy.dot(Sy)-Sx.dot(Sx))+1/2*(h16*ezy+h15*exy)*(Sx.dot(Sy)+Sy.dot(Sx))
	return H_S

# eps=normal(loc=0,scale=1e-4,size=(3,3))
# print(eps)
# print_matrix(H_strain(eps))


def simu():
	n=100000
	transis=np.zeros((n,2))
	transisfull=np.zeros(2*n)
	for i in range(n):
		B=normal(loc=0,scale=2,size=3)
		B=B/norm(B)*500
		H=H_base()+H_mag(B)
		# E=normal(loc=0,scale=2e5,size=3)
		# E=np.random.standard_cauchy(size=3)*2e5 #Ca correspond mieux avec un E Lorentzien. Je vais aps trop chercher à comprendre c'est deja assez le bordel
		# H=H_base()+H_elec(E)
		# eps=normal(loc=0,scale=2e-4,size=(3,3))
		# H=H_base()+H_strain(eps)
		egval,egvec=np.linalg.eigh(H)
		transis[i,:]=[egval[1]-egval[0],egval[2]-egval[0]]
		transisfull[2*i]=egval[1]-egval[0]
		transisfull[2*i+1]=egval[2]-egval[0]


	plt.figure(num=1,figsize=(6,4),dpi=80)
	plt.xticks(fontsize=15)
	plt.yticks(fontsize=15)
	plt.locator_params(axis='x', nbins=5)

	nbins=200
	x1,y1=make_hist(transis[:,0],bins=nbins)
	# plt.plot(x1,y1)
	x2,y2=make_hist(transis[:,1],bins=nbins)
	# plt.plot(x2,y2)
	x,y=np.concatenate((x1,x2)),np.concatenate((y1,y2))
	x,y=sort_y_by_x(x,y)
	y=y/max(y)
	# plt.plot(x,y)

	x,y=make_hist(transisfull,bins=2*nbins,range=(1300,4500))
	y=y/max(y)
	plt.plot(x,y)

	plt.show()

simu()

def transverse_field_fit_quadratique():
	n=500
	Bs=np.linspace(0,200,n)
	egvs=np.zeros((n,3))
	for i in range(n):
		B=[Bs[i],0,0]
		H=H_base()+H_mag(B)
		egval,egvec=np.linalg.eigh(H)
		egvs[i,:]=egval
	# plt.plot(Bs,egvs)
	x,y=Bs,egvs[:,0]
	plt.plot(x,y)
	popt,yfit=quad_fit(x,y)
	plt.plot(x,yfit)
	print(popt,2.8**2/2870)
	plt.show()