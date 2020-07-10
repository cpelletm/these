import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.optimize import curve_fit

class curveFitting(): # import numpy as np // from scipy.optimize import curve_fit
    def __init__(self,x,y):
        self.x=np.array(x)
        self.y=np.array(y)
        self.fit=np.zeros(len(x))

        self.coefs=[]

    def lin(self): #fit : ax+b
        A=np.vstack([self.x,np.ones(len(self.x))]).T
        a,b = np.linalg.lstsq(A, self.y, rcond=None)[0]
        self.coefs=[a,b]
        self.fit=a*x+b
        self.label="%3.2Ex+%3.2E"%(a,b)

    def exp(self,tau=1,A=1,B=0): #fit : B+A*exp(-x/tau)
    	def f(x,A,B,tau):
    		return B+A*np.exp(-x/tau)
    	p0=[A,B,tau]
    	popt, pcov = curve_fit(f, self.x, self.y, p0)
    	self.coefs=popt
    	A=popt[0]
    	B=popt[1]
    	tau=popt[2]
    	self.fit=B+A*np.exp(-self.x/tau)
    	self.label="tau=%4.3E"%tau


x=np.arange(0,100,1)
rd=np.zeros(len(x))
for i in range(len(rd)) :
	rd[i]=random.random()

y=np.exp(-(x+5*rd)/10)+5


cf=curveFitting(x,y)
getattr(cf,'exp')()

method_list = [func for func in dir(cf) if (callable(getattr(cf, func)) and func[0]!="_")]





plt.plot(x,y,'x')
plt.plot(x,cf.fit,label=cf.label)
plt.legend()
plt.show()