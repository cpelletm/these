import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *


fnames,fval=extract_glob('T1')
n=len(fnames)
taus=np.zeros(n)
for i in range(n):
	fname=fnames[i]
	x,y=extract_data(fname,ycol=5)
	T1ph=0.003626
	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
	taus[i]=popt[1]

plt.plot(fval,1/taus)
plt.show()

# fnames,fval=extract_glob('ESR')
# n=len(fnames)
# transis1=[]
# transis2=[]
# for i in range(n):
# 	fname=fnames[i]
# 	x,y=extract_data(fname)
# 	cs=find_ESR_peaks(x,y)
# 	if len(cs)==2 :
# 		cs=find_ESR_peaks(x,y,precise=True)
# 		transis1+=[cs[0]]
# 		transis2+=[cs[1]]
# 	else :
# 		transis1+=[np.nan]
# 		transis2+=[np.nan]

# plt.plot(fval,transis1,'x')
# plt.plot(fval,transis2,'x')
# plt.show()
