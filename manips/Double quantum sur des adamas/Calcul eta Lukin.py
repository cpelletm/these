from numpy import cos,sin,sqrt,pi,arccos
import numpy as np
from scipy.integrate import quad, dblquad, nquad
from numpy.linalg import norm



#base cistal :
def x(theta,phi):
	return(sin(theta)*cos(phi))

def y(theta,phi):
	return(sin(theta)*sin(phi))

def z(theta,phi):
	return(cos(theta))

#base NV :
#Rappel Numpy : tu rentres les matrices ligne par ligne, et M[i]=ligne(i)
#Ici les lignes représentent les vecteurs de la base du NV (exprimés dans la base x,y,z), et les colonnes les vecteurs x,y,z exprimés dans la base du NV
classe1Rot=np.array([[1/sqrt(2),-1/sqrt(2),0],[1/sqrt(6),1/sqrt(6),-2/(sqrt(6))],[1/sqrt(3),1/sqrt(3),1/sqrt(3)]]) #classe1Rot.dot([1,1,1])=[0,0,1]
classe2Rot=classe1Rot.dot(np.array([[-1,0,0],[0,-1,0],[0,0,1]]))#Pi rotation ("big" diagonal=NV)
classe3Rot=classe1Rot.dot(np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
classe4Rot=classe1Rot.dot(np.array([[1,0,0],[0,-1,0],[0,0,-1]]))

#Rappel : une matrice de passage de determinant -1 (eg symmétrie plane) no conserve pas le trièdre direct. Privilégier des matrices de rotations qui sont toujours det=1
classe5Rot=classe1Rot.dot(np.array([[0,1,0],[-1,0,0],[0,0,1]]))#Pi/2 rotation ("small" diagonal=VN)
classe6Rot=classe1Rot.dot(np.array([[1,0,0],[0,0,1],[0,-1,0]]))
classe7Rot=classe1Rot.dot(np.array([[0,0,-1],[0,1,0],[1,0,0]]))
classe8Rot=classe1Rot.dot(np.array([[0,-1,0],[-1,0,0],[0,0,-1]]))# VN for the class 1 (complicated rotation)


# print(classe3Rot.T.dot([0,1,0]))
# print(classe3Rot[1])

classesRot=[classe1Rot,classe2Rot,classe3Rot,classe4Rot,classe5Rot,classe6Rot,classe7Rot,classe8Rot]



def cartesian1(anglex):
	x1=classesRot[classNV1-1][0]*cos(anglex)+classesRot[classNV1-1][1]*sin(anglex)
	y1=classesRot[classNV1-1][1]*cos(anglex)-classesRot[classNV1-1][0]*sin(anglex)
	z1=classesRot[classNV1-1][2]
	return(x1,y1,z1)

def cartesian2(anglex):
	x2=classesRot[classNV2-1][0]*cos(anglex)+classesRot[classNV2-1][1]*sin(anglex)
	y2=(classesRot[classNV2-1][1]*cos(anglex)-classesRot[classNV2-1][0]*sin(anglex))
	z2=classesRot[classNV2-1][2]
	return(x2,y2,z2)


#Legacy
def xx_diff_noC(theta,phi,anglex1=0,anglex2=1):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	x1,y1,z1=cartesian1(anglex1)
	x2,y2,z2=cartesian2(anglex2)
	g=(3*x1.dot(r)*x2.dot(r)-x1.dot(x2))
	integrande=1/(4*pi)*abs(g)*sin(theta)#/(2*pi)#/(2*pi)
	return(integrande)
def xx_diff_fullC(theta_r,phi_r,theta_E=0,phi_E=0):
	r=np.array([x(theta_r,phi_r),y(theta_r,phi_r),z(theta_r,phi_r)])
	E=np.array([x(theta_E,phi_E),y(theta_E,phi_E),z(theta_E,phi_E)])

	z1=classesRot[classNV1-1][2]
	x1=E-(E.dot(z1))*z1
	x1=x1/np.linalg.norm(x1)
	y1=np.cross(z1,x1)

	z2=classesRot[classNV2-1][2]
	x2=E-(E.dot(z2))*z2
	x2=x2/np.linalg.norm(x2)
	y2=np.cross(z2,x2)
	# x2=-x2 #Anticorrelation
	# y2=-y2


	g=(3*x1.dot(r)*x2.dot(r)-x1.dot(x2))
	integrande=1/(4*pi)*abs(g)*sin(theta_r)*1/(4*pi)*sin(theta_E)
	return(integrande)
def yy_diff_noC(theta,phi,anglex1=0,anglex2=0):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	x1,y1,z1=cartesian1(anglex1)
	x2,y2,z2=cartesian2(anglex2)
	g=(3*y1.dot(r)*y2.dot(r)-y1.dot(y2))
	integrande=1/(4*pi)*abs(g)*sin(theta)#/(2*pi)#/(2*pi)
	return(integrande)
def xy_diff_noC(theta,phi,anglex1=0,anglex2=0):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	x1,y1,z1=cartesian1(anglex1)
	x2,y2,z2=cartesian2(anglex2)
	g=(3*x1.dot(r)*y2.dot(r)-x1.dot(y2))
	integrande=1/(4*pi)*abs(g)*sin(theta)#/(2*pi)/(2*pi)
	return(integrande)
def xy_diff_fullC(theta_r,phi_r,theta_E=0,phi_E=0):
	r=np.array([x(theta_r,phi_r),y(theta_r,phi_r),z(theta_r,phi_r)])
	E=np.array([x(theta_E,phi_E),y(theta_E,phi_E),z(theta_E,phi_E)])

	z1=classesRot[classNV1-1][2]
	x1=E-(E.dot(z1))*z1
	x1=x1/np.linalg.norm(x1)
	y1=np.cross(z1,x1)

	z2=classesRot[classNV2-1][2]
	x2=E-(E.dot(z2))*z2
	x2=x2/np.linalg.norm(x2)
	y2=np.cross(z2,x2)
	# x2=-x2 #Anticorrelation
	# y2=-y2


	g=(3*x1.dot(r)*y2.dot(r)-x1.dot(y2))
	integrande=1/(4*pi)*abs(g)*sin(theta_r)*1/(4*pi)*sin(theta_E)
	return(integrande)
def gp_diff_fullC(theta_r,phi_r,theta_E=pi/2,phi_E=0):
	r=np.array([x(theta_r,phi_r),y(theta_r,phi_r),z(theta_r,phi_r)])
	E=np.array([x(theta_E,phi_E),y(theta_E,phi_E),z(theta_E,phi_E)])

	z1=classesRot[classNV1-1][2]
	x1=E-(E.dot(z1))*z1
	x1=x1/np.linalg.norm(x1)
	y1=np.cross(z1,x1)


	z2=classesRot[classNV2-1][2]
	x2=E-(E.dot(z2))*z2
	x2=x2/np.linalg.norm(x2)
	y2=np.cross(z2,x2)

	g=1/2*(3*x1.dot(r)*x2.dot(r)-x1.dot(x2)+3*y1.dot(r)*y2.dot(r)-y1.dot(y2))
	h=1/2*(3*x1.dot(r)*y2.dot(r)-x1.dot(y2)-3*y1.dot(r)*x2.dot(r)+y1.dot(x2))
	integrande=1/(4*pi)*sqrt(g**2+h**2)*sin(theta_r)#/(2*pi)/(2*pi)
	return(integrande)


#Actual

def sq_mag(theta,phi,anglex1=0,anglex2=0):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	x1,y1,z1=cartesian1(anglex1)
	x2,y2,z2=cartesian2(anglex2)
	g=1/2*(3*x1.dot(r)*x2.dot(r)-x1.dot(x2)+3*y1.dot(r)*y2.dot(r)-y1.dot(y2))
	h=1/2*(3*x1.dot(r)*y2.dot(r)-x1.dot(y2)-3*y1.dot(r)*x2.dot(r)+y1.dot(x2))
	integrande=1/(4*pi)*sqrt(g**2+h**2)*sin(theta)#/(2*pi)/(2*pi)
	return(integrande)

def pure_dq_mag(theta,phi,anglex1=0,anglex2=0):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	x1,y1,z1=cartesian1(anglex1)
	x2,y2,z2=cartesian2(anglex2)
	g=1/2*(3*x1.dot(r)*x2.dot(r)-x1.dot(x2)-3*y1.dot(r)*y2.dot(r)+y1.dot(y2))
	h=1/2*(3*x1.dot(r)*y2.dot(r)-x1.dot(y2)+3*y1.dot(r)*x2.dot(r)-y1.dot(x2))
	integrande=1/(4*pi)*sqrt(g**2+h**2)*sin(theta)#/(2*pi)/(2*pi)
	return(integrande)

def full_dq_mag(theta,phi,anglex1=0,anglex2=0,dqratio=0.5):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	x1,y1,z1=cartesian1(anglex1)
	x2,y2,z2=cartesian2(anglex2)
	gsq=1/2*(3*x1.dot(r)*x2.dot(r)-x1.dot(x2)+3*y1.dot(r)*y2.dot(r)-y1.dot(y2))
	hsq=1/2*(3*x1.dot(r)*y2.dot(r)-x1.dot(y2)-3*y1.dot(r)*x2.dot(r)+y1.dot(x2))
	gdq=1/2*(3*x1.dot(r)*x2.dot(r)-x1.dot(x2)-3*y1.dot(r)*y2.dot(r)+y1.dot(y2))
	hdq=1/2*(3*x1.dot(r)*y2.dot(r)-x1.dot(y2)+3*y1.dot(r)*x2.dot(r)-y1.dot(x2))
	integrande=1/(4*pi)*sqrt(gsq**2+gdq**2*dqratio+hsq**2+hdq**2*dqratio)*sin(theta)#/(2*pi)/(2*pi)
	return(integrande)

def sq_elec(theta,phi,anglex1=0,anglex2=0,corr=False):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	if corr :
		theta_E=anglex1 #Attention faudra bien normaliser anglex1 juste sur [0,pi]
		phi_E=anglex2
		x1,y1,z1=cartesian1(0)
		x2,y2,z2=cartesian2(0)
		E=np.array([x(theta_E,phi_E),y(theta_E,phi_E),z(theta_E,phi_E)]) 
		Eperp1=E.dot(x1)*x1+E.dot(y1)*y1
		x1=Eperp1/norm(Eperp1)
		y1=np.cross(z1,x1)
		Eperp2=E.dot(x2)*x2+E.dot(y2)*y2
		x2=Eperp2/norm(Eperp2)
		y2=np.cross(z2,x2)
		#Attention : pb de sampling de E, faudrait normaliser avec sin(theta) et tout...
	else :		
		x1,y1,z1=cartesian1(anglex1)
		x2,y2,z2=cartesian2(anglex2)

	g=(3*x1.dot(r)*x2.dot(r)-x1.dot(x2))
	if corr :
		integrande=1/(4*pi)*abs(g)*sin(theta)*sin(theta_E)
	else :
		integrande=1/(4*pi)*abs(g)*sin(theta)#/(2*pi)#/(2*pi)
	return(integrande)

def pure_dq_elec(theta,phi,anglex1=0,anglex2=0,corr=False):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	if corr :
		theta_E=anglex1 #Attention faudra bien normaliser anglex1 juste sur [0,pi]
		phi_E=anglex2
		x1,y1,z1=cartesian1(0)
		x2,y2,z2=cartesian2(0)
		E=np.array([x(theta_E,phi_E),y(theta_E,phi_E),z(theta_E,phi_E)]) 
		Eperp1=E.dot(x1)*x1+E.dot(y1)*y1
		x1=Eperp1/norm(Eperp1)
		y1=np.cross(z1,x1)
		Eperp2=E.dot(x2)*x2+E.dot(y2)*y2
		x2=Eperp2/norm(Eperp2)
		y2=np.cross(z2,x2)
		#Attention : pb de sampling de E, faudrait normaliser avec sin(theta) et tout...
	else :		
		x1,y1,z1=cartesian1(anglex1)
		x2,y2,z2=cartesian2(anglex2)
	g=(3*x1.dot(r)*y2.dot(r)-x1.dot(y2))
	if corr :
		integrande=1/(4*pi)*abs(g)*sin(theta)*sin(theta_E)
	else :
		integrande=1/(4*pi)*abs(g)*sin(theta)#/(2*pi)/(2*pi)
	return(integrande)

def full_dq_elec(theta,phi,anglex1=0,anglex2=0,dqratio=0.5,corr=False):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	if corr :
		theta_E=anglex1 #Attention faudra bien normaliser anglex1 juste sur [0,pi]
		phi_E=anglex2
		x1,y1,z1=cartesian1(0)
		x2,y2,z2=cartesian2(0)
		E=np.array([x(theta_E,phi_E),y(theta_E,phi_E),z(theta_E,phi_E)]) 
		Eperp1=E.dot(x1)*x1+E.dot(y1)*y1
		x1=Eperp1/norm(Eperp1)
		y1=np.cross(z1,x1)
		Eperp2=E.dot(x2)*x2+E.dot(y2)*y2
		x2=Eperp2/norm(Eperp2)
		y2=np.cross(z2,x2)
		#Attention : pb de sampling de E, faudrait normaliser avec sin(theta) et tout...
	else :		
		x1,y1,z1=cartesian1(anglex1)
		x2,y2,z2=cartesian2(anglex2)
	gsq=(3*x1.dot(r)*x2.dot(r)-x1.dot(x2))
	gdq=(3*x1.dot(r)*y2.dot(r)-x1.dot(y2))
	if corr :
		integrande=1/(4*pi)*np.sqrt(gsq**2+gdq**2*dqratio)*sin(theta)*sin(theta_E)
	else :
		integrande=1/(4*pi)*np.sqrt(gsq**2+gdq**2*dqratio)*sin(theta)#/(2*pi)/(2*pi)
	return(integrande)

def my2Dint(f,xrange,yrange,nx,ny,**kwarg):
	xs=np.linspace(xrange[0],xrange[1],nx+1)
	dx=xs[1]-xs[0]
	ys=np.linspace(yrange[0],yrange[1],ny+1)
	dy=ys[1]-ys[0]
	ds=dx*dy
	h=0
	for i in range(nx+1):
		x=xs[i]
		for j in range(ny+1):
			y=ys[j]
			pref=1
			if i==0 or i==nx :
				pref*=0.5
			if j==0 or j==nx :
				pref*=0.5
			h+=pref*f(x,y,**kwarg)*ds
	return h

def my3Dint(f,xrange,yrange,zrange,n,**kwarg):
	xs=np.linspace(xrange[0],xrange[1],n+1)
	dx=xs[1]-xs[0]
	ys=np.linspace(yrange[0],yrange[1],n+1)
	dy=ys[1]-ys[0]
	zs=np.linspace(zrange[0],zrange[1],n+1)
	dz=zs[1]-zs[0]
	tot3D=0
	for i in range(n+1):
		print('2D %i sur %i'%(i,n))
		x=xs[i]
		tot2D=0
		if i==0 or i==n :
			xpref=0.5
		else :
			xpref=1
		for j in range(n+1):
			y=ys[j]
			tot1D=0
			if j==0 or j==n :
				ypref=0.5
			else :
				ypref=1
			for k in range(n+1) :
				z=zs[k]
				if k==0 or k==n :
					zpref=0.5
				else :
					zpref=1
				pref=xpref*ypref*zpref
				tot1D+=pref*f(x,y,z,**kwarg)*dz
			tot2D+=tot1D*dy
		tot3D+=tot2D*dx
	return tot3D

def my4Dint(f,wrange,xrange,yrange,zrange,n,**kwarg):
	ws=np.linspace(wrange[0],wrange[1],n+1)
	dw=ws[1]-ws[0]
	xs=np.linspace(xrange[0],xrange[1],n+1)
	dx=xs[1]-xs[0]
	ys=np.linspace(yrange[0],yrange[1],n+1)
	dy=ys[1]-ys[0]
	zs=np.linspace(zrange[0],zrange[1],n+1)
	dz=zs[1]-zs[0]
	ds=dx*dy*dz*dw
	h=0
	for l in range(n+1):
		w=ws[l]
		if l==0 or l==n :
			wpref=0.5
		else :
			wpref=1
		for i in range(n+1):
			# print('2D %i sur %i ; 3D %i sur %i'%(i,n,l,n))
			x=xs[i]
			if i==0 or i==n :
				xpref=0.5
			else :
				xpref=1
			for j in range(n+1):
				y=ys[j]
				if j==0 or j==n :
					ypref=0.5
				else :
					ypref=1
				for k in range(n+1) :
					z=zs[k]
					if k==0 or k==n :
						zpref=0.5
					else :
						zpref=1
					pref=xpref*ypref*zpref*wpref
					h+=pref*f(w,x,y,z,**kwarg)*ds
	return h

#flip flop
# eta0=(2/(3*sqrt(3))/4)**2
# eta121=(2/(3*sqrt(3))/4+0.8328/4)**2
# eta22=(2/(3*sqrt(3))/4+0.6507/4)**2
# eta31=(2/(3*sqrt(3))/4+2*0.8328/4)**2
# eta40mag=(2/(3*sqrt(3))/4+0.8328/4+2*0.6507/4)**2
# eta40EnoC=(0.7110/4+3*0.6828/4)**2
# eta40EfullC=(0.7698/4+3*0.6951/4)**2
# print(eta40EfullC,eta40EfullC/eta0)
#DQ
# eta40mag=(1/4+2*0.8328/4+0.6507/4)**2
# eta40EnoC=(0.7110/4+3*0.6828/4)**2
# eta40EfullC=(0.6366/4+3*0.6705/4)**2



# classNV1=1
# classNV2=2
# eta=my2Dint(full_dq_mag,[0,pi],[0,2*pi],300,300) # nx=100 : precision ~1e-4 300 : precision ~1e-7

# eta=my3Dint(sq_elec,[0,pi],[0,2*pi],[0,2*pi],100)/(2*pi)

# eta=my4Dint(sq_elec,[0,pi],[0,2*pi],[0,2*pi],[0,2*pi],corr=False,100)/(2*pi)/(2*pi)

# classNV1=1
# classNV2=1
# eta=my4Dint(full_dq_elec,[0,pi],[0,2*pi],[0,2*pi],[0,2*pi],100,corr=False,dqratio=0.5)/((2*pi)**2)
# print('Class 11, full dq, no corr, dq=0.5',eta)


eta2=(1/4*0.8702+2/4*0.9373+1/4*1.0074)**2
print(eta2,eta2/(9.259e-3))

# opts={}
# opts['epsrel']=1e-4
# opts['epsabs']=1e-4
# #Attention : diviser par 2*pi
# classNV1=1
# classNV2=2
# eta=nquad(gp_diff_noC,ranges=[[0,pi],[0,2*pi]],opts=opts)
# print(eta)

# opts={}
# opts['epsrel']=1e-4
# opts['epsabs']=1e-4
# #Attention : diviser par 2*pi
# classNV1=1
# classNV2=1
# eta=nquad(xx_diff_noC,ranges=[[0,pi],[0,2*pi],[0,2*pi]],opts=opts)
# print('NV1-NV1:',eta)



