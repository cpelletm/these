import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
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

Mesures T1 :
C13 0B : baseline (T1=0)
1x : T1=0.00609014
2x2 : T1=0.00031344 ; 0.00030245 ; 0.0002971 ; 0.0003125
1x2x1 : T1= 0.00020091 ; 0.00022116 ; 
Bon j'arrête en cours de route parce que ca fitte pas si bien (cf T1 121 nuit)


T1 avec un alpha=0.82 fixe :
1x : 0.00086313

"""

# x,y=extract_data('ESR champ transverse très faible')
# plt.plot(x,y,'o-',markerfacecolor='None')
# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)
# plt.show()



#Baseline : T1=1.21753193e-03 ; alpha=8.29849679e-01 
# fname='T1 0B court'
# x,y=extract_data(fname,ycol=5)
# plt.plot(x,y)
# # popt,yfit=stretch_with_baseline(x,y,tau_BL=1.21753193e-03,alpha_BL=8.29849679e-01)
# popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.8,fixed=True)
# plt.plot(x,yfit)
# print(popt)
# plt.show()

def random_plot():
	plt.figure(num=1,figsize=(4,3),dpi=80) #à écrire au début a priori
	ax=plt.gca()
	ax.tick_params(labelsize=13)
	fname='ESR 2x2'
	x,y=extract_data(fname)
	y=y/max(y)
	plt.plot(x,y)
	plt.show()


random_plot()
def plot_champs_transverses():
	fname='T1 champ transverse très faible classe 4 (DQ)'
	x,y=extract_data(fname,ycol=5)
	x=x*1000
	y=y/max(y)
	plt.plot(x,y,'-o',label='weak transverse field',markerfacecolor="None")
	# fname='T1 moyen B transverse'
	# x,y=extract_data(fname,ycol=5)
	# y=y/max(y)
	# plt.plot(x,y,label='moyen champ transverse',marker='o',markerfacecolor="None",ms=8,mew=2)
	fname='T1 transverse gros champ'
	x,y=extract_data(fname,ycol=5)
	x=x*1000
	y=y/max(y)
	plt.plot(x,y,'-o',label='strong transverse field',markerfacecolor="None")
	fname='T1 1 classe pour le champ transverse moyen'
	x,y=extract_data(fname,ycol=5)
	x=x*1000
	y=y/max(y)
	plt.plot(x,y,'-o',label='non-transverse field',markerfacecolor="None")
	# fname='T1 1x3'
	# x,y=extract_data(fname,ycol=5)
	# y=y/max(y)
	# plt.plot(x,y,label='Baseline 2',marker='o',markerfacecolor="None",ms=8,mew=2)
	plt.xticks(fontsize=15)
	plt.yticks(fontsize=15)
	plt.legend()
	plt.show()

def fig121_Vs_22():
	plt.figure(num=1,figsize=(9,6),dpi=80) #à écrire au début a priori


	ax=plt.gca()
	ax.tick_params(labelsize=20)
	ax.set_xlabel(r'Dark time (s)',fontsize=20,fontweight='bold')
	ax.set_ylabel(r'Relative Contrast' ,fontsize=20,fontweight='bold')


	fname='T1 2x2 gauche (2)'
	x,y=extract_data(fname,ycol=5)
	y=y/max(y)
	plt.plot(x,y,'o',markerfacecolor="None",color='tab:blue',ms=8,mew=2)
	fname='T1 2x2 droite (2)'
	x,y=extract_data(fname,ycol=5)
	y=y/max(y)
	plt.plot(x,y,'s',markerfacecolor="None",color='tab:blue',ms=8,mew=2)
	fname='T1 2x2'
	x,y=extract_data(fname,ycol=5)
	y=y/max(y)
	plt.plot(x,y,'^',markerfacecolor="None",color='tab:blue',ms=8,mew=2)
	fname='T1 2x2 autre raie'
	x,y=extract_data(fname,ycol=5)
	y=y/max(y)
	plt.plot(x,y,'*',markerfacecolor="None",color='tab:blue',ms=8,mew=2)


	fname='T1 121 nuit'
	x,y=extract_data(fname,ycol=5)
	y=y/max(y)
	plt.plot(x,y,'o',color='tab:orange',ms=8,mew=2)
	fname='T1 1x2x1'
	x,y=extract_data(fname,ycol=5)
	y=y/max(y)
	plt.plot(x,y,'s',color='tab:orange',ms=8,mew=2)
	fname='T1 121 (3)'
	x,y=extract_data(fname,ycol=5)
	y=y/max(y)
	plt.plot(x,y,'^',color='tab:orange',ms=8,mew=2)
	fname='T1 121 (4)'
	x,y=extract_data(fname,ycol=5)
	y=y/max(y)
	plt.plot(x,y,'*',color='tab:orange',ms=8,mew=2)
	plt.show()


def test_fits_t1_phonon():
	#Bon après pas mal de test, c'est bien de la merde les fits avec stretch et phonon, le T1 stretch il danse vraiment la salsa et les valeurs c'est assez nimp
	#C'est peut etre a cause du coté micro, il faudrait vraiment que je fasse plus de test sur les gros adamas pour en être sur. Et limite broyer des diamants aussi

	#En attendant si tu veux des valeurs, mieux vaut prendre des stretch arb. alpha=0.8 fonctionne bien
	T1ph=1/1800

	fname='T1 1 classe pour le champ transverse moyen'

	# fname='T1 2x2 autre raie'
	# fname='T1 2x2'
	# fname='T1 2x2 droite (2)'
	# fname='T1 2x2 gauche (2)'
	# fname='T1 121 nuit'
	# fname='T1 121 (3)'
	# fname='T1 121 (4)'
	# fname='T1 1x2x1'
	# fname='T1 0B court'
	x,y=extract_data(fname,ycol=5)
	plt.plot(x,y)
	# popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph,fixed=False)
	popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.8,fixed=True)
	plt.plot(x,yfit)
	print(1/popt[1])#,popt[2])
	plt.show()