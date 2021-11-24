import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *




data=np.zeros((11,11))
for i in range(11) :
	for j in range(11) :
		x,y=extract_data('x=%i.000000,y=%i.000000'%(i,j))
		peaks=find_ESR_peaks(x,y,threshold=0.3)
		popt,yfit=ESR_n_pics(x,y,peaks)
		centers=popt[1]
		widths=popt[2]
		amps=popt[3]
		data[i,j]=amps[0]
	
	
print_map(data)



x,y=extract_data('x=%i.000000,y=%i.000000'%(1,8))
plt.plot(x,y,'x-')

peaks=find_ESR_peaks(x,y,threshold=0.3,precise=True)



# plt.show()
