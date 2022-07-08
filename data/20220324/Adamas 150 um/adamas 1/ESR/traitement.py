import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

petite_figure()

def plot_NRJ_V1():
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

# plot_NRJ_V1()

def simple_plot(i=0):
	fnames=glob.glob('*.csv')
	fval=[float(fnames[i][2:-5]) for i in range(len(fnames))] 
	fnames=[s for _,s in sorted(zip(fval,fnames))]
	fval=sorted(fval)
	fval=np.array(fval)
	n=len(fval)
	fname=fnames[i]
	x,y=extract_data(fname)
	xmax=find_elem(2950,x)
	plt.plot(x[:xmax],y[:xmax])

	fmoins_th=2862.3732486672525+5.336405357793713*fval+0.4892478887834715*fval**2+0.4361255116793501*fval**3-0.047696861387582994*fval**4
	fplus_th=2879.6100403000905-10.350382035600058*fval+8.72563530864743*fval**2-0.5448652051415266*fval**3+0.008459469208990177*fval**4

	fm=fmoins_th[i]
	fp=fplus_th[i]
	m=find_elem(fm,x)
	M=find_elem(fp,x)
	xtofit=x[m-20:M+20]
	ytofit=y[m-20:M+20]
	# plt.plot([fmoins_th[i],fmoins_th[i]],[0,1])
	# plt.plot([fplus_th[i],fplus_th[i]],[0,1])
	# plt.plot(xtofit,ytofit)

	popt,yfit=ESR_n_pics(xtofit,ytofit,[fm,fp],typ='gauss')
	# plt.plot(xtofit,yfit)
	print(popt)

simple_plot(0)

peaks=[2816,2844,2844,2863,2877,2898,2898,2923]
B=find_B_cartesian_mesh(peaks)
print(B,B.norm,B.transitions4Classes())

def find_NRJ_V2():
	fnames=glob.glob('*.csv')
	fval=[float(fnames[i][2:-5]) for i in range(len(fnames))] 
	fnames=[s for _,s in sorted(zip(fval,fnames))]
	fval=sorted(fval)
	fval=np.array(fval)
	n=len(fval)

	fmoins_th=2862.3732486672525+5.336405357793713*fval+0.4892478887834715*fval**2+0.4361255116793501*fval**3-0.047696861387582994*fval**4
	fplus_th=2879.6100403000905-10.350382035600058*fval+8.72563530864743*fval**2-0.5448652051415266*fval**3+0.008459469208990177*fval**4

	fpexp=[]
	fmexp=[]
	for i in range(n):
		# print(i)
		fname=fnames[i]
		x,y=extract_data(fname)


		fm=fmoins_th[i]
		fp=fplus_th[i]
		m=find_elem(fm,x)
		M=find_elem(fp,x)
		xtofit=x[m-20:M+20]
		ytofit=y[m-20:M+20]

		popt,yfit=ESR_n_pics(xtofit,ytofit,[fm,fp])
		fmexp+=[popt[1][0]]
		fpexp+=[popt[1][1]]

	nmax=180
	Bs=(np.array(fval)-0.17)*31
	plt.plot(Bs[:nmax],fmexp[:nmax])
	plt.plot(Bs[:nmax],fpexp[:nmax])



# find_NRJ_V2()

plt.show()