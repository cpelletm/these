import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from analyse import *

def findB():
	fnames=glob.glob('*.csv')
	taus=[]
	alphas=[]
	vs=[]
	Bs=[]
	xmin=0
	xmax=60
	xmin2=80
	xmax2=-1
	for i in range(len(fnames)):
		if fnames[i][2]=='-' :
			v=-float(fnames[i][3:-7])
		else :
			v=float(fnames[i][2:-7])
		vs+=[v]
		x,y=extract_data(fnames[i],xcol=6,ycol=7)
		cs=find_ESR_peaks(x,y)
		Bs+=[(max(cs)-min(cs))/(2*2.8)]

		# x,y=extract_data(fnames[i],xcol=4,ycol=5)
		# # popt,yfit=stretch_arb_exp_fit(x,y)
		# # alphas+=[popt[3]]
		# popt,yfit=stretch_arb_exp_fit(x,y,alpha=0.85,fixed=True)
		# taus+=[popt[2]]

	Bs=[x for _, x in sorted(zip(vs, Bs))]
	vs=sorted(vs)
	vs=vs[xmin:xmax]+vs[xmin2:xmax2]
	Bs=np.array(Bs)
	vs=np.array(vs)
	Bs=np.concatenate((Bs[xmin:xmax],-Bs[xmin2:xmax2]))

	plt.plot(vs,Bs,'o',markerfacecolor="None",ms=8,mew=2,label='T1')
	popt,yfit=lin_fit(vs,Bs)
	plt.plot(vs,yfit)
	print(popt)
	plt.legend()
	plt.show()

#B=46.34*V+7.978

def Contraste_uW():
	fnames=glob.glob('*.csv')
	taus=[]
	alphas=[]
	vs=[]
	contrast=[]
	xmin=0
	xmax=60
	xmin2=80
	xmax2=-1
	for i in range(len(fnames)):
		if fnames[i][2]=='-' :
			v=-float(fnames[i][3:-7])
		else :
			v=float(fnames[i][2:-7])
		vs+=[v]
		x,y=extract_data(fnames[i],xcol=6,ycol=7)
		cs=find_ESR_peaks(x,y)
		xval=min(cs)
		for i in range(len(x)):
			if x[i]>xval :
				break
		contrast+=[y[i]]

		# x,y=extract_data(fnames[i],xcol=4,ycol=5)
		# # popt,yfit=stretch_arb_exp_fit(x,y)
		# # alphas+=[popt[3]]
		# popt,yfit=stretch_arb_exp_fit(x,y,alpha=0.85,fixed=True)
		# taus+=[popt[2]]

	contrast=[x for _, x in sorted(zip(vs, contrast))]
	contrast=np.array(contrast)
	vs=sorted(vs)
	vs=np.array(vs)
	Bs=46.34318614687412*vs-7.978127707569323
	# Bs=np.concatenate((Bs[xmin:xmax],Bs[xmin2:xmax2]))
	# contrast=np.concatenate((contrast[xmin:xmax],contrast[xmin2:xmax2]))
	Bs=Bs[xmin:xmax]
	contrast=contrast[xmin:xmax]
	freqs=Bs*2.8+2870
	plt.plot(freqs,contrast,'-o',markerfacecolor="None",ms=8,mew=2,label='Contraste uw')
	# popt,yfit=cos_fit(Bs,contrast)
	# plt.plot(Bs,yfit)
	plt.legend()
	plt.show()

Contraste_uW()
#Note : il faudrait sans doute enelver les 2/3 points de chaque cotés de la petite bosse en 0 B, ça correspond à la région ou tu peux pas trop distinguer la 111 des autres classes
def total():
	fnames=glob.glob('*.csv')
	taus=[]
	alphas=[]
	vs=[]
	xmin=0
	xmax=60
	xmin2=80
	xmax2=-1
	for i in range(len(fnames)):
		if fnames[i][2]=='-' :
			v=-float(fnames[i][3:-7])
		else :
			v=float(fnames[i][2:-7])
		vs+=[v]

		x,y=extract_data(fnames[i],xcol=4,ycol=5)
		# # popt,yfit=stretch_arb_exp_fit(x,y)
		# # alphas+=[popt[3]]
		popt,yfit=stretch_arb_exp_fit(x,y,alpha=0.85,fixed=True)
		taus+=[popt[2]]

	taus=[x for _, x in sorted(zip(vs, taus))]
	vs=sorted(vs)
	vs=np.array(vs)
	Bs=46.34318614687412*vs-7.978127707569323


	plt.plot(Bs,taus,'o',markerfacecolor="None",ms=8,mew=2,label='T1')
	popt,yfit=lor_fit(Bs,taus)
	print(popt)
	plt.plot(Bs,yfit,label='width=%3.2f G'%popt[2])
	plt.legend()
	plt.show()
# total()


def single():
	fname='V=0.716194 V'
	x,y=extract_data(fname,xcol=4,ycol=5)
	plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2)
	popt,yfit=stretch_arb_exp_fit(x,y,alpha=0.85,fixed=True)
	plt.plot(x,yfit)
	print(popt[2])
	plt.show()

# single()