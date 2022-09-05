import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


plt.figure(num=1,figsize=(3,2),dpi=80)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.locator_params(axis='x', nbins=5)



def plot_ESR_1x1x1x1():
	fnames,fval=extract_glob('T1 1x1x1x1/ESR')
	# x,y=extract_data('T1 1x1x1x1/ESR 3V')
	x,y=extract_data(fnames[-1])
	n=len(x)#//2
	x=x[:n]
	y=y[:n]
	y=y/max(y)
	plt.plot(x,y)

# plot_ESR_1x1x1x1()

def plot_spread_1x1x1x1():
	fnames,fval=extract_glob('T1 1x1x1x1/ESR')
	n=len(fnames)
	# x,y=extract_data(fnames[-1])
	# peaks=find_ESR_peaks(x,y,precise=True)
	# B=find_B_cartesian_mesh(peaks)
	# print(peaks,B,B.transitions4Classes())
	B_3_V=[78.55,31.80,16.86]
	Bamp_3_V=norm(B_3_V)
	Bamps=np.linspace(0,Bamp_3_V,n//2)
	Bxs=np.linspace(0,B_3_V[0],n//2)
	Bys=np.linspace(0,B_3_V[1],n//2)
	Bzs=np.linspace(0,B_3_V[2],n//2)
	transis=np.zeros((n//2,8))
	for i in range(n//2):
		B=magneticField(x=Bxs[i],y=Bys[i],z=Bzs[i])
		transis[i,:]=B.transitions4Classes()

	# for i in range(8):
	# 	plt.plot(Bamps,transis[:,i])

	for i in range(3):
		plt.plot(Bamps,transis[:,i+1]-transis[:,i])

	for i in range(4,7):
		plt.plot(Bamps,transis[:,i+1]-transis[:,i])

	plt.plot(Bamps,[8.04]*len(Bamps),'--')

# plot_spread_1x1x1x1()

def plot_ESR_100():
	x,y=extract_data('T1 100 align 3/ESR/V=-2.000000')
	y=y/max(y)
	plt.plot(x,y)

# plot_ESR_100()

def plot_ESR_0B(i=108):
	fnames,fval=extract_glob('T1 100 align 3/ESR')
	x,y=extract_data(fnames[i]) #'T1 100 align 3/ESR/V=0.311558'
	y=y/max(y)
	plt.plot(x,y)
	

# plot_ESR_0B(i=108)


def plot_T1__fit_main_text():
	fnames,fval=extract_glob('T1 1x1x1x1/T1')
	i=104
	x,y=extract_data(fnames[i],ycol=5)
	y=y/max(y)
	x=x*1e3
	# T1ph=0.003626*1e3
	T1ph=6
	plt.plot(x,y,'o',markerfacecolor='None',mew=1,ms=5,color=color(0),label=r'$B=0$')
	# popt,yfit=stretch_exp_fit_zero(x,y,norm=False)
	# popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph,fixed=True)
	popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.5)
	print(popt)
	plt.plot(x,yfit,lw=2,color=color(1))

	x,y=extract_data(fnames[15],ycol=5)
	x=x*1e3
	for i in range(16,45):
		x2,y2=extract_data(fnames[i],ycol=5)
		y+=y2
	y=y/max(y)
	plt.plot(x,y,'x',markerfacecolor='None',mew=1,ms=5,color=color(2),label=r'$B\neq 0$')
	# popt,yfit=stretch_exp_fit_zero(x,y,norm=False)
	# popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph,fixed=True)
	popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.9)
	print(popt)
	plt.plot(x,yfit,lw=2,color=color(1))
	plt.legend()

# plot_T1__fit_main_text()

#~~~~RQ : normaliser les fits des T1 n'a pas de sens tant que je ne connais pas la vraie valeur en t=0
#En plus y'a des p-e des blagues de tdv de l'état metastable pour les temps très courts, à voir si ça se soutrait correctement
#Y'a aussi le fait que je suis obligé d'attendre plus longtemps que le pulse uW, sinon ça fausse le truc (genre tu peux avoir du spin lockin ou chais pas)

def plot_T1_fit(i=104):
	fnames,fval=extract_glob('T1 1x1x1x1/T1')
	x,y=extract_data(fnames[i],ycol=5)
	# x=x-x[0]
	y=y/max(y)
	x=x*1e3
	
	# popt,yfit=exp_fit_zero(x,y)
	# plt.plot(x,yfit)
	# popt,yfit=stretch_exp_fit_zero(x,y)
	# plt.plot(x,yfit)
	T1ph=0.003626*1e3
	plt.plot(x,y,'x',markerfacecolor='None',mew=1.2,ms=5,color=color(0),label='Experimental data')
	popt,yfit=stretch_exp_fit_zero(x,y,norm=False)
	plt.plot(x,yfit,'--',lw=2,color=color(1),label=r'$\exp (-\sqrt{\frac{\tau}{T_1^{\rm dd}}})$')
	# popt,yfit=exp_fit_zero(x,y,norm=False)
	# plt.plot(x,yfit,'--',lw=2,color=color(1),label=r'$\exp (-\frac{\tau}{T_1^{\rm ph}} )$')
	# popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	# plt.plot(x,yfit,lw=2,color=color(1),label=r'$\exp (-\frac{\tau}{T_1^{\rm ph}} -\sqrt{\frac{\tau}{T_1^{\rm dd}}})$')
	plt.legend(fontsize=13)

# plot_T1_fit(i=104)

def plot_T1_fit_0B():
	fname='T1 0B'
	x,y=extract_data(fname,ycol=5)
	y=y/max(y)
	x=x*1e3
	plt.plot(x,y,'x',markerfacecolor='None',mew=1.2,ms=5,color=color(0),label='Experimental data')
	popt,yfit=stretch_exp_fit_zero(x,y,norm=False)
	plt.plot(x,yfit,'--',lw=2,color=color(1),label=r'$\exp (-\sqrt{\frac{\tau}{T_1^{\rm dd}}})$')
	popt,yfit=exp_fit_zero(x,y,norm=False)
	plt.plot(x,yfit,'--',lw=2,color=color(2),label=r'$\exp (-\frac{\tau}{T_1^{\rm ph}} )$')
	plt.legend(fontsize=13)

# plot_T1_fit_0B()



def plot_T1_fit_avg():
	fnames,fval=extract_glob('T1 1x1x1x1/T1')
	x,y=extract_data(fnames[15],ycol=5)
	x=x*1e3
	for i in range(16,45):
		x2,y2=extract_data(fnames[i],ycol=5)
		y+=y2
	y=y/max(y)
	T1ph=0.003626*1e3
	plt.plot(x,y,'x',markerfacecolor='None',mew=1.2,ms=8,color=color(0),label='Experimental data')
	popt,yfit=stretch_exp_fit_zero(x,y,norm=False)
	plt.plot(x,yfit,'--',lw=2,color=color(1),label=r'$\exp (-\sqrt{\frac{\tau}{T_1^{\rm dd}}})$')
	popt,yfit=exp_fit_zero(x,y,norm=False)
	plt.plot(x,yfit,'-.',lw=2,color=color(2),label=r'$\exp (-\frac{\tau}{T_1^{\rm ph}} )$')
	# popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	# plt.plot(x,yfit,lw=2,color=color(1),label=r'$\exp (-\frac{\tau}{T_1^{\rm ph}} -\sqrt{\frac{\tau}{T_1^{\rm dd}}})$')
	plt.legend(fontsize=13)

# plot_T1_fit_avg()

def alphas_T1():
	# fnames,fval=extract_glob('T1 100 align 3/T1')
	# fval.remove(fval[194])
	# fnames.remove(fnames[194])
	# fval.remove(fval[178])
	# fnames.remove(fnames[178])
	fnames,fval=extract_glob('T1 1x1x1x1/T1')
	n=len(fnames)
	# errors=[]
	# for i in range(n):
	# 	x,y=extract_data(fnames[i],ycol=5)
	# 	y=y/max(y)
	# 	T1ph=0.003626*1e3
	# 	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	# 	errors+=[1/estim_error(y,yfit,rel=False)]
	# plt.plot(errors)
	# taus=[]
	# for i in range(n):
	# 	x,y=extract_data(fnames[i],ycol=5)
	# 	y=y/max(y)
	# 	T1ph=0.003626*1e3
	# 	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	# 	taus+=[1/popt[1]]
	# plt.plot(taus)
	alphas=[]
	taus=[]
	for i in range(n):
		x,y=extract_data(fnames[i],ycol=5)
		y=y/max(y)
		popt,yfit=stretch_arb_exp_fit_zero(x,y)
		alphas+=[popt[2]]
		T1ph=0.003626*1e3
		popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
		taus+=[popt[1]]
	taus=np.array(taus)
	taus=taus/max(taus)
	Bs=[np.array([78.55,31.8,16.86])*(x-0.17)/2.8 for x in fval]
	Bamps=np.array([norm(B)*np.sign(B[0]) for B in Bs])
	plt.plot(Bamps,alphas,'o',markerfacecolor='None')
	# plt.plot(taus)


# alphas_T1()



def plot_PL_1x1x1x1():
	x,y=extract_data('T1 1x1x1x1/scan 1x1x1x1',ycol=3)
	# x,y=extract_data('scan align random',ycol=3)


	B=(x+0.17)*86.4/3
	i0=find_elem(-0.17,x)
	i2=find_elem(2,x)



	# y=y[i2:i0]
	# B=B[i2:i0]
	y=y/max(y)

	plt.plot(B,y)


# plot_PL_1x1x1x1()

def plot_T1_1x1x1() :

	fnames,fval=extract_glob('T1 1x1x1x1/T1')
	n=len(fval)
	taus=np.zeros(n)

	Bs=[np.array([78.55,31.8,16.86])*(x-0.17)/2.8 for x in fval]

	Bamps=np.array([norm(B)*np.sign(B[0]) for B in Bs])

	for i in range(n):
		fname=fnames[i]
		x,y=extract_data(fname,ycol=5)
		# T1ph=0.003626
		T1ph=5e-3
		popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
		taus[i]=popt[1]

	nmin=106
	nmax=173
	x=Bamps[nmin:nmax]

	y=1/taus[nmin:nmax]



	plt.plot(x,y)
	# popt,yfit=lor_fit(x,y,x0=0.00001,amp=1600,ss=50,sigma=6) #Ok je fais full merde
	# print(popt)
	# plt.plot(x,yfit)


plot_T1_1x1x1()

def plot_T1_100() :
	fnames,fval=extract_glob('T1 100 align 3/T1')
	fval.remove(fval[194])
	fnames.remove(fnames[194])
	fval.remove(fval[178])
	fnames.remove(fnames[178])
	n=len(fval)
	taus=np.zeros(n)
	Bs=(np.array(fval)-0.16)*29


	nmax=107
	for i in range(n):
		fname=fnames[i]
		x,y=extract_data(fname,ycol=5)
		# T1ph=0.003626
		T1ph=0.005
		popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
		taus[i]=popt[1]

	x=-Bs[:nmax]
	y=1/taus[:nmax]
	# y=y-y[-1]
	# y=y/max(y)
	plt.plot(x,y)

	# popt,yfit=lor_fit(x,y,x0=0.00001)
	# print(popt)
	# plt.plot(x,yfit)

# plot_T1_100()

def plot_PL_100():
	x,y=extract_data('T1 100 align 3/scan EM',ycol=3)
	B=(x+0.16)*29
	i0=find_elem(-0.12,x)
	i2=find_elem(2,x)



	y=y[i2:i0]
	x=B[i2:i0]
	y=y/max(y)

	plt.plot(x,y)

# plot_PL_100()


plt.show()

