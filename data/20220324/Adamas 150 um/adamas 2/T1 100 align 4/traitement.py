import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


def find_transis():
	fnames,fval=extract_glob('ESR')
	del (fnames[187])
	del fval[187]
	n=len(fnames)
	fval=fval[:n]
	transis=np.zeros((n,2))
	for i in range(n):
		fname=fnames[i]
		x,y=extract_data(fname)
		cs=find_ESR_peaks(x,y,threshold=0.5)
		if len(cs)==2 :
			cs=find_ESR_peaks(x,y,threshold=0.5,precise=True)
			transis[i,:]=cs
		else :
			print('toto',i)
			transis[i,:]=[np.nan,np.nan]

	plt.plot(fval,transis)

def plot_HWHM():
	fnames,fval=extract_glob('ESR')
	del (fnames[187])
	del fval[187]
	HWHMs=np.zeros((len(fnames),2))
	for k in range(len(fnames)):
		fname=fnames[k]
		x,y=extract_data(fname)
		trueCs=find_ESR_peaks(x,y,threshold=0.5,precise=False)
		cs=find_ESR_peaks(x,y,threshold=0.5,precise=False)
		n=find_elem(cs[0],x)
		Vmax=y[n]
		i=n
		while abs(y[i]-Vmax) < Vmax/2:
			i=i+1
		HWHM1=abs(x[i]-trueCs[0])

		n=find_elem(cs[1],x)
		Vmax=y[n]
		i=n
		while abs(y[i]-Vmax) < Vmax/2:
			i=i-1
		HWHM2=abs(x[i]-trueCs[1])
		HWHMs[k,:]=[HWHM1,HWHM2]

	plt.plot(fval, HWHMs)


# plot_HWHM()


def plot_T1():
	fnames,fval=extract_glob('T1')
	n=len(fval)
	fnames2=[]
	fval2=[]
	for i in range(n):
		if  i%2 :
			fnames2+=[fnames[i]]
			fval2+=[fval[i]]

	fnames,fval=fnames2,fval2
	n=len(fval)

	taus=np.zeros(n)

	nmax=-1

	for i in range(n):
		fname=fnames[i]
		x,y=extract_data(fname,ycol=5)
		x=x[:nmax]
		y=y[:nmax]
		T1ph=0.00277119
		popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
		taus[i]=popt[1]

	plt.plot(fval,1/taus)

plot_T1()

plt.show()

