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

# fname='ESR 100 +2 V' #+2 V : B=88.957 G
# fname='ESR 100 -2 V' #-2V : B= 107.911 G
# x,y=extract_data(fname)
# plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=1)
# cs=find_ESR_peaks(x,y,returnUnit='x',precise=True)
# print(cs)
# print(find_B_spherical(cs))
# plt.show()

# x=np.array([+2,-2])
# y=[88.957,-107.911]
# popt,yfit=lin_fit(x,y)
# print(popt)
#B=49.217*V - 9.477


fname='scan 100 phi=3 nuit'
x,y=extract_data(fname)
x=49.217*x-9.477
xmin=300
xmax=450
x=x[xmin:xmax]
y=y[xmin:xmax]
plt.ylim((-0.015112794129843515, 0.0158428339153203))
plt.plot(x,y,'o-',markerfacecolor="None",ms=8,mew=1)
ax=plt.gca()
ax.tick_params(labelsize=20)



plt.show()