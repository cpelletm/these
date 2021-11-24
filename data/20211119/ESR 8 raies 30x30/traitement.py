import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *



xmin=1580
xmax=1720
n=30
xs=np.linspace(0,10,n)

#J'ai pas réussi à faire le décalage en fréquence, en tout cas pour la raie spin nucl. Ca doit être faisable quand meme

data=np.zeros((n,n))
for j in range(n) :
	print(j)
	for i in range(n) :
		x,y=extract_data('x=%.6f,y=%.6f'%(xs[i],xs[j]))
		x=x[xmin:xmax]
		y=y[xmin:xmax]
		dx=x[1]-x[0]
		cs=find_ESR_peaks(x,y,width=1.5,threshold=0.8)
		popt,yfit=ESR_fixed_amp_and_width(x,y,cs,typ='lor')

		# c=sum(popt[1])/3
		# if i==0 and j==0 :
		# 	c=c-3*dx
		# elif i!=0 :
		# 	while c-data[i-1,j]>0.5*dx :
		# 		c=c-dx
		# else :
		# 	while c-data[i,j-1]>0.5*dx :
		# 		c=c-dx
		data[i,j]=1/popt[2]
print_map(data)

# popt=[ss,centers,width,amp]



# x,y=extract_data('x=%.6f,y=%.6f'%(xs[27],xs[0]))
# plt.plot(x,y,'x-')
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# cs=find_ESR_peaks(x,y,width=1,threshold=0.8)
# popt,yfit=ESR_fixed_amp_and_width(x,y,cs,typ='lor')
# plt.plot(x,yfit)
# refs=popt[1]
# dx=x[1]-x[0]

# x,y=extract_data('x=%.6f,y=%.6f'%(xs[0],xs[0]))
# plt.plot(x,y,'x-')
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# cs=find_ESR_peaks(x,y,width=1,threshold=0.8)
# popt,yfit=ESR_fixed_amp_and_width(x,y,cs,typ='lor')
# plt.plot(x,yfit)
# pic=popt[1][0]
# compteur=0
# while pic > refs[0]+0.5*dx :
# 	pic=pic-dx
# 	compteur+=1
# print(compteur)
# x=x-compteur*dx
# plt.plot(x,yfit)


plt.show()
