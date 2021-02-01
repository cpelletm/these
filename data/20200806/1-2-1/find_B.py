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

def extract_data(filename,xcol=0,ycol=1):
	x=[]
	y=[]
	with open(filename,'r',encoding = "ISO-8859-1") as f:
		for line in f :
			line=line.split()
			try :
				x+=[float(line[xcol])]
				y+=[float(line[ycol])]
			except :
				pass
	return(np.array(x),np.array(y))

def find_nearest(value,array): #suppose the array is sorted
	i=0
	while i<len(array)-1 and array[i]<value :
		diff=value-array[i]
		i+=1
	if i==len(array)-1:
		return i
	elif i==0:
		return i
	elif diff < array[i]-value :
		return i-1
	else :
		return i




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
	
	# err=np.linalg.norm(ESR_peaks-ESR_B)
	err=0
	for i in range(8):
		if ESR_peaks[i]>0 :			
			err+=(ESR_peaks[i]-ESR_B[i])**2
	# err=0
	# ESR_B=list(ESR_B)
	# for peak in ESR_peaks:
	# 	i=find_nearest(peak,ESR_B)
	# 	val=ESR_B.pop(i)
	# 	err+=(peak-val)**2
	err=np.sqrt(err)
	return(err)


def find_B(ESR_peaks):
	sol=minimize(err_func,x0=[100,27.3,22.5],args=ESR_peaks,bounds=[(0,1000),(0,54.74),(0,45)]) #Ca fait 1/16e d'espace, il faudrait 1/48e pour être bijectif mais les expressions deviennent moches

	return sol.x

def test():
	B=mag_field(10,52,28,radian=False)
	ESR=transitions(B)
	print(ESR)

	print(find_B(ESR))
	print(err_func(find_B(ESR),ESR))

	B=mag_field(10,52,62,radian=False)
	ESR=transitions(B)
	print(ESR)

# test()



def cart_to_spher(r):
	x=r[0]
	y=r[1]
	z=r[2]
	xphi=x/np.sqrt(x**2+y**2)
	yphi=y/np.sqrt(x**2+y**2)
	if xphi>-1 :
		phi_r=2*np.arctan(yphi/(xphi+1))
	else :
		phi_r=np.pi
	theta_r=np.arccos(z/np.sqrt(x**2+y**2+z**2))
	if phi_r<0 : #Cartes de 0 à 2pi plutot que de -pi à pi
		phi_r+=2*np.pi
	amp=np.sqrt(x**2+y**2+z**2)
	return(amp,theta_r,phi_r)

def trajet_121():
	ESR=[2574,2696,2849,2892,2962,2994,3108,3181]
	sol=find_B(ESR)
	B1=mag_field(sol[0],sol[1],sol[2],radian=False)
	ESR=[2570,2738,2759,2898,2955,3068,3087,3188]
	sol=find_B(ESR)
	B2=mag_field(sol[0],sol[1],sol[2],radian=False)
	B1_cart=np.array([B1.x,B1.y,B1.z])
	B2_cart=np.array([B2.x,B2.y,B2.z])
	B_diff=(B2_cart-B1_cart)/4
	B3_cart=B1_cart+7.3*B_diff
	B1_cart=B1_cart-0.7*B_diff
	amp,theta,phi=cart_to_spher(B3_cart)
	B3=mag_field(amp,theta,phi,radian=True)
	# return(transitions(B3))
	return(B1_cart,B3_cart)

print(trajet_121())

def check_peaks():
	fname='ESR-meca-0.8V'
	ESR=trajet_121()

	x,y=extract_data(fname+'.txt')
	y=y/max(y)
	x=x*1000
	plt.plot(x,y)

	ax=plt.gca()
	ylim=ax.get_ylim()
	color = next(ax._get_lines.prop_cycler)['color']
	for peak in ESR :
		plt.plot([peak,peak],[0,2],'--',color=color)
	ax.set_ylim(ylim)
	plt.show()

# check_peaks()

# ESR_0V=[2574,2696,2849,2892,2962,2994,3108,3181]
# ESR_04V=[2570,2738,2759,2898,2955,3068,3087,3188]
# ESR=ESR_04V
# print(find_B(ESR))
# print(err_func(find_B(ESR),ESR))
