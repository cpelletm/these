import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
import matplotlib.animation as animation
from analyse import *


x,y=extract_data('ESR 3V')
plt.plot(x,y,'o-',markerfacecolor='None')
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()

def anim_ESR():
	fnames,fval=extract_glob('ESR',6)
	fnames.remove(fnames[29])
	fval.remove(fval[29])

	fig = plt.figure() # initialise la figure
	line, = plt.plot([], []) 

	x,y=extract_data(fnames[0])
	plt.xlim(min(x), max(x))
	plt.ylim(0,3)
	t=plt.text(x=2900,y=0.5,s='slide %i'%0,fontsize=20,fontweight='bold')

	def animate(i): 
		f=fnames[i]
		x,y=extract_data(f)
		line.set_data(x, y)
		t.set_text('slide %i'%i)
		return line,t
	 
	ani = animation.FuncAnimation(fig, animate, frames=len(fnames), blit=True, interval=50, repeat=True)

	plt.show()


def anim_T1():
	fnames,fval=extract_glob('T1',5,-5)
	fnames.remove(fnames[29])
	fval.remove(fval[29])

	fig = plt.figure() # initialise la figure
	line, = plt.plot([], []) 

	x,y=extract_data(fnames[0])
	y=y/max(y)
	x=x*1000
	plt.xlim(min(x), max(x))
	plt.ylim(0,1)
	t=plt.text(x=2,y=0.5,s='slide %i'%0,fontsize=20,fontweight='bold')

	def animate(i): 
		f=fnames[i]
		x,y=extract_data(f,ycol=5)
		y=y/max(y)
		x=x*1000
		line.set_data(x, y)
		t.set_text('slide %i'%i)
		return line,t
	 
	ani = animation.FuncAnimation(fig, animate, frames=len(fnames), blit=True, interval=50, repeat=True)

	plt.show()


def taus_en_fonction_de_DeltaE():
	fnames,fval=extract_glob('T1',5,-5)
	fnames.remove(fnames[29])
	fval.remove(fval[29])

	taus=[]
	for fname in fnames :
		x,y=extract_data(fname,ycol=5)
		x=x*1000
		y=y/max(y)
		popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.75,fixed=True)
		taus+=[popt[1]]

	taus=np.array(taus)
	# plt.plot(fval,taus)
	# plt.show()

	fnames,fval=extract_glob('ESR',6)
	fnames.remove(fnames[29])
	fval.remove(fval[29])
	DeltaEs=[]
	for fname in fnames :
		x,y=extract_data(fname)
		cs=find_ESR_peaks(x,y,threshold=0.35,precise=True)
		DeltaEs+=[cs[3]-cs[2]]

	plt.plot(DeltaEs,1/taus)
	plt.show()

def plot_3_T1s():
	x,y=extract_data(fnames[0],ycol=5)
	x=x*1000
	y=y/max(y)
	plt.plot(x,y)
	popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.75,fixed=True)
	plt.plot(x,yfit)
	print(popt)

	x,y=extract_data(fnames[-1],ycol=5)
	x=x*1000
	y=y/max(y)
	plt.plot(x,y)
	popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.75,fixed=True)
	plt.plot(x,yfit)
	print(popt)

	x,y=extract_data('T1 1 classe',ycol=5)
	x=x*1000
	y=y/max(y)
	plt.plot(x,y)
	popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.75,fixed=True)
	plt.plot(x,yfit)
	print(popt)
	plt.show()


