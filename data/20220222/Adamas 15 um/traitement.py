import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
sys.path.append('/home/pellet-mary/these/python_clément')
from analyse import *

"""
Calculs Eta :
eta0=0.3849/4
eta=(0.3849/4+2*0.6507/4+0.8328/4)/30

eta c13 0B : 0.05 eta0
eta base +/- 1 classe : 3-4 eta0
eta 121 : 10 eta0
eta 22 : 7.2 eta0
eta 31 : 28.4 eta0
eta 40 : 42.8 eta0
eta 0B sans DQ : 51-55 eta0

Mesures T1 :
C13 0B : baseline (T1=0)
1x : T1=0.00609014
2x2 : T1=0.00031344 ; 0.00030245 ; 0.0002971 ; 0.0003125
1x2x1 : T1= 0.00020091 ; 0.00022116 ; 
Bon j'arrête en cours de route parce que ca fitte pas si bien (cf T1 121 nuit)


T1 avec un alpha=0.82 fixe :
1x : 0.00086313

"""




#Baseline : T1=1.21753193e-03 ; alpha=8.29849679e-01 
fname='T1 0B court'
x,y=extract_data(fname,ycol=5)
plt.plot(x,y)
# popt,yfit=stretch_with_baseline(x,y,tau_BL=1.21753193e-03,alpha_BL=8.29849679e-01)
popt,yfit=stretch_arb_exp_fit_zero(x,y,alpha=0.82,fixed=True)
plt.plot(x,yfit)
print(popt)
plt.show()