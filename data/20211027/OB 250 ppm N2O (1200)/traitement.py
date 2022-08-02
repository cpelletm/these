import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax=plt.gca()


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

# fname='ESR +2 V' #+2 V : B=87.225841 G
# fname='ESR -2 V' #-2V : B= 107.318993 G
# x,y=extract_data(fname)
# plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=1)
# cs=find_ESR_peaks(x,y,returnUnit='x',precise=True)
# print(cs)
# print(find_B_spherical(cs))
# plt.show()

# x=np.array([+2,-2])
# y=[87.225841,-97.099537]
# popt,yfit=lin_fit(x,y)
# print(popt)


popt=[46.08134449999998, -4.936848000000009]
fname='scan 100 juste substrat nuit'
x,y=extract_data(fname)
x=(popt[0]*x+popt[1])
xmin=1060
xmax=-1
x=x[xmin:xmax]
y=y[xmin:xmax]
plt.plot(x,y,'o',markerfacecolor="None",ms=6,mew=0.5,label='SBST-B (1200°)')

popt=[50.66541125, -8.47312149999999]
fname='scan substrat 50 ppm N2 (800)'
x,y=extract_data(fname)
x=(popt[0]*x+popt[1])
xmin=1060
xmax=-1
y=y+0.07
x=x[xmin:xmax]
y=y[xmin:xmax]
plt.plot(x,y,'o',markerfacecolor="None",ms=6,mew=0.5,label='SBST-B (800°)')

xVH=56
xC13=20
xWar1=122

ymin=-0.05
ymax=0.125

# plt.plot([xVH,xVH],[ymin,ymax],ls='--',color=color(3))

# fname='scan 100 MNOB 5 (800)'
# x,y=extract_data(fname)
# x=44.06668149999998*x-8.966174000000011
# xmin=300
# xmax=470
# # x=x[xmin:xmax]
# # y=y[xmin:xmax]
# plt.plot(x,y,'o-',markerfacecolor="None",ms=8,mew=1,label='MNOB 05 (800°)')

# ax.tick_params(labelsize=20)
# ax.set_xlabel(r'B $\parallel$[100] (G)',fontsize=12)
# ax.set_ylabel(r'Demodulated PL' ,fontsize=12)
ax.legend()
plt.show()