import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from analyse import *



def total():
	fnames=glob.glob('*.csv')
	phis=[]
	deltaDQ=[]
	deltaVHm=[]
	deltaVHp=[]
	deltaBtransverse=[]
	for fname in fnames :
		phis+=[float(fname[:-4])]
		x,y=extract_data(fname)
		deltaDQ+=[y[260]-y[265]]
		deltaVHm+=[y[205]-y[209]]
		deltaVHp+=[y[317]-y[322]]
		deltaBtransverse+=[y[155]-y[372]]

	deltaDQ=[x for _, x in sorted(zip(phis, deltaDQ))]
	deltaVHm=[x for _, x in sorted(zip(phis, deltaVHm))]
	deltaVHp=[x for _, x in sorted(zip(phis, deltaVHp))]
	deltaBtransverse=[x for _, x in sorted(zip(phis, deltaBtransverse))]
	phis=sorted(phis)
	phis=np.array(phis)
	deltaDQ=np.array(deltaDQ)
	deltaVHm=np.array(deltaVHm)
	deltaVHp=np.array(deltaVHp)
	deltaBtransverse=np.array(deltaBtransverse)
	x=phis
	y=deltaBtransverse
	plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=2)
	popt,yfit=cos_fit(x,y)
	print(popt[1]*180/np.pi,popt[2]*180/np.pi)
	plt.plot(x,yfit,label=r'$\phi$=%3.2f'%(popt[2]*180/np.pi))
	# plt.plot(phis,deltaVHm/max(deltaVHm))
	plt.legend()
	plt.show()


total()

#260:266 ; 205:210 ; 317:322 ; 155:372
def single():
	fname='90'
	x,y=extract_data(fname)
	plt.plot(y,'o',markerfacecolor="None",ms=8,mew=2)
	plt.show()

# single()