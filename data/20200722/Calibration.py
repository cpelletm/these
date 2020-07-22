import numpy as np
import matplotlib.pyplot as plt

def lecture (fichier,sep=None, colonne=0): #colonne=0 => rend le tableau complet
	data=[]
	with open(fichier,"r") as f:	
		for line in f :
			line=line.split(sep)
			try :
				float(line[0])
			except :
				continue
			ligne=[]
			for elem in line :
				ligne+=[float(elem)]
			data+=[ligne]
	npdata=np.array(data)
	if colonne==0 :
		return npdata
	else :
		return npdata[:,colonne-1]
		
def cs(x,n=3): # retourne x avec n chiffres significatifs
	y=round(x,-int(floor(log10(abs(x)))+1-n))
	if y-int(y)==0 :
		y=int(y)
	return str(y)
		
def linfit(x,y): #retourne a,b,label avec f(x)=ax+b 
	A=np.vstack([x,np.ones(len(x))]).T
	a,b=np.linalg.lstsq(A,y,rcond=None)[0]
	lab='fit {0:1.2e}*X{1:+1.2e}'.format(a,b)
	return a,b,lab


		
V=[-2.385,-1.916,-1.434,-0.954,-0.476,0,0.476,0.954,1.434,1.916,2.385]
B=[-145,-116,-87,-56,-25,6,33,58,97,124,146]

V=np.array(V)
B=np.array(B)
a,b,lab=linfit(V,B)
plt.plot(V,B,'x-')
plt.plot(V,a*V+b,label=lab)
plt.legend()
plt.show()
				
        


