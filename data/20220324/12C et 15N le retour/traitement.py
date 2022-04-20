import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


def plot_ESR():
	x,y=extract_data('ESR B transverse 70 G 15 dB')
	n=len(y)
	x=np.linspace(x[0],x[-1],n)


	# x2=list(x[0:85])+list(x[95:139])
	# y2=list(y[0:85])+list(y[95:139])
	x2=x[:110]
	y2=y[:110]
	plt.plot(x,y)
	# plt.plot(x2,y2,'x')

	popt,yfit=lor_fit(x2,y2,x0=2.879)
	def f(x,amp,x0,sigma,ss) :
		return ss+amp*1/(1+((x-x0)/(sigma))**2)
	plt.plot(x,f(x,*popt),label='HWHM=%.0f kHz'%(popt[2]*1e6))
	plt.legend()


plt.figure(num=1,figsize=(3,2),dpi=80)
plt.xticks(fontsize=11)
plt.yticks(fontsize=12)
# x,y=extract_data('scan EM weekend',ycol=3)
# y=y/max(y)
# x=x-x[259]
# x=x*35
x,y=extract_data("scan PL à l'ancienne")
x2=list(x)
y2=list(y)
for i in range(len(y)):
	e=y[i]
	if e <0 :
		x2.remove(x[i])
		y2.remove(y[i])

x=np.array(x2)
y=np.array(y2)

def find_B_EM():
	x,y=extract_data("ESR EM 3V pour le 2e scan PL")
	plt.plot(x,y)
	peaks=[2723,2723,2758,2758,3044,3050,3071,3075]
	B=find_B_cartesian_mesh(peaks)
	print(B,B.amp/3)
	# B=76.9 G @ 3V
x=x-x[104]
x=x*30
x=-x
y=y/max(y)
plt.plot(x,y)
plt.show()




