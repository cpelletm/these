import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *


plt.figure(num=1,figsize=(3,2),dpi=80)
x,y=extract_data('ESR/V=-2.040000')
y=y/max(y)
plt.plot(x,y)
plt.xticks(fontsize=11)
plt.yticks(fontsize=12)

fnames,fval=extract_glob('ESR')
n=len(fval)

# i=-1
# print(fval[i])
# x,y=extract_data(fnames[i])
# peaks=find_ESR_peaks(x,y,precise=True)
# B=find_B_cartesian_mesh(peaks,transi='all')
# print(B,B.amp,B.angleFrom100(),B.angleFrom111())

# Bs=[np.array([78.55,31.8,16.86])*(x-0.17)/2.8 for x in fval]

# transis=np.zeros((n,8))
# for i in range(n):
# 	fname=fnames[i]
# 	x,y=extract_data(fname)
# 	cs=find_ESR_peaks(x,y,threshold=0.3)
# 	if len(cs)==8 :
# 		transis[i,:]=cs
# 	else :
# 		transis[i,:]=[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]

# for j in range(8):
# 	plt.plot(fval,transis[:,j],'x')


# transis=np.zeros((n,8))
# for i in range(n):
# 	cart=Bs[i]
# 	B=magneticField(cart[0],cart[1],cart[2])
# 	transis[i,:]=B.transitions4Classes()

# for j in range(8):
# 	plt.plot(fval,transis[:,j])

# y=list(transis[:35,0])+list(transis[65:,7])
# x=fval[:35]+fval[65:]


# plt.plot(x,y,'x')
# popt,yfit=fit_ordre_4(x,y)
# x=np.array(x)

# yfit=sum((x**i)*popt[-i-1] for i in range(len(popt)))
# plt.plot(x,yfit)
# print(popt)






# fnames,fval=extract_glob('T1')
# n=len(fval)
# taus=np.zeros(n)

# Bs=[np.array([78.55,31.8,16.86])*(x-0.17)/2.8 for x in fval]

# Bamps=[norm(B)*np.sign(B[0]) for B in Bs]

# for i in range(n):
# 	fname=fnames[i]
# 	x,y=extract_data(fname,ycol=5)
# 	T1ph=T1ph=0.003626
# 	popt,yfit=stretch_et_phonons(x,y,T1ph=T1ph)
# 	taus[i]=popt[1]

# nmin=106
# x=Bamps[nmin:]
# y=1/taus[nmin:]

# plt.plot(x,y)


plt.show()

