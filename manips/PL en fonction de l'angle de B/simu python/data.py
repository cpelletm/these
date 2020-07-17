import numpy as np
from numpy import cos,sin,sqrt,pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



Sz=np.array([[1,0,0],[0,0,0],[0,0,-1]])
Sy=np.array([[0,-1j,0],[1j,0,-1j],[0,1j,0]])/np.sqrt(2)
Sx=np.array([[0,1,0],[1,0,1],[0,1,0]])/np.sqrt(2)
Sz2=np.array([[1,0,0],[0,0,0],[0,0,1]]) # Pour éviter une multilplcation matricielle

c0=np.array([0,0,0])
c1=np.array([-1,1.,-1])/sqrt(3)
c2=np.array([1,1,1])/sqrt(3)
c3=np.array([-1,-1,1])/sqrt(3)
c4=np.array([1,-1,-1])/sqrt(3)

carb=[c0,c1,c2,c3,c4]

sigma=5E6 #Hz
gamma=2.8E6 #Hz.G-1
N=500
h=6.63E-34 #SI
D=2.88E9 #Hz

inhomogenous_broad=0 #Hz
gamma_f=4E6 #Hz

tau_las=1e-4 #s
t1_phonons=3e-3 #s
t1_non_deg=200e-3 #s

mag_field = 100 #G



def ChampMag(theta,phi,amp): #amp en gauss, angles en degrés
    theta=theta*pi/180
    phi=phi*pi/180
    return amp*np.array([sin(theta)*cos(phi),cos(theta),sin(theta)*sin(phi)])



def show(B) :
    def link(ax,c1,c2,linewidth=1,color='blue',linestyle='-'):
        ax.plot3D([c1[0],c2[0]],[c1[1],c2[1]],[c1[2],c2[2]],color=color,linewidth=linewidth,linestyle=linestyle)

    def sphere(ax,c,linewidth=1,color='black'):
        ax.scatter(c[0],c[1],c[2], marker='o',linewidth=linewidth,color=color)


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    B=B/np.linalg.norm(B)/np.sqrt(3)

    for c in carb :
        link(ax,c0,c,2)
        sphere(ax,c,linewidth=10)

    link(ax,B,-B,linewidth=2,color='red')
    sphere(ax,B,linewidth=2,color='red')
    sphere(ax,-B,linewidth=2,color='red')

    c5=np.array([1,1,-1])/sqrt(3)
    c6=np.array([1,-1,1])/sqrt(3)
    c7=np.array([-1,1,1])/sqrt(3)
    c8=np.array([-1,-1,-1])/sqrt(3)

    for arrete in ((c5,c1),(c5,c2),(c5,c4),(c6,c3),(c6,c2),(c6,c4),(c7,c1),(c7,c2),(c7,c3),(c8,c1),(c8,c3),(c8,c4)) :
        link(ax,arrete[0],arrete[1],linewidth=2,color='purple',linestyle=':')

    ax.grid(False)
    ax.axis('off')
    plt.show()

def NRJ(B,c) :
    return gamma*sum(B*c)/sum(c*c)

def Transparence(centres,f) :
    T=0
    for c in centres : 
        T+=0.1/(1+((f-c)/inhomogenous_broad)**2)
    return T

def make_ESR(B) :
    centres=[]
    for c in carb[1:] :
        egva=egv(c,B)
        centres+=[egva[1]-egva[0]]
        centres+=[egva[2]-egva[0]]
    fmax=max(centres)+5*sigma
    fmin=min(centres)-5*sigma
    frange=np.linspace(fmin,fmax,N)
    ESR=np.zeros(N)
    for i in range(N) :
        ESR[i]=1-Transparence(centres,frange[i])
    return frange,ESR

def show_ESR(B) :
    x,y=make_ESR(B)
    plt.plot(x,y)
    plt.show()

#4x = (0,0)
#1x2x1 = (45,45)
#show_ESR(ChampMag(45,45,200))

def map_2D(theta_range,phi_range,amp) :
    imax=len(theta_range)
    jmax=len(phi_range)
    map=np.zeros((imax,jmax))

    for i in range (imax) :
        for j in range(jmax) :
            theta=theta_range[i]
            phi=phi_range[j]
            B=ChampMag(theta,phi,amp)
            map[i,j]=min(make_ESR(B)[1])
        print("%i sur %i" % (i,imax))

    plt.pcolor(phi_range,theta_range,map)

    plt.show()

def rotation_diamond(theta_x,theta_z) : # Rappel : les rotations ne commutent pas à 3D. Rotation en x puis en z
    theta_x=theta_x*pi/180
    theta_z=theta_z*pi/180
    Rotx=np.array([[1,0,0],[0,cos(theta_x),-sin(theta_x)],[0,sin(theta_x),cos(theta_x)]])
    Rotz=np.array([[cos(theta_z),-sin(theta_z),0],[sin(theta_z),cos(theta_z),0],[0,0,1]])
    for i in range(1,len(carb)) :
        carb[i]=Rotx.dot(carb[i])
        carb[i]=Rotz.dot(carb[i])

def egv(c,B) :
    #Il n'y a rien qui quantifie l'axe x et y donc je met toute la partie transverse de B selon x
    Bz=B.dot(c)
    Bx=sqrt(np.linalg.norm(B)**2-Bz**2)
    H=D*Sz2+gamma*Bz*Sz+gamma*Bx*Sx
    egva,egve=np.linalg.eigh(H)
    egva.sort()
    return egva

def map_2D_croisements_rainbow(theta_range,phi_range,amp) :
    imax=len(theta_range)
    jmax=len(phi_range)
    map=np.zeros((imax,jmax))
    egvmoins=np.zeros(4)
    egvplus=np.zeros(4)
    scatter=[[],[],[],[],[],[]]
    for i in range (imax) :
        for j in range(jmax) :
            theta=theta_range[i]
            phi=phi_range[j]
            B=ChampMag(theta,phi,amp)
            for k in range(4) :
                egva=egv(carb[k+1],B)
                egvmoins[k]=egva[1]-egva[0]
                egvplus[k]=egva[2]-egva[0]
            if abs(egvmoins[0]-egvmoins[1]) < sigma :
                scatter[0]+=[[phi,theta]]
            if abs(egvmoins[0]-egvmoins[2]) < sigma :
                scatter[1]+=[[phi,theta]]
            if abs(egvmoins[0]-egvmoins[3]) < sigma :
                scatter[2]+=[[phi,theta]]
            if abs(egvmoins[1]-egvmoins[2]) < sigma :
                scatter[3]+=[[phi,theta]]
            if abs(egvmoins[1]-egvmoins[3]) < sigma :
                scatter[4]+=[[phi,theta]]
            if abs(egvmoins[2]-egvmoins[3]) < sigma :
                scatter[5]+=[[phi,theta]]
            #map[i,j]+=min(abs(egvmoins[0]-egvmoins[1]),2*gamma)
        print("%i sur %i" % (i,imax))

    #plt.pcolor(phi_range,theta_range,map)

    scatter01=np.array(scatter[0])
    scatter02=np.array(scatter[1])
    scatter03=np.array(scatter[2])
    scatter12=np.array(scatter[3])
    scatter13=np.array(scatter[4])
    scatter23=np.array(scatter[5])

    try :
        plt.scatter(scatter01[:,0],scatter01[:,1],color='r',marker=',')
    except :
        pass
    try :
        plt.scatter(scatter02[:,0],scatter02[:,1],color='b',marker=',')
    except :
        pass
    try :
        plt.scatter(scatter03[:,0],scatter03[:,1],color='g',marker=',')
    except :
        pass
    try :
        plt.scatter(scatter12[:,0],scatter12[:,1],color='yellow',marker=',')
    except :
        pass
    try :
        plt.scatter(scatter13[:,0],scatter13[:,1],color='purple',marker=',')
    except :
        pass
    try :
        plt.scatter(scatter23[:,0],scatter23[:,1],color='orange',marker=',')
    except :
        pass

    plt.show()


def PL(B):
    pl=0
    egvmoins=[]
    egvplus=[]
    for c in carb[1:] :
        egva=egv(c,B)
        egvmoins+=[egva[1]-egva[0]]
        egvplus+=[egva[2]-egva[0]]
    for egv1 in egvmoins :
        eta=1
        for egv2 in egvmoins :
            if egv1 != egv2 :
                eta+=1.69*np.sqrt((inhomogenous_broad**2+4*gamma_f**2)/(inhomogenous_broad**2+4*gamma_f**2+(egv1-egv2)**2))
        t1=1/(eta**2/t1_non_deg+1/t1_phonons)
        pl+=(1/tau_las+1/t1)/(1/tau_las+3/t1)*1/4*(1/tau_las+3/t1_phonons)/(1/tau_las+1/t1_phonons)

    return(pl)


    

def map_2D_croisements(theta_range,phi_range,amp) :
    imax=len(theta_range)
    jmax=len(phi_range)
    map=np.zeros((imax,jmax))
    for i in range (imax) :
        for j in range(jmax) :
            theta=theta_range[i]
            phi=phi_range[j]
            B=ChampMag(theta,phi,amp)
            egvtot=[]
            for c in carb[1:] :
                egva=egv(c,B)
                egvtot+=[egva[1]-egva[0]]
                egvtot+=[egva[2]-egva[0]]
            for v1 in egvtot :
                for v2 in egvtot :
                    if abs(v1-v2) < sigma :
                        map[i,j]+=1-abs(v1-v2)/sigma
            map[i,j]=(map[i,j]-8)/2
            #map[i,j]+=min(abs(egvmoins[0]-egvmoins[1]),2*gamma)
        print("%i sur %i" % (i,imax))

    #plt.pcolor(phi_range,theta_range,map)
    fig,ax=plt.subplots()
    ax.set_xlabel(r'$\theta$')
    ax.set_ylabel(r'$\phi$',rotation=0)
    c=ax.pcolormesh(phi_range,theta_range,map)
    fig.colorbar(c,ax=ax)
    plt.show()

def map_transverse_field(theta_range,phi_range,amp=100):
    imax=len(theta_range)
    jmax=len(phi_range)
    map=np.zeros((imax,jmax))
    for i in range (imax) :
        for j in range(jmax) :
            theta=theta_range[i]
            phi=phi_range[j]
            B=ChampMag(theta,phi,amp)
            for c in carb[1:]:
                Bz=B.dot(c)
                Bx=sqrt(np.linalg.norm(B)**2-Bz**2)

                map[i,j]-=Bx

        print("%i sur %i" % (i,imax))

    #plt.pcolor(phi_range,theta_range,map)
    fig,ax=plt.subplots()
    ax.set_xlabel(r'$\theta$')
    ax.set_ylabel(r'$\phi$',rotation=0)
    c=ax.pcolormesh(phi_range,theta_range,map)
    fig.colorbar(c,ax=ax)
    plt.show()       

def map_pl(theta_range,phi_range,amp) :
    imax=len(theta_range)
    jmax=len(phi_range)
    map=np.zeros((imax,jmax))
    for i in range (imax) :
        for j in range(jmax) :
            theta=theta_range[i]
            phi=phi_range[j]
            B=ChampMag(theta,phi,amp)
            map[i,j]=PL(B)
            #map[i,j]+=min(abs(egvmoins[0]-egvmoins[1]),2*gamma)
        print("%i sur %i" % (i,imax))

    #plt.pcolor(phi_range,theta_range,map)
    fig,ax=plt.subplots()
    ax.set_xlabel(r'$\theta$')
    ax.set_ylabel(r'$\phi$',rotation=0)
    c=ax.pcolormesh(phi_range,theta_range,map)
    fig.colorbar(c,ax=ax)
    plt.show()

def line_PL(theta_min,theta_max,phi_min,phi_max,amp):
    theta_range=np.linspace(theta_min,theta_max,N)
    phi_range=np.linspace(phi_min,phi_max,N)

    val=[]
    abscisse=[]
    for i in range(N):
        val+=[PL(ChampMag(theta_range[i],phi_range[i],amp))]
        abscisse+=[np.sqrt((theta_range[i]-theta_range[0])**2+(phi_range[i]-phi_range[0])**2)]

    plt.plot(abscisse,val)
    plt.show()

#egv(carb[1],ChampMag(90,0,100))

#show(ChampMag(90,0,100))

#show([1,1,0])

# rotation_diamond(45,0)


#show_ESR(ChampMag(90,180,100))


map_2D_croisements(np.linspace(0,180,180),np.linspace(0,360,360),100)
#map_2D_croisements(np.linspace(0,180,360),np.linspace(0,360,720),100)
#map_pl(np.linspace(84,96,80),np.linspace(171,189,80),mag_field)
# line_PL(89.9,89.9,171,189,100)



def contraste():
    def line_PL_2(theta_min,theta_max,phi_min,phi_max,amp):
        theta_range=np.linspace(theta_min,theta_max,N)
        phi_range=np.linspace(phi_min,phi_max,N)

        val=[]
        abscisse=[]
        for i in range(N):
            val+=[PL(ChampMag(theta_range[i],phi_range[i],amp))]
            abscisse+=[np.sqrt((theta_range[i]-theta_range[0])**2+(phi_range[i]-phi_range[0])**2)]

        val=val/max(val)
        line=plt.plot(abscisse,val)
        hwhm=1-(1-min(val))/2
        i=0
        while val[i]>hwhm :
            i+=1
        print(tau_las,abscisse[i])
        return line

    for i in range(10):
        global tau_las
        tau_las=(1+(i+1)/10)*1e-3
        line=line_PL_2(86,94,171,171,100)
        line[0].set_label('%e'%tau_las)
    plt.legend()
    plt.show()

#contraste()
#map_transverse_field(np.linspace(0,180,360),np.linspace(0,360,720),100)

def funcanim() :
    for amp in np.arange(100,410,10) :
        plt.clf()
        map_2D_croisements(np.linspace(0,180,360),np.linspace(0,360,720),300)
        plt.savefig('%i_G'%amp)
        print('%i_G'%amp)

#funcanim()










                
        


