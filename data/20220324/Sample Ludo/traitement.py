import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.locator_params(axis='x', nbins=5)




# fname='T1 0B vert=exp orange=stretch'
fname='T1 100 2V toujours plus vite'
nmax=100
x,y=extract_data(fname,ycol=5)
x=x*1e3
y=y/max(y)
plt.plot(x[:nmax],y[:nmax],'x',markerfacecolor="None",ms=7,mew=1,label='Experimental Data',color=color(0))
popt,yfit=exp_fit_zero(x,y)
print(popt)
plt.plot(x[:nmax],yfit[:nmax],lw=3,label=r'exp($-t/\tau$)',color=color(1))
popt,yfit=stretch_exp_fit_zero(x,y)
print(popt)
plt.plot(x[:nmax],yfit[:nmax],lw=3,label=r'exp($-\sqrt{t/\tau}$)',color=color(2))

plt.legend()
plt.show()