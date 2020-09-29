import numpy as np

#unit = s,ms,us,ns


def rabi(taux,t_lect,t_ecl):
	with open('PB_instructions.txt','w') as f:
		for i in range(len(taux)) :
			tau=taux[i]
			if i == 0:
				f.write('label : ')
			else : 
				f.write('\t')

			f.write('0b 0100, '+t_ecl+'\n')
			f.write('\t0b 1000, '+tau+'\n')
			f.write('\t0b 0110, 20 ns \n') 
			f.write('\t0b 0100, '+t_lect+'\n') 
			f.write('\t0b 0110, 20 ns') 
			if i==len(taux)-1:
				f.write(', branch, label')
			else :
				f.write('\n')




def t_pola(dt,n_points) :
	with open('PB_instructions.txt','w') as f:
		for i in range(n_points):
			if i == 0:
				f.write('label : ')
			else : 
				f.write('\t')
			if i < n_points/2 :
				f.write('0b 1110, 20 ns\n')
				f.write('\t0b 1100, '+dt)
			else :
				f.write('0b 0110, 20 ns\n')
				f.write('\t0b 0100, '+dt)
			if i==n_points-1:
				f.write(', branch, label')
			else :
				f.write('\n')

# t_pola('50 us',500)

def ESR(t_scan='1 ms') :
	with open('PB_instructions.txt','w') as f:
		for s in t_scan.split() :
			try :
				val=float(s)
			except :
				unit=s
		f.write('label: 0b 0111, '+str(val/2)+unit+'\n')
		f.write('\t0b 0000, '+str(val/2)+unit+', branch, label')


# ESR()


def AOM_on():
	with open('PB_instructions.txt','w') as f:
		f.write('label: 0b 0100, 100 ms, branch, label')

AOM_on()

def APD(dt):
	with open('PB_instructions.txt','w') as f:
		f.write('label: 0b 0110, %f ms\n'%(dt/2))
		f.write('\t0b 0100,  %f ms, branch, label'%(dt/2))

# APD(30)




