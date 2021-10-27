import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from analyse import *
from scipy.signal import find_peaks

def Contraste_uW():
	fnames=glob.glob('*.csv')
	vs=[]
	contrast=[[],[],[],[],[],[],[],[]]
	freqs=[[],[],[],[],[],[],[],[]]
	for i in range(len(fnames)):
		if fnames[i][2]=='-' :
			v=-float(fnames[i][3:-7])
		else :
			v=float(fnames[i][2:-7])
		vs+=[v]
		x,y=extract_data(fnames[i])
		cs=find_ESR_peaks(x,y,returnUnit='x')
		popt,yfit=ESR_n_pics(x,y,cs,width=3.5,amp=0.2)
		cs=popt[1]
		amps=popt[3]
		for k in range(8):
			contrast[k]+=[amps[k]]
			freqs[k]+=[cs[k]]
		print(i)
		# x,y=extract_data(fnames[i],xcol=4,ycol=5)
		# # popt,yfit=stretch_arb_exp_fit(x,y)
		# # alphas+=[popt[3]]
		# popt,yfit=stretch_arb_exp_fit(x,y,alpha=0.85,fixed=True)
		# taus+=[popt[2]]

	contrast=[x for _, x in sorted(zip(vs, contrast))]
	contrast=np.array(contrast)
	freqs=[x for _, x in sorted(zip(vs, freqs))]
	freqs=np.array(freqs)
	vs=sorted(vs)
	vs=np.array(vs)

	for k in range(8) :
		plt.plot(freqs[k],contrast[k],'-o',markerfacecolor="None",ms=8,mew=2,label='Contraste uw')
	# popt,yfit=cos_fit(Bs,contrast)
	# plt.plot(Bs,yfit)
	# plt.legend()
	plt.show()

Contraste_uW()


def test():
	fnames=glob.glob('*.csv')
	fname=fnames[21]
	x,y=extract_data(fname)
	plt.plot(x,y)
	cs=find_ESR_peaks(x,y)
	print(cs)
	popt,yfit=ESR_n_pics(x,y,cs,width=3.5,amp=0.2)
	plt.plot(x,yfit)
	print(popt)
	cs=popt[1]
	amps=popt[3]
	plt.show()

# test()