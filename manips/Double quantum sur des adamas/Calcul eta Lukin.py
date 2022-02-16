from numpy import cos,sin,sqrt,pi,arccos
import numpy as np
from scipy.integrate import quad, dblquad, nquad



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


def gp_diff_noC(theta,phi,anglex1=0,anglex2=0):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	x1,y1,z1=cartesian1(anglex1)
	x2,y2,z2=cartesian2(anglex2)
	g=1/2*(3*x1.dot(r)*x2.dot(r)-x1.dot(x2)+3*y1.dot(r)*y2.dot(r)-y1.dot(y2))
	h=1/2*(3*x1.dot(r)*y2.dot(r)-x1.dot(y2)-3*y1.dot(r)*x2.dot(r)+y1.dot(x2))
	integrande=1/(4*pi)*sqrt(g**2+h**2)*sin(theta)#/(2*pi)/(2*pi)
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



def my2Dint(f,xrange,yrange,nx,ny):
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
			h+=pref*f(x,y)*ds
	return h

def my3Dint(f,xrange,yrange,zrange,n):
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
				tot1D+=pref*f(x,y,z)*dz
			tot2D+=tot1D*dy
		tot3D+=tot2D*dx
	return tot3D

def my4Dint(f,wrange,xrange,yrange,zrange,n):
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
					h+=pref*f(w,x,y,z)*ds
	return h


# classNV1=1
# classNV2=1

# eta=my2Dint(xx_diff_fullC,[0,pi],[0,2*pi],300,300) # nx=100 : precision ~1e-4 300 : precision ~1e-7
# # eta=nquad(xx_diff_noC,ranges=[[0,pi],[0,2*pi]])
# print(eta,4/3/sqrt(3))

# eta=my3Dint(xx_diff_noC,[0,pi],[0,2*pi],[0,2*pi],100)/(2*pi) # nx=100 : precision ~1e-4 300 : precision ~1e-7
# print(eta)
#eta_xx_18=0.7697816068506358 #n=200
#eta_xx_11=0.7698153937622911
#eta_yy_11=0.7696949517654613
#eta_yy_18=0.7697745137506845 #n=200


for i in range(1,9):
	classNV1=1
	classNV2=i
	eta=my4Dint(xx_diff_fullC,[0,pi],[0,2*pi],[0,pi],[0,2*pi],100) # nx=100 : precision ~1e-4 300 : precision ~1e-7
	print('NV1-NV%i:'%i,eta)

# classNV1=1
# classNV2=2
# eta=my4Dint(xx_diff_fullC,[0,pi],[0,2*pi],[0,pi],[0,2*pi],100) # nx=100 : precision ~1e-4 300 : precision ~1e-7
# print('NV1-NV2:',eta)




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


# print(4.467346794318131/(2*pi))
# print(26.95422595711054/(4*pi**2))


# print((1/8*0.3849+1/8+3/8*0.8328+3/8*0.6507)**2)
# print((0.7110*1/4+0.6828*3/4)**2)


