import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

#unité naturelle : Gauss et MHz

D=2870 #Mhz
gamma_e=2.8 #Mhz/gauss

Sz=np.array([[1,0,0],[0,0,0],[0,0,-1]])
Sy=np.array([[0,-1j,0],[1j,0,-1j],[0,1j,0]])*1/np.sqrt(2)
Sx=np.array([[0,1,0],[1,0,1],[0,1,0]])*1/np.sqrt(2)
Sz2=np.array([[1,0,0],[0,0,0],[0,0,1]]) # Pour éviter une multilplcation matricielle

c1=np.array([-1,1.,-1])/np.sqrt(3)
c2=np.array([1,1,1])/np.sqrt(3)
c3=np.array([-1,-1,1])/np.sqrt(3)
c4=np.array([1,-1,-1])/np.sqrt(3)

carb=[c1,c2,c3,c4]

angle_111_theta=np.arccos(1/np.sqrt(3))
angle_111_phi=np.arccos(1/np.sqrt(3)/np.sin(angle_111_theta))

class mag_field() : #l'amplitude est en Gauss
	def __init__(self,amp,theta,phi,radian=True) :
		self.amp=amp
		if not radian :
			theta=theta*np.pi/180
			phi=phi*np.pi/180
		self.theta=theta
		self.phi=phi
		self.z=amp*np.cos(theta)
		self.x=amp*np.sin(theta)*np.cos(phi)
		self.y=amp*np.sin(theta)*np.sin(phi)
		self.vect=np.array([self.x,self.y,self.z])

def Hamiltonian(B,c) : #H est en MHz
	Bz=c.dot(B.vect)
	Bx=np.sqrt(max(sum(x**2 for x in B.vect)-Bz**2,0)) #A cause des arrondis tu peux avoir un Bz plus grand que B en norme
	H=D*Sz2+gamma_e*(Bz*Sz+Bx*Sx)
	return H

def transitions(B) :
	egv=[]
	for c in carb :
		H=Hamiltonian(B,c)
		egva,egve=np.linalg.eigh(H)
		egva=np.sort(egva)
		egv+=[egva[1]-egva[0]]
		egv+=[egva[2]-egva[0]]
	return np.sort(np.array(egv))

def err_func(B_coord,ESR_peaks) :
	ESR_peaks=np.sort(ESR_peaks)
	B=mag_field(B_coord[0],B_coord[1],B_coord[2],radian=False)
	ESR_B=transitions(B)
	err=np.linalg.norm(ESR_peaks-ESR_B)
	return(err)


def find_B(ESR_peaks):
	sol=minimize(err_func,x0=[100,45,45],args=ESR_peaks,bounds=[(0,1000),(50,100),(0,45)])

	return sol.x


def err_func_demi(B_coord,ESR_peaks) :
	ESR_peaks=np.sort(ESR_peaks)
	B=mag_field(B_coord[0],B_coord[1],B_coord[2],radian=False)
	ESR_B=transitions(B)[:4]
	err=np.linalg.norm(ESR_peaks-ESR_B)
	return(err)
def find_B_demi(ESR_peaks):
	sol=minimize(err_func_demi,x0=[100,45,45],args=ESR_peaks,bounds=[(0,1000),(50,100),(0,45)])

	return sol.x
def test():
	B=mag_field(10,128,62,radian=False)
	ESR=transitions(B)
	print(ESR)

	print(find_B(ESR))
	print(err_func(find_B(ESR),ESR))

	B=mag_field(10,52,62,radian=False)
	ESR=transitions(B)
	print(ESR)

ESR=[2657,2727,2765,2831,2980,3031,3060,3106]
print(find_B(ESR))

ESR2=[2687,2687,2790,2790]
B2=find_B_demi(ESR2)
print(B2)
B=mag_field(B2[0],B2[1],B2[2],radian=False)
ESR=transitions(B)
print(ESR)