import numpy as np
import matplotlib.pyplot as plt
from numpy import cos,sin,pi
import scipy.optimize

def map_full() :
	ax=plt.gca()

	#Theta en ordonée de 0 a 180 ; phi en abscisse de 0 à 360
	lw1=3
	ls1='-'
	#(100)
	color = next(ax._get_lines.prop_cycler)['color']
	plt.plot([90,90],[0,180],linewidth=lw1,ls=ls1,label=r'Plane $\bot (100)$ ',color=color)
	plt.plot([270,270],[0,180],linewidth=lw1,ls=ls1,color=color)

	#(010)
	color = next(ax._get_lines.prop_cycler)['color']
	plt.plot([180,180],[0,180],linewidth=lw1,ls=ls1,label=r'Plane $\bot (010)$ ',color=color)
	plt.plot([0,0],[0,180],linewidth=lw1/2,ls=ls1,color=color)
	plt.plot([360,360],[0,180],linewidth=lw1/2,ls=ls1,color=color)

	#(001)
	color = next(ax._get_lines.prop_cycler)['color']
	plt.plot([0,360],[90,90],linewidth=lw1,ls=ls1,label=r'Plane $\bot (001)$ ',color=color)

	lw2=2
	ls2='--'


	#(110)
	color = next(ax._get_lines.prop_cycler)['color']
	plt.plot([135,135],[0,180],linewidth=lw2,ls=ls2,label=r'Plane $\bot (110)$ ',color=color)
	plt.plot([315,315],[0,180],linewidth=lw2,ls=ls2,color=color)

	#(1-10)
	color = next(ax._get_lines.prop_cycler)['color']
	plt.plot([45,45],[0,180],linewidth=lw2,ls=ls2,label=r'Plane $\bot (1\bar{1}0)$ ',color=color)
	plt.plot([225,225],[0,180],linewidth=lw2,ls=ls2,color=color)


	phis=np.linspace(0,360,500)
	#(101)
	color = next(ax._get_lines.prop_cycler)['color']
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*cos(phi*pi/180)+cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	plt.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (101)$ ',color=color)

	#(10-1)
	color = next(ax._get_lines.prop_cycler)['color']
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*cos(phi*pi/180)-cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	plt.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (10\bar{1})$ ',color=color)

	#(011)
	color = next(ax._get_lines.prop_cycler)['color']
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*sin(phi*pi/180)+cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	plt.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (011)$ ',color=color)

	#(01-1)
	color = next(ax._get_lines.prop_cycler)['color']
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*sin(phi*pi/180)-cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	plt.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (01\bar{1})$ ',color=color)


	# plt.plot(phis,90+45*cos(pi/180*phis)) #Pour les mauvaises langues qui disent que ça sert à rien

	#Particular directions
	plt.scatter([0,180,360],[90,90,90],s=80,facecolors='red',edgecolors='red',label=r'$(100)$ direction',zorder=10)
	theta_111=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*np.sqrt(2)/2-cos(theta*pi/180),bracket=[0,180]).root
	plt.scatter([45,225],[theta_111,180-theta_111],s=80,facecolors='g',edgecolors='g',label=r'$(111)$ direction',zorder=10)




	plt.xlabel(r'$\phi$(°)')
	plt.ylabel(r'$\theta$(°)')


	plt.legend()
	plt.show()

def map_zoom():
	fig,ax=plt.subplots()

	#Theta en ordonée de 0 a 180 ; phi en abscisse de 0 à 360
	lw1=3
	ls1='-'

	color = next(ax._get_lines.prop_cycler)['color']
	#(010)
	color = next(ax._get_lines.prop_cycler)['color']
	ax.plot([180,180],[0,180],linewidth=lw1,ls=ls1,label=r'Plane $\bot (010)$ ',color=color)
	ax.plot([0,0],[0,180],linewidth=lw1/2,ls=ls1,color=color)
	ax.plot([360,360],[0,180],linewidth=lw1/2,ls=ls1,color=color)

	#(001)
	color = next(ax._get_lines.prop_cycler)['color']
	ax.plot([0,360],[90,90],linewidth=lw1,ls=ls1,label=r'Plane $\bot (001)$ ',color=color)

	lw2=2
	ls2='--'


	color = next(ax._get_lines.prop_cycler)['color']
	color = next(ax._get_lines.prop_cycler)['color']
	color = next(ax._get_lines.prop_cycler)['color']
	color = next(ax._get_lines.prop_cycler)['color']
	phis=np.linspace(0,360,500)

	#(011)
	color = next(ax._get_lines.prop_cycler)['color']
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*sin(phi*pi/180)+cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	ax.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (011)$ ',color=color)

	#(01-1)
	color = next(ax._get_lines.prop_cycler)['color']
	thetas=[]
	for phi in phis :
		theta=scipy.optimize.root_scalar(lambda theta:sin(theta*pi/180)*sin(phi*pi/180)-cos(theta*pi/180),bracket=[0,180]).root
		thetas+=[theta]
	ax.plot(phis,thetas,linewidth=lw2,ls=ls2,label=r'Plane $\bot (01\bar{1})$ ',color=color)


	# ax.plot(phis,90+45*cos(pi/180*phis)) #Pour les mauvaises langues qui disent que ça sert à rien

	#Particular directions
	plt.scatter([0],[0],s=80,facecolors='red',edgecolors='red',label=r'$(100)$ direction',zorder=10)



	for line in ax.get_lines() :
		line.set_data(line.get_xdata()-180,line.get_ydata()-90)

	plt.xlabel(r'$\phi$(°)')
	plt.ylabel(r'$\theta$(°)')
	plt.xlim([-9,9])
	plt.ylim([-6,6])


	plt.legend()
	plt.show()

map_zoom()