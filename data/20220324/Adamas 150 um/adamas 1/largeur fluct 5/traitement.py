import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.locator_params(axis='x', nbins=5)

def plot_conversion_V_to_f():
	fnames,fval=extract_glob('ESR')
	n=len(fnames)
	transis=np.zeros((n,2))
	for i in range(n):
		fname=fnames[i]
		x,y=extract_data(fname)
		cs=find_ESR_peaks(x,y,threshold=0.5)
		if len(cs)==2 :
			cs=find_ESR_peaks(x,y,threshold=0.5,precise=True)
			transis[i,:]=cs
		else :
			transis[i,:]=[np.nan,np.nan]

	# plt.plot(transis,'x')

	nmin=40
	nmax=60

	absc=fval[:nmin]+fval[nmax:]
	transi1=list(transis[:nmin,0])+list(transis[nmax:,1])
	transi2=list(transis[:nmin,1])+list(transis[nmax:,0])
	plt.plot(absc,transi1,'x')
	plt.plot(absc,transi2,'x')

	x=np.array(fval)
	popt,yfit=lin_fit(absc,transi1)
	print(popt)
	E1=popt[0]*x+popt[1]
	plt.plot(x,E1)

	popt,yfit=lin_fit(absc,transi2)
	print(popt)
	E2=popt[0]*x+popt[1]
	plt.plot(x,E2)

# popt,yfit=fit_ordre_4(absc,transi1)
# x=np.array(fval)
# E1=sum(popt[-i-1]*x**i for i in range(len(popt)))
# plt.plot(x,E1)

# popt,yfit=fit_ordre_4(absc,transi2)
# x=np.array(fval)
# E2=sum(popt[-i-1]*x**i for i in range(len(popt)))
# plt.plot(x,E2)


# fnames,fval=extract_glob('T1')
# print(fnames)
# n=len(fnames)
# taus=np.zeros(n)
# for i in range(n):
# 	fname=fnames[i]
# 	x,y=extract_data(fname,ycol=5)
# 	T1ph=0.003626
# 	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
# 	taus[i]=popt[1]

# ax1=plt.gca()
# ax1.plot((E2-E1),1/taus)
# ax2=ax1.twinx()

def plot_and_fit_full_ESR():
	x,y=extract_data('ESR avant après (121 au centre)',ycol=5)
	y=y/max(y)
	plt.plot(x,y)
	peaks=find_ESR_peaks(x,y,threshold=0.1)
	popt,yfit=find_nearest_ESR(x,y,peaks=peaks,returnType='cartesian')
	plt.plot(x,yfit)
	print(popt)
	plt.show()


#~~~~Partie transitions théoriques ~~~~~
B1=[38.13731417698277, 62.485689916286, 87.60516054475868]
B2=[46.75349012735024, 25.425444067196413,  90.53037150987437]
n=100
Bxs=np.linspace(B1[0],B2[0],n)
Bys=np.linspace(B1[1],B2[1],n)
Bzs=np.linspace(B1[2],B2[2],n)
transis=np.zeros((n,4))
for i in range(n):
	B=magneticField(x=Bxs[i], y=Bys[i],  z=Bzs[i])
	transis[i,:]=B.transitions4ClassesMoins()

x=np.linspace(4,8,n)
plt.plot(x,transis[:,0],color=color(0),label='Predicted transition')
for i in range(1,len(transis[0,:])):
	plt.plot(x,transis[:,i],color=color(0))

#~~~~~~Partie ODMR ~~~~~~
fnames,fval=extract_glob('ESR')
n=len(fnames)
transis=np.zeros((n,2))
for i in range(n):
	fname=fnames[i]
	x,y=extract_data(fname)
	cs=find_ESR_peaks(x,y,threshold=0.5)
	if len(cs)==2 :
		cs=find_ESR_peaks(x,y,threshold=0.5,precise=True)
		transis[i,:]=cs
	else :
		transis[i,:]=[np.nan,np.nan]

plt.plot(fval,transis[:,0],'o',markerfacecolor="None",ms=5,mew=0.7,color=color(1),label='ODMR measurement')
plt.plot(fval,transis[:,1],'o',markerfacecolor="None",ms=5,mew=0.7,color=color(1))

plt.legend()
plt.show()