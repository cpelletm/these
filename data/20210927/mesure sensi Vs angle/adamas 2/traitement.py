import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


def fit_T1_0B():
	fname="T1 0B soustraction"
	plt.figure(num=1,figsize=(6,4),dpi=80)
	plt.xticks(fontsize=15)
	plt.yticks(fontsize=15)
	plt.locator_params(axis='x', nbins=5)
	x,y=extract_data(fname,xcol=0,ycol=5)
	x=x*1e3
	y=y/max(y)
	plt.plot(x,y,'o',markerfacecolor="None",ms=5,mew=1,label='Experimental Data')
	popt,yfit=exp_fit_zero(x,y)
	print(popt)
	plt.plot(x,yfit,lw=3,label=r'exp($-t/\tau$)')
	popt,yfit=stretch_exp_fit_zero(x,y)
	print(popt)
	plt.plot(x,yfit,lw=3,label=r'exp($-\sqrt{t/\tau}$)',color=color(2))
	ax=plt.gca()
	# ax.set_xlabel(r'Dark time (ms)',fontsize=20)
	# ax.set_ylabel(r'Spin polarization (AU)' ,fontsize=20)
	plt.legend(fontsize=15)
	plt.show()


x,y=extract_data('ESR 0B')
y=y/max(y)
plt.plot(x,y)

x,y=extract_data('ESR 1 raie zoom')
y=y/max(y)
x=x-2695+2866
plt.plot(x,y)

x,y=extract_data('esr 100 +2V')
y=y/max(y)
x,y=x[70:110],y[70:110]
x=x-2782+2866
plt.plot(x,y)

plt.show()