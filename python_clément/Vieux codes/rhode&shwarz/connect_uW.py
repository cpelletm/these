# Simple Python script using PyVISA
#
# The script opens a connection to an instrument and queries its identification string
# with a SCPI command '*IDN?'
# Preconditions:
# - R&S VISA or NI VISA installed
# - Python 2.7.13 or newer installed
# - Python PyVISA 1.7 package or newer installed
# - Resource string adjusted to fit your instrument physical connection

import visa
import numpy as np
import time

n_debug=0

resourceString1 = 'TCPIP::192.168.2.101::INSTR'  # Standard LAN connection (also called VXI-11)
resourceString2 = 'TCPIP::192.168.2.101::hislip0'  # Hi-Speed LAN connection - see 1MA208
resourceString3 = 'GPIB::20::INSTR'  # GPIB Connection
resourceString4 = 'USB0::0x0AAD::0x0054::182239::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"

rm = visa.ResourceManager()
PG = rm.open_resource( resourceString4 )
#print(dir(PG))
PG.write_termination = '\n'
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
# PG.clear()  # Clear instrument io buffers and status

idn_response = PG.query('*IDN?')  # Query the Identification string
print ('Hello, I am ' + idn_response)
for i in range(10) :
	PG.query('SYSTem:ERRor:NEXT?') #C'est crade mais c'est pour clear l'error queue

PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1
PG.write(':LIST:DELete:ALL')
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1
PG.write('OUTP ON') #OF/ON pour allumer éteindre la uW
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1
PG.write('LIST:SEL "new_list"') #Il lui faut un nom, j'espere qu'il y a pas de blagues si je réécris dessus
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1

def create_list_freq(fmin,fmax,level,n_points) :
	#Frequecy given in GHz
	freq_list=np.linspace(fmin,fmax,n_points)
	instruction_f='SOUR:LIST:FREQ'
	for f in freq_list :
		if f==max(freq_list) :
			instruction_f+=' %1.4f GHz'%f
		else :
			instruction_f+=' %1.4f GHz,'%f
	instruction_pow='SOUR:LIST:POW'
	for f in freq_list :
		if f==max(freq_list) :
			instruction_pow+=' %1.4f dBm'%level
		else :
			instruction_pow+=' %1.4f dBm,'%level
	return instruction_f,instruction_pow

freq_list,pow_list=create_list_freq(2.8,2.95,0,151)
# print(freq_list)

PG.write(freq_list)
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1 #¶5
PG.write(pow_list)
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1
print(PG.query('LIST:FREQ:POIN?'))
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1
print(PG.query('LIST:POW:POIN?'))
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1
PG.write('LIST:DWEL 100ms')
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1
PG.write('LIST:MODE AUTO')
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1 #10

PG.write('SOURce:LIST:TRIGger:SOURce SINGle')
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1

PG.write('FREQ:MODE LIST')
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1


PG.write('SOUR:LIST:TRIG:EXEC')
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1 #13


time.sleep(2)

PG.write('SOUR:FREQ:MODE CW')
PG.write('*WAI')
print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
n_debug+=1

# PG.write('*RST')
# PG.write('*WAI')
# print(PG.query('SYSTem:ERRor:NEXT?')+'n_debug=%i'%n_debug)
# n_debug+=1

