import numpy as np

#unit = s,ms,us,ns


def rabi(t_scan,n_scan,t_lect,t_ecl):
	with open('PB_instructions.txt','w') as f:
		for s in t_scan.split() :
			try :
				val=float(s)
			except :
				unit=s
		taux=np.linspace(0,val,n_scan)
		for i in range(1,len(taux)) :
			tau=str(taux[i])+unit
			if i == 1:
				f.write('label : ')
			else : 
				f.write('\t')

			f.write('0b 0100, '+t_ecl+'\n')
			f.write('\t0b 1000, '+tau+'\n')
			f.write('\t0b 0110, '+t_lect) #Est-ce qu'on peut compter sur les deux fronts ?
			if i==len(taux)-1:
				f.write(', branch, label')
			else :
				f.write('\n')



# rabi('1000 us',101,'500 us','500 us')


def AOM_on():
	with open('PB_instructions.txt','w') as f:
		f.write('label: 0b 0100, 100 ms, branch, label')

AOM_on()


