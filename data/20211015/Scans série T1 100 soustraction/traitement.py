import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from analyse import *

def total():
	fnames=glob.glob('*.csv')
	taus=[]
	alphas=[]
	vs=[]
	for i in range(len(fnames)):
		if fnames[i][2]=='-' :
			v=-float(fnames[i][3:-7])
		else :
			v=float(fnames[i][2:-7])
		vs+=[v]
		x,y=extract_data(fnames[i],xcol=4,ycol=5)
		# popt,yfit=stretch_arb_exp_fit(x,y)
		# alphas+=[popt[3]]
		popt,yfit=stretch_arb_exp_fit(x,y,alpha=0.85,fixed=True)
		taus+=[popt[2]]

	plt.plot(vs,taus,'o',markerfacecolor="None",ms=8,mew=2,label='T1')
	plt.legend()
	plt.show()

total()

def single():
	fname='V=0.716194 V'
	x,y=extract_data(fname,xcol=4,ycol=5)
	plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2)
	popt,yfit=stretch_arb_exp_fit(x,y,alpha=0.85,fixed=True)
	plt.plot(x,yfit)
	print(popt[2])
	plt.show()

# single()