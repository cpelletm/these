import numpy as np
import matplotlib.pyplot as plt

#La ref ce sera les eV

q=1.6e-19
h=6.63e-34
kb=1.38e-23
c=3e8
lambda_central=740e-9 #SiV

def tohz (ev):
	return ev*q/h
	
def fromhz (hz) :
	return hz*h/q
	

def tolmabda (ev):
	return c/(ev*q/h)*1e9
	
def fromlambda (nm):
	return c/(nm*q/h)*1e9
	
def todlambda (ev):
	return ev*q/h*lambda_central**2/c*1e9
	
def fromdlambda (nm):
	return nm*c*1e-9*h/q/lambda_central**2
	
def tocm (ev) :
	return ev*q/h/c/100	
	
def fromcm (cm) :
	return 100*cm*h*c/q
	
def totemp(ev) :
	return ev*q/kb
	
def fromtemp(K) :
	return K*kb/q
	
evrange=[fromhz(1e9),fromhz(1e12),fromhz(1e6)]
evrange+=[fromlambda(400),fromlambda(800),fromlambda(740)]
evrange+=[fromdlambda(1),fromdlambda(10)]
evrange+=[fromcm(1)]
evrange+=[fromtemp(300), fromtemp(4)]
for i in range(10) :
	evrange+=[5*10**(-i)]
	evrange+=[10**(-i)]
	
evrange.sort(reverse=True)
f=open('conversion.dat','w+')
	
compteur = 0
for ev in evrange :
	line = "{0:1.2e} & {1:1.2e} & {2:1.2e} & {3:1.2e} & {4:1.2e} & {5:1.2e} \\\ \n".format(ev,tohz(ev),tolmabda(ev),tocm(ev), totemp(ev), todlambda(ev) )
	f.write(line)
	if compteur%5==4 :
		f.write("&&&&& \\\ \n")
	compteur+=1
	
f.close() 
	
        


