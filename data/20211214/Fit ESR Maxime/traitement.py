import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/zouzou/these/python_clément')
from analyse import *

x,y=extract_data('pos_1_0_delay_480')
plt.plot(x,y,'x')
# peaks=find_ESR_peaks(x,y,threshold=0.5)
peaks=[2676,2712,2753,2785]
# popt,yfit=ESR_n_pics(x,y,peaks)
# peaks=popt[1]
# print(peaks)
# startingB=magneticField(x=28.9,y=17.03,z=101.68)
# B=find_B_cartesian(peaks,transis='-')
# print(B,B.transitions4ClassesMoins())
popt,yfit=find_nearest_ESR(x,y,peaks,transis='-',returnType='cartesian',fittingProtocol='cartesian')
#spehrical : [107.61199641007401, 12.871940256660517, 42.58586653428593]
#Cartesian : [21.27487424726588, 11.049219398251672, 104.90775113314604]
plt.plot(x,yfit)
print(popt)

plt.show()