import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *



xmin=245
xmax=271

n=30
xs=np.linspace(0,10,n)

data=np.zeros((n,15))
for j in range(15) :
	print(j)
	for i in range(n) :
		x,y=extract_data('x=%.6f,y=%.6f'%(xs[i],xs[j]))
		cs=find_ESR_peaks(x,y,width=10)
		cs=list(cs)
		if len(cs) > 4 :
			if cs[1]-cs[0] < 15 :
				if y[list(x).index(cs[0])] > y[list(x).index(cs[1])] :
					cs.pop(1)
				else :
					cs.pop(0)
			else :
				print('i=%i,j=%i'%(i,j))
		popt,yfit=ESR_n_pics(x,y,cs,width=5,typ='gauss')
		cs=popt[1]
		widths=popt[2]
		amps=popt[3]
		data[i,j]=amps[0]/amps[-1]
print_map(data)

#1,0 ; 21,0 ; 21,13

# x,y=extract_data('x=%.6f,y=%.6f'%(xs[27],xs[11]))
# plt.plot(x,y,'x-')
# cs=find_ESR_peaks(x,y,width=10)
# cs=list(cs)
# if len(cs) > 4 :
# 	if y[list(x).index(cs[0])] > y[list(x).index(cs[1])] :
# 		cs.pop(1)
# 	else :
# 		cs.pop(0)
# print(cs)
# popt,yfit=ESR_n_pics(x,y,cs,width=5,typ='gauss')
# print(popt)
# plt.plot(x,yfit)

# x,y=extract_data('x=%.6f,y=%.6f'%(xs[0],xs[0]))
# plt.plot(x,y,'x-')
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# popt,yfit=parabola_fit(x,y)
# print(popt)
# plt.plot(x,yfit)


plt.show()
