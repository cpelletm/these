from sympy import *

x,t,z,tau,gamma=symbols('x t z tau gamma')

init_printing(use_unicode=True)

#print(diff(sin(x)*exp(x), x)

print(integrate(exp(-(x*gamma))*exp(-1/(t*gamma))/sqrt(gamma**3*t*pi), (gamma,0,z)))
