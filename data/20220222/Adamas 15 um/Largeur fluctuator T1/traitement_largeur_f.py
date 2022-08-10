import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
import matplotlib.animation as animation
from analyse import *

"""
Calculs Eta :
eta0=0.3849/4
eta=(0.3849/4+2*0.6507/4+0.8328/4)/30

eta c13 0B : 0.05 eta0
eta base +/- 1 classe : 3-4 eta0
eta 121 : 10 eta0
eta 22 : 7.2 eta0
eta 31 : 28.4 eta0
eta 40 : 42.8 eta0
eta 0B sans DQ : 51-55 eta0


"""
def full_animation():

	fig,axes=plt.subplots(2)
	fig.set_size_inches([10,8])
	[ax1,ax2]=axes
	ax1.set_ylim([0,3])
	ax2.set_ylim([-0.2,1.2])
	ax1.set_xlabel('Frequency (MHz)',fontweight='bold')
	ax1.set_ylabel('ODMR contrast',fontweight='bold')
	ax2.set_xlabel('Dark time (ms)',fontweight='bold')
	ax2.set_ylabel('T1 contrast',fontweight='bold')

	nFrameMin=20
	nFrameMax=80


	fnames,fval=extract_glob('Série ESR 2',16)
	fnames.remove(fnames[43])
	fval.remove(fval[43])
	fnames=fnames[nFrameMin:nFrameMax]


	x,y=extract_data(fnames[0])
	l1=ax1.plot(x,y)[0]

	xESR=x
	yESRs=[]
	for i in range(len(fnames)):
		x,y=extract_data(fnames[i])
		yESRs+=[y]

	fnames,fval=extract_glob('Série T1 2',15)
	fnames.remove(fnames[43])
	fval.remove(fval[43])
	fnames=fnames[nFrameMin:nFrameMax]


	x,y=extract_data(fnames[0],ycol=5)
	nT1max=100
	x=x[:nT1max]*1e3
	y=y[:nT1max]/max(y[:nT1max])
	l2=ax2.plot(x,y,'o',markerfacecolor='None')[0]
	popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.8,fixed=True)
	l3=ax2.plot(x,yfit,lw=2,label='tau=%.3f'%(popt[1]))[0]
	xT1=x
	yT1s=[]
	yfits=[]
	taus=[]
	for i in range(len(fnames)):
		x,y=extract_data(fnames[i],ycol=5)
		y=y[:nT1max]/max(y[:nT1max])
		yT1s+=[y]
		popt,yfit=stretch_arb_exp_fit_zero(xT1,y,alpha=0.8,fixed=True)
		yfits+=[yfit]
		taus+=[popt[1]]

	def animate(i): 
		l1.set_data(xESR, yESRs[i])
		l2.set_data(xT1, yT1s[i])
		l3.set_data(xT1, yfits[i])
		return l1,l2,l3
	 
	ani = animation.FuncAnimation(fig, animate, frames=len(fnames), blit=True, interval=100, repeat=True)
	ani.save('Anim.html')


	# plt.legend()
	plt.show()

# full_animation()

def plot_esr_centre(ax):
	fnames,fval=extract_glob('Série ESR 2',16)

	fnames.remove(fnames[43])
	fval.remove(fval[43])
	x,y=extract_data(fnames[0])
	nmax=500
	x=x[:nmax]
	y=y[:nmax]
	popt,yfit=lor_fit(x,y)
	print(popt)
	c=popt[1]
	x=x-c
	y=y/max(y)
	ax.plot(x,y,'--',lw=1,label='ESR FWHM=%4.3f MHz'%(2*popt[2]))



f1=[2692.8082987830603, 2692.663919492887, 2692.5363084577684, 2692.4253545753463, 2692.330945941972, 2692.2529698527087, 2692.1913128013293, 2692.145860480318, 2692.11649778087, 2692.10310879289, 2692.105576804994, 2692.12378430451, 2692.157612977475, 2692.206943708636, 2692.271656581454, 2692.351630878097, 2692.4467450794455, 2692.556876865091, 2692.6819031133346, 2692.8216999011893, 2692.9761425043775, 2693.1451053973333, 2693.328462253201, 2693.526085943836, 2693.737848539804, 2693.9636213103813, 2694.203274723555, 2694.4566784460235, 2694.723701343195, 2695.004211479189, 2695.298076116835, 2695.6051617176745, 2695.9253339419583, 2696.2584576486483, 2696.6043968954177, 2696.96301493865, 2697.3341742334383, 2697.7177364335885, 2698.113562391616, 2698.5215121587466, 2698.941444984918, 2699.373219318776, 2699.816692807681, 2700.738163833615, 2701.215872658915, 2701.7047032158007, 2702.204509145184, 2702.715143286688, 2703.2364576786454, 2703.7683035581, 2704.310531360806, 2704.8629907212294, 2705.4255304725457, 2705.9979986466415, 2706.580242474114, 2707.1721083842713, 2707.773442005132, 2708.384088163425, 2709.0038908845913, 2709.632693392781, 2710.2703381108563, 2710.9166666603883, 2711.57151986166, 2712.2347377336655, 2712.9061594941086, 2713.5856235594047, 2714.2729675446785, 2714.968028263767, 2715.670641729217, 2716.380643152286, 2717.097866942943, 2717.822146709866, 2718.5533152604453, 2719.291204600782, 2720.035645935686, 2720.7864696686797, 2721.543505401996, 2722.3065819365775, 2723.0755272720785, 2723.850168606863, 2724.6303323380075, 2725.415844061297, 2726.206528571228, 2727.0022098610084, 2727.8027111225565, 2728.6078547465004, 2729.4174623221797, 2730.231354637645, 2731.0493516796564, 2731.871272633686, 2732.696935883916, 2733.526159013239, 2734.3587588032588, 2735.1945512342895, 2736.033351485356, 2736.8749739341947, 2737.719232157251, 2738.5659389296825, 2739.4149062253573, 2740.2659452168527]
f2=[2735.9811549719916, 2735.084678252642, 2734.1924909827676, 2733.30488702252, 2732.42215560626, 2731.544581342557, 2730.672444214191, 2729.80601957815, 2728.945578165631, 2728.0913860820415, 2727.2437048069964, 2726.4027911943213, 2725.56889747205, 2724.742271242426, 2723.923155481901, 2723.111788541138, 2722.308404145007, 2721.5132313925874, 2720.7264947571693, 2719.9484140862505, 2719.1792046015385, 2718.4190768989497, 2717.6682369486102, 2716.9268860948546, 2716.1952210562276, 2715.473433925482, 2714.76171216958, 2714.0602386296937, 2713.3691915212034, 2712.6887444337, 2712.0190663309813, 2711.360321551056, 2710.712669806142, 2710.0762661826657, 2709.4512611412624, 2708.8378005167774, 2708.236025518265, 2707.6460727289873, 2707.0680741064184, 2706.5021569822384, 2705.948444062339, 2705.40705342682, 2704.87809852999, 2703.85792664068, 2703.366913427864, 2702.888743513065, 2702.423507221638, 2701.9712902531473, 2701.532173681366, 2701.106233954277, 2700.6935428940706, 2700.294167697148, 2699.90817093412, 2699.535610549805, 2699.176539863231, 2698.8310075676354, 2698.499057730465, 2698.1807297933756, 2697.876058572232, 2697.5850742571083, 2697.3078024122874, 2697.0442639762614, 2696.7944752617327, 2696.558447955612, 2696.336189119018, 2696.1277011872808, 2695.9329819699383, 2695.752024650738, 2695.584817787636, 2695.4313453127984, 2695.2915865326, 2695.165516127625, 2695.0531041526656, 2694.9543160367257, 2694.8691125830155, 2694.7974499689562, 2694.739279746178, 2694.694548840519, 2694.6631995520283, 2694.6451695549626, 2694.640391897789, 2694.648795003183, 2694.670302668029, 2694.704834063421, 2694.7523037346627, 2694.8126216012665, 2694.8856929569533, 2694.971418469654, 2695.0696941815086, 2695.180411508866, 2695.3034572422844, 2695.438713546531, 2695.5860579605824, 2695.745363397624, 2695.916498145051, 2696.099325864467, 2696.2937055916855, 2696.4994917367285, 2696.716534083828, 2696.944677791424]
f1=np.array(f1)
f2=np.array(f2)
df=f1-f2

def conversion_position_frequency():
	f1=[]
	f2=[]
	inf=35
	sup=60
	absc=fval[:inf]+fval[sup:]
	for i in range(inf):
		f=fnames[i]
		x,y=extract_data(f)
		[x1,x2]=find_ESR_peaks(x,y,width=False,threshold=0.5,returnUnit='x',precise=True)
		f1+=[x1]
		f2+=[x2]

	for i in range(sup,len(fnames)):
		f=fnames[i]
		x,y=extract_data(f)
		[x1,x2]=find_ESR_peaks(x,y,width=False,threshold=0.5,returnUnit='x',precise=True)
		f1+=[x2]
		f2+=[x1]

	plt.plot(absc,f1,'o',markerfacecolor="None",label='Class 1 exp')
	plt.plot(absc,f2,'o',markerfacecolor="None",label='Class 2 exp')

	popt,yfit=fit_ordre_4(absc,f1)
	[a,b,c,d,e]=popt
	x=np.array(fval)
	yfit=a*x**4+b*x**3+c*x**2+d*x+e
	print(list(yfit))
	plt.plot(x,yfit,label='Class 1 fit')

	popt,yfit=fit_ordre_4(absc,f2)
	[a,b,c,d,e]=popt
	x=np.array(fval)
	yfit=a*x**4+b*x**3+c*x**2+d*x+e
	print(list(yfit))
	plt.plot(x,yfit,label='Class 2 fit')
	plt.legend()
	plt.xlabel('Magnet position (mm)')
	plt.ylabel('Classes frequencies (MHz)')
	plt.show()


def anim_ESR():
	fig = plt.figure() # initialise la figure
	line, = plt.plot([], []) 
	plt.xlim(min(x), max(x))
	plt.ylim(0,3)

	def animate(i): 
		f=fnames[i]
		x,y=extract_data(f)
		line.set_data(x, y)
		return line,
	 
	ani = animation.FuncAnimation(fig, animate, frames=len(fnames), blit=True, interval=50, repeat=False)

	plt.show()

fnames,fval=extract_glob('Série T1 2',15)

fnames.remove(fnames[43])
fval.remove(fval[43])

def anim_T1():
	x,y=extract_data(fnames[0],ycol=5)
	fig = plt.figure() # initialise la figure
	line, = plt.plot([], []) 
	plt.xlim(min(x), max(x))
	plt.ylim(-0.3,1)

	def animate(i): 
		f=fnames[i]
		x,y=extract_data(f,ycol=5)
		y=y/max(y)
		line.set_data(x, y)
		return line,
	 
	ani = animation.FuncAnimation(fig, animate, frames=len(fnames), blit=True, interval=50, repeat=False)

	plt.show()


def plot_T1(ax):
	taus=[]
	for i in range(len(fnames)):
		x,y=extract_data(fnames[i],ycol=5)
		# popt,yfit=stretch_et_phonons(x,y,T1ph=0.003,fixed=True)
		popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.8,fixed=True)
		taus+=[popt[1]]

	x,y=np.array(df),np.array(taus)
	y=1/y
	# y=y-min(y)
	# y=y/max(y)
	color = next(ax._get_lines.prop_cycler)['color']
	ax.plot(x,y,'o',markerfacecolor='None',ms=8,mew=2,label='1/T1',color=color)

	popt,yfit=lor_fit(x,y)
	print(popt)
	color = next(ax._get_lines.prop_cycler)['color']
	ax.plot(x,yfit,lw=2,label='1/T1 fit FWHM=%4.3f MHz'%(2*popt[2]),color=color)


def plot_largeur_fluct_et_ESR():
	fig, ax1 = plt.subplots()
	plot_esr_centre(ax=ax1)
	ax1.tick_params(labelsize=20)
	ax1.set_xlabel(r'$\Delta \nu$ (MHz)',fontsize=20)
	ax1.set_ylabel(r'ODMR relative contrast' ,fontsize=20)


	ax2 = ax1.twinx()
	plot_T1(ax2)
	ax2.tick_params(labelsize=20)
	ax2.set_ylabel(r'1/$T_1$ (s$^{-1}$)' ,fontsize=20)


	ax1.legend(loc='center left')
	ax2.legend(loc='center right')
	plt.show()

plot_largeur_fluct_et_ESR()