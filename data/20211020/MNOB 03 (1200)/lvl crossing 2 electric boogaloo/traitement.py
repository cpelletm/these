import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
from analyse import *
from scipy.signal import find_peaks




# fname='ESR -1.6V'
# x,y=extract_data(fname)
# plt.plot(x,y,'o',markerfacecolor="None",ms=8,mew=1)
# cs=find_ESR_peaks(x,y,width=6,threshold=0.1)
# print(cs)

# # popt,yfit=ESR_n_pics(x,y,cs)
# popt,yfit=find_nearest_ESR(x,y,cs,returnType='cartesian')
# plt.plot(x,yfit,lw=2)

# print(popt)

# fname='ESR -1.6V'
# x,y=extract_data(fname)
# cs=find_ESR_peaks(x,y,width=6,threshold=0.1)
# B16=find_B_spherical(cs)

# fname='ESR -1.8V'
# x,y=extract_data(fname)
# cs=find_ESR_peaks(x,y,width=6,threshold=0.1)
# B18=find_B_spherical(cs,startingB=B16)

# fname='ESR -2V'
# x,y=extract_data(fname)
# cs=find_ESR_peaks(x,y,width=6,threshold=0.15)
# B2=find_B_spherical(cs,startingB=B18)

# print(B2.cartesian)

B2=np.array([ 40.13295929 , 27.24256421, 120.95138062])
B18=np.array([ 39.31933443 ,22.43052865, 119.41573909])
B16=np.array([38.68270793205372, 16.403977792279605, 117.24147662164134])
B15=np.array([38.25087830303723, 13.091069138360165, 116.60798506391646])

Bmin=B2
Bmax=B2+(B15-B2)*10
dB=Bmax-Bmin
transis=[]
Bs=[]
n=100
for i in range(n) :
	B=Bmin+i/n*dB
	B=magneticField(x=B[0],y=B[1],z=B[2])
	transis+=[B.transitions4ClassesMoins()]
	Bs+=[np.linalg.norm(i/n*dB)]
transis=np.array(transis)
vs=np.linspace(-2,2,n)


for i in range(4) :
	plt.plot(vs,transis[:,i])



plt.show()

