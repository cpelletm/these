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


		
def s1():
	data=lecture("s1")
	plt.plot(data[:,0],data[:,1],'b-x',label='label',ms=7, mew=3)
	plt.xlabel('Axe x')
	plt.ylabel('Axe y')
	
notes=[16,19,15.5,10,15.5,15,15,13.5,16.5,19.5,18,15,13.5,26,17.5,19,14.5,14.5,15,14,23.5,17,21,15,20,22.5,11,16,13,17.5,16,11.5]
notes=np.array(notes)
print(sum(notes)/len(notes))
plt.hist(notes)
plt.show()

				
        


