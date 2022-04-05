import numpy as np
import matplotlib.pyplot as plt

t1=2
t2=4
t3=7
t4=8
t5=10

n=100
x1=np.linspace(0,t1,n)
x2=np.linspace(t1,t2,n)
x3=np.linspace(t2,t3,n)
x4=np.linspace(t3,t4,n)
x5=np.linspace(t4,t5,n)

x=list(x1)+list(x2)+list(x3)+list(x4)+list(x5)

ylas=[0]*n+[1]*n+[0]*n+[0]*n+[1]*n
yuW=[0]*n+[0]*n+[1]*n+[0]*n+[0]*n
osc=list(0.5+0.4*np.cos((x3-t2)/0.17)*np.exp(-(x3-t2)/3))
ypop=[0.33]*n+list(0.9-0.56*np.exp(-(x2-t1)/0.3))+osc+[osc[-1]]*n+list(0.9-(0.9-osc[-1])*np.exp(-(x5-t4)/0.3))
ysignal=[0]*n+list(1-0.66*np.exp(-(x2-t1)/0.3))+[0]*n+[0]*n+list(1-(1-osc[-1])*np.exp(-(x5-t4)/0.3))


# ylas=np.array(ylas)+6
# yuW=np.array(yuW)+4
# ypop=np.array(ypop)+2

# plt.plot(x,ylas,color='g',lw=2)
# plt.plot(x,yuW,color='purple',lw=2)
plt.plot(x,ypop,color='black',lw=2)
# plt.plot(x,ysignal,color='darkred',lw=2)
plt.show()