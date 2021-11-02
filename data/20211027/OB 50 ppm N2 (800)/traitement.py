import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *





# cs=[2746.490,3046.340] #+2V
# cs=[3082.486,2727.596] #-2V
# print(cs)
# print(find_B_spherical(cs))
# plt.show()

# x=np.array([+2,-2])
# y=[92.857701,-109.803944]
# popt,yfit=lin_fit(x,y)
# print(popt)


popt=[50.66541125, -8.47312149999999]

fname='scan substrat 100 long'
x,y=extract_data(fname)
x=(popt[0]*x+popt[1])
xmin=1060
xmax=-1
# x=x[xmin:xmax]
# y=y[xmin:xmax]
plt.plot(x,y,'o-',markerfacecolor="None",ms=8,mew=1,label='N2O 50 ppm (800°)')


# fname='scan 100 MNOB 5 (800)'
# x,y=extract_data(fname)
# x=44.06668149999998*x-8.966174000000011
# xmin=300
# xmax=470
# # x=x[xmin:xmax]
# # y=y[xmin:xmax]
# plt.plot(x,y,'o-',markerfacecolor="None",ms=8,mew=1,label='MNOB 05 (800°)')
# ax=plt.gca()
# ax.tick_params(labelsize=20)
# ax.set_xlabel(r'B $\parallel$[100] (G)',fontsize=20)
# ax.set_ylabel(r'Demodulated PL' ,fontsize=20)
plt.show()