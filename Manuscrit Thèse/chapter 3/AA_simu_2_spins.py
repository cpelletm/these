import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *
from numpy import random

#Fut un temps y'avait du monte-carlo mais j'ai glissé chef. C'était lent en plus
	
plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

#Le vecteur pop c'est (00, 10, 01, 11)



def pop(glas=1e3,g1=300,g2=300,gdd=1000):
	basis=['00','10','01','11']

	#Règle de pouce : ligne=arrivée, colonne = départ
	Mlas=glas*np.array([
		[0,1,1,0],
		[0,0,0,1],
		[0,0,0,1],
		[0,0,0,0]])

	M1=g1*np.array([
		[0,1,0,0],
		[1,0,0,0],
		[0,0,0,1],
		[0,0,1,0]])

	M2=g2*np.array([
		[0,0,1,0],
		[0,0,0,1],
		[1,0,0,0],
		[0,1,0,0]])

	Mdd=gdd*np.array([
		[0,0,0,0],
		[0,0,1,0],
		[0,1,0,0],
		[0,0,0,0]])

	Ms=[Mlas,M1,M2,Mdd]
	M=sum(Ms)
	n=len(M[0,:])
	for j in range(n):
		M[j,j]=-sum(M[:,j])

	M[n-1,:]=np.array([0]*(n-1)+[1])

	X=solve_rate_equation(Mlas,M1,M2,Mdd)
	return (X)


def PL(pop):
	return(pop[0]+0.5*(pop[1]+pop[2]))
	# return(2*pop[0]+pop[1]+pop[2]+0.7*(2*pop[3]+pop[1]+pop[2]))


n=100
gdds=np.linspace(0,10000,n)
g2s=[300,600,900,1200,1500]
PL0=PL(pop())
for g2 in g2s :
	Pls=np.zeros(n)
	for i in range(n):
		Pls[i]=PL(pop(gdd=gdds[i],g2=g2))
	plt.plot(gdds,Pls)
plt.ylim([0.665,0.82])
plt.show()