import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *




# fname='ESR 1 raie clean'
# x,y=extract_data(fname)
# plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=1)
# cs=find_ESR_peaks(x,y,width=2,threshold=0.7)
# print(cs)
# popt,yfit=ESR_fixed_amp_and_width(x,y,cs,width=1,typ='lor')
# plt.plot(x,yfit,lw=2,label='width=%4.3f MHz'%popt[2])
# plt.xlabel('frequency (MHz)')
# plt.ylabel('demodulated PL (UA)')
# print(popt)
# plt.legend()

# fname='ESR 100 +2V' #+2 V : B=79.167189 G
# fname='ESR 100 -2V' #-2V : B= 97.099537 G
# x,y=extract_data(fname)
# plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=1)
# cs=find_ESR_peaks(x,y,returnUnit='x',precise=True)
# print(cs)
# print(find_B_spherical(cs))
# plt.show()

# x=np.array([+2,-2])
# y=[79.167189,-97.099537]
# popt,yfit=lin_fit(x,y)
# print(popt)
#B=444.06668149999998*V -8.966174000000011


fname='scan 100 phi=3'
x,y=extract_data(fname)
x=44.06668149999998*x-8.966174000000011
xmin=300
xmax=470
x=x[xmin:xmax]
y=y[xmin:xmax]
plt.plot(x,y,'o-',markerfacecolor="None",ms=8,mew=1,label='MNOB 05 (800°)')


# fname='scan MNOB 03 (1200)'
# x,y=extract_data(fname)
# x=49.217*x-9.477
# y=y+0.01
# xmin=300
# xmax=450
# x=x[xmin:xmax]
# y=y[xmin:xmax]
# plt.plot(x,y,'o-',markerfacecolor="None",ms=8,mew=1,label='MNOB 03 (1200°)')
ax=plt.gca()
ax.tick_params(labelsize=20)
# ax.set_xlabel(r'B $\parallel$[100] (G)',fontsize=20)
# ax.set_ylabel(r'Demodulated PL' ,fontsize=20)
plt.show()