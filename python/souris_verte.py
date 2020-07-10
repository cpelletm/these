import numpy as np 
import matplotlib.pyplot as plt

def time_souris(N) :
	souris=np.zeros((N,2))

	pos_init=np.random.rand(N)
	pos_init=np.sort(pos_init)
	souris[:,0]=pos_init

	rand_vit=np.random.rand(N)
	vit_init=np.zeros(N)
	for i in range(N) :
		if rand_vit[i]>0.5 :
			vit_init[i]=1
		else :
			vit_init[i]=-1
	souris[:,1]=vit_init

	# print('souris=')
	# print(souris)
	t=0
	prems=0
	der=N-1
	while der-prems>=0 :
		tcol=100
		if souris[prems,1] < 0 and souris[prems,0]*60 < tcol :
			tcol=souris[prems,0]*60
			ncol=[prems,prems]

		if souris[der,1] > 0 and (1-souris[der,0])*60 < tcol :
			tcol=(1-souris[der,0])*60
			ncol=[der,der]

		for i in range(prems,der) :
			if souris[i,1]>0 and souris[i+1,1]<0 and (souris[i+1,0]-souris[i,0])*60/2 <tcol :
				tcol=(souris[i+1,0]-souris[i,0])*60/2
				ncol=[i,i+1]

		souris[:,0]=souris[:,0]+souris[:,1]*tcol/60
		t=t+tcol

		if ncol[0]==ncol[1] :
			if ncol[0]==prems :
				prems=prems+1
			elif ncol[0]==der :
				der=der-1
			else :
				print("tu t'es chié frer")
				break
		

		if ncol[0]!=ncol[1] :
			souris[ncol[0],1]=-1
			souris[ncol[1],1]=1

		# print('prems=%f et der=%f'%(prems,der))
		# print('tcol=%f'%tcol)
		# print('ncol=')
		# print(ncol)
		# print('souris=')
		# print(souris)
	return(t)

Ns=range(1,21)
time_Ns=[]
for N in Ns:
	times=np.zeros(500)
	for i in range(len(times)) :
		times[i]=time_souris(N)
	time=sum(times)/len(times)
	time_Ns+=[time]

plt.plot(Ns,time_Ns)
plt.show()


