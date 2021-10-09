import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from analyse import *


fnames=glob.glob('*.csv')
Ps=[float(fname[2:-7]) for fname in fnames]
ar=np.array([fnames,Ps])
fnames=[x for _,x in sorted(zip(Ps,fnames))] #magie noire d'internet
Ps=sorted(Ps)
n=len(Ps)

# Cs=[]
# for i in range(n) :
# 	x,y=extract_data(fnames[i])
# 	# y=y/y[0]
# 	Cs+=[max(y[280:298])-min(y[280:298])]
# 	y=list(y)
# 	# print(y.index(max(y[280:298])),y.index(min(y[280:298])))
# Cs=np.array(Cs)/max(Cs)
# plt.plot(Ps,Cs,'o',markerfacecolor="None",ms=8,mew=2,label='C13+')


# Cs=[]
# for i in range(n) :
# 	x,y=extract_data(fnames[i])
# 	# y=y/y[0]
# 	Cs+=[max(y[228:246])-min(y[228:246])]
# 	y=list(y)
# 	# print(y.index(max(y[228:246])),y.index(min(y[228:246])))
# Cs=np.array(Cs)/max(Cs)
# plt.plot(Ps,Cs,'x',markerfacecolor="None",ms=8,mew=2,label='C13-')

Cs=[]
for i in range(n) :
	x,y=extract_data(fnames[i])
	zero=sum(y[:50])/50
	y=y/zero
	Cs+=[max(y)-min(y)]
Cs=np.array(Cs)
plt.plot(Ps,Cs,'^',markerfacecolor="None",ms=8,mew=2,label='DQ')
# plt.xscale('log')
plt.legend()
plt.show()