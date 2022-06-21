import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

#les x et y sont inversés pour cette série
fnames=glob.glob('*.csv')
fval=[float(fnames[i][2:-5]) for i in range(len(fnames))] 
fnames=[s for _,s in sorted(zip(fval,fnames))]
fval=sorted(fval)


n=len(fval)
posm=np.zeros(n)
posp=np.zeros(n)
for i in range(n):

	fname=fnames[i]
	x,y=extract_data(fname)
	peaks=find_ESR_peaks(x,y,width=4,threshold=0.3)
	ecart_min=peaks[1]-peaks[0]
	pos=0
	for k in range(0,len(peaks)-1) :
		if peaks[k+1]-peaks[k]<ecart_min :
			ecart_min=peaks[k+1]-peaks[k]
			pos=k
	posm[i]=peaks[pos]
	posp[i]=peaks[pos+1]

#Cauchemard du vendredi soir putain....
posm=list(posm)
posp=list(posp)
fval_short=list(fval)

posm=posm[0:55]+posm[75:100]+posm[106:]
posp=posp[0:55]+posp[75:100]+posp[106:]
fval_short=fval[0:55]+fval[75:100]+fval[106:]



plt.plot(fval_short,posm,'x')
popt,yfit=fit_ordre_4(fval_short,posm)
# plt.plot(fval_short,yfit)
print(popt)
x=np.linspace(0.8,5,501)
freqs=2862.3732486672525+5.336405357793713*x+0.4892478887834715*x**2+0.4361255116793501*x**3-0.047696861387582994*x**4
plt.plot(x,freqs)
plt.plot(fval_short,posp,'x')
popt,yfit=fit_ordre_4(fval_short,posp)
print(popt)
x=np.linspace(0.8,5,501)
freqs=2879.6100403000905-10.350382035600058*x+8.72563530864743*x**2-0.5448652051415266*x**3+0.008459469208990177*x**4
plt.plot(x,freqs)

plt.show()