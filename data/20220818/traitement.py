import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

fnames=['ESR 03V champ transverse.csv', 'ESR 1 raie.csv', 'ESR raie champ transverse 0.3 V zoom.csv', 'ESR 1V.csv', 'ESR 1 raie champ transverse.csv', 'ESR 3V.csv', 'ESR raie champ transverse 0.5 V zoom.csv', 'ESR 0B.csv', 'ESR raie champ transverse 1 V zoom.csv']

f0=[0,2705,0,0,2905,0,0,2870,0]

plt.figure(num=1,figsize=(6,4),dpi=80)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.locator_params(axis='x', nbins=5)

# fname='Adamas 150/ESR 1 raie.csv'
# x,y=extract_data(fname)
# y=y-min(y)
# y=y/max(y)
# x=x-2705
# xmin=find_elem(x,-15)
# xmax=find_elem(x,15)
# plt.plot(x[xmin:xmax],y[xmin:xmax],label='ADM-150')

# fname='Adamas 150/ESR 1 raie champ transverse.csv'
# x,y=extract_data(fname)
# y=y-min(y)
# y=y/max(y)
# x=x-2905
# xmin=find_elem(x,-15)
# xmax=find_elem(x,15)
# plt.plot(x[xmin:xmax],y[xmin:xmax])

# fname='Adamas 150/ESR 0B.csv'
# x,y=extract_data(fname)
# y=y-min(y)
# y=y/max(y)
# x=x-2870
# xmin=find_elem(x,-15)
# xmax=find_elem(x,15)
# plt.plot(x[xmin:xmax],y[xmin:xmax])


['rose/B transverse zoom 0.5V.csv', 'rose/ESR 0B (+0.00V).csv', 'rose/ESR 1 raie.csv', 'rose/ESR 0B (+0.06V).csv', 'rose/ESR 0B (+0.02V).csv', 'rose/B transverse zoom 0.5V réaligné (genre beaucoup).csv', 'rose/ESR champ transverse 2V.csv', 'rose/B transverse zoom 2V.csv', 'rose/B transverse zoom 1V.csv']

# fname='rose/ESR 1 raie.csv'
# x,y=extract_data(fname)
# y=y-min(y)
# y=y/max(y)
# x=x-2728
# xmin=find_elem(x,-15)
# xmax=find_elem(x,15)
# width=2.6+2.8
# print(width)
# plt.plot(x[xmin:xmax],y[xmin:xmax],label='CVD-pink')

# fname='rose/B transverse zoom 2V.csv'
# x,y=extract_data(fname)
# y=y-min(y)
# y=y/max(y)
# x=x-2886.5
# xmin=find_elem(x,-15)
# xmax=find_elem(x,15)
# width=1.2+1.08
# print(width)
# plt.plot(x[xmin:xmax],y[xmin:xmax])

fname='rose/ESR 0B (+0.02V)'
x,y=extract_data(fname)
y=y-min(y)
y=y/max(y)
x=x-2870.5
xmin=find_elem(x,-15)
xmax=find_elem(x,15)
width=4.4-0.9
print(width)
plt.plot(x[xmin:xmax],y[xmin:xmax])



#~~~~~~~~~~~~~~~~~~~~~ Sumi 2

# fname='Sumi 2/ESR 1 raie'
# x,y=extract_data(fname)
# y=y-min(y)
# y=y/max(y)
# x=x-2678
# xmin=find_elem(x,-15)
# xmax=find_elem(x,15)
# width=3.5+3.16
# print(width)
# plt.plot(x[xmin:xmax],y[xmin:xmax],label='Sumi-2')

# fname='Sumi 2/ESR B transverse zoom'
# x,y=extract_data(fname)
# y=y-min(y)
# y=y/max(y)
# x=x-2885.8
# xmin=find_elem(x,-15)
# xmax=find_elem(x,15)
# width=2.86+2.64
# print(width)
# plt.plot(x[xmin:xmax],y[xmin:xmax])

# fname='Sumi 2/ESR 0B'
# x,y=extract_data(fname)
# y=y-min(y)
# y=y/max(y)
# x=x-2870.2
# xmin=find_elem(x,-15)
# xmax=find_elem(x,15)
# width=3.45+2.46
# print(width)
# plt.plot(x[xmin:xmax],y[xmin:xmax])

plt.plot([-15,15],[0.5,0.5])

plt.legend()
plt.show()
