from numpy import cos,sin,sqrt,pi,arccos
import numpy as np
from scipy.integrate import quad, dblquad


#base cistal :
def x(theta,phi):
	return(sin(theta)*cos(phi))

def y(theta,phi):
	return(sin(theta)*sin(phi))

def z(theta,phi):
	return(cos(theta))

#base NV :
#Rappel Numpy : tu rentres les matrices ligne par ligne, et M[i]=ligne(i)
#Ici les lignes représentent les vecteurs dela base du NV (exprimés dans la base x,y,z), et les colonnes les vecteurs x,y,z exprimés dans la base du NV
classe1Rot=np.array([[1/sqrt(2),-1/sqrt(2),0],[1/sqrt(6),1/sqrt(6),-2/(sqrt(6))],[1/sqrt(3),1/sqrt(3),1/sqrt(3)]]) #classe1Rot.dot([1,1,1])=[0,0,1]
classe2Rot=classe1Rot.dot(np.array([[-1,0,0],[0,-1,0],[0,0,1]]))
classe3Rot=classe1Rot.dot(np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
classe4Rot=classe1Rot.dot(np.array([[1,0,0],[0,-1,0],[0,0,-1]]))


# print(classe3Rot.T.dot([0,1,0]))
# print(classe3Rot[1])

classesRot=[classe1Rot,classe2Rot,classe3Rot,classe4Rot]

classNV1=1
classNV2=4
#C'est vraiment pas opti comme façon de faire, mais bon allons y quand meme
x1=classesRot[classNV1-1][0]
y1=classesRot[classNV1-1][1]
z1=classesRot[classNV1-1][2]


# 0.38490017056254233 0.8327775080569433 0.8242328246712349 0.7513109757772565

# 0.7698003602248628 0.6878741656726536

t=pi/4
x2=classesRot[classNV2-1][0]*cos(t)+classesRot[classNV2-1][1]*sin(t)
y2=-(classesRot[classNV2-1][1]*cos(t)-classesRot[classNV2-1][0]*sin(t))
z2=classesRot[classNV2-1][2]




def gp_same(theta,phi):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	res=1/2*(3*x1.dot(r)**2+3*y1.dot(r)**2-2)
	return(res)

def gp_diff(theta,phi):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	res=1/2*(3*x1.dot(r)*x2.dot(r)-x1.dot(x2)+3*y1.dot(r)*y2.dot(r)-y1.dot(y2))
	return(res)

def gm_same(theta,phi):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	res=1/2*(3*x1.dot(r)**2-3*y1.dot(r)**2)
	return(res)

def gm_diff(theta,phi):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	res=1/2*(3*x1.dot(r)*x2.dot(r)-x1.dot(x2)-3*y1.dot(r)*y2.dot(r)+y1.dot(y2))
	return(res)

def hp_diff(theta,phi):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	res=1/2*(3*x1.dot(r)*y2.dot(r)-x1.dot(y2)+3*y1.dot(r)*x2.dot(r)-y1.dot(x2))
	return(res)

def hm_diff(theta,phi):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	res=1/2*(3*x1.dot(r)*y2.dot(r)-x1.dot(y2)-3*y1.dot(r)*x2.dot(r)+y1.dot(x2))
	return(res)

def xx_same(theta,phi):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	res=(3*x1.dot(r)**2-1)
	return(res)

def xx_diff(theta,phi):
	r=[x(theta,phi),y(theta,phi),z(theta,phi)]
	res=(3*x1.dot(r)*x2.dot(r)-x1.dot(x2))
	return(res)

def SQ_xx_same(theta,phi):
	return(1/(4*pi)*abs(xx_same(theta,phi))*sin(theta))

def SQ_xx_diff(theta,phi):
	return(1/(4*pi)*abs(xx_diff(theta,phi))*sin(theta))

eta_same_xx=dblquad(SQ_xx_same,a=0,b=2*pi,gfun=0,hfun=pi)[0]
eta_diff_xx=dblquad(SQ_xx_diff,a=0,b=2*pi,gfun=0,hfun=pi)[0]

print(eta_same_xx,eta_diff_xx)

def SQ_same_mag(theta,phi):
	return(1/(4*pi)*sqrt(gp_same(theta,phi)**2)*sin(theta))


def SQ_diff_mag(theta,phi):
	return(1/(4*pi)*sqrt(gp_diff(theta,phi)**2+hm_diff(theta,phi)**2)*sin(theta))


def SQ_same_pm(theta,phi):
	return(1/(4*pi)*sqrt(gp_same(theta,phi)**2+gm_same(theta,phi)**2)*sin(theta))


def SQ_diff_pm(theta,phi):
	return(1/(4*pi)*sqrt(gp_diff(theta,phi)**2+gm_diff(theta,phi)**2)*sin(theta))

#ATTENTION : f(y,x) pour scipy....

# eta_same_mag=dblquad(SQ_same_mag,a=0,b=2*pi,gfun=0,hfun=pi)[0]
# eta_diff_mag=dblquad(SQ_diff_mag,a=0,b=2*pi,gfun=0,hfun=pi)[0]
# eta_mag=1/4*eta_same_mag+3/4*eta_diff_mag


# eta_same_pm=dblquad(SQ_same_pm,a=0,b=2*pi,gfun=0,hfun=pi)[0]
# eta_diff_pm=dblquad(SQ_diff_pm,a=0,b=2*pi,gfun=0,hfun=pi)[0]
# eta_pm=1/4*eta_same_pm+3/4*eta_diff_pm


# print(eta_same_mag,eta_diff_mag,eta_same_pm,eta_diff_pm)
# print(eta_mag**2,eta_pm**2)


