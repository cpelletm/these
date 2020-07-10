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
import numpy
import time

resourceString1 = 'TCPIP::192.168.2.101::INSTR'  # Standard LAN connection (also called VXI-11)
resourceString2 = 'TCPIP::192.168.2.101::hislip0'  # Hi-Speed LAN connection - see 1MA208
resourceString3 = 'GPIB::20::INSTR'  # GPIB Connection
resourceString4 = 'USB0::0x0AAD::0x0197::5601.3800k03-101213::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"

rm = visa.ResourceManager()
PG = rm.open_resource( resourceString4 )
print(dir(PG))
PG.write_termination = '\n'

PG.clear()  # Clear instrument io buffers and status

idn_response = PG.query('*IDN?')  # Query the Identification string

print ('Hello, I am ' + idn_response)



#PG.write('INST 1;APPLY "5,DEF";OUTP:SEL 1;OUTP:GEN 1')

#PG.write('OUTP:GEN 1')

PG.write('OUTP:GEN 0')
PG.write('*WAI')
PG.write('INST 1')
PG.write('*WAI')
PG.write('VOLTage:RAMP ON')
PG.write('*WAI')
PG.write('VOLTage:EASYramp:TIME %f'% 1)#le temps est en secondes et j'arrive pas à faire 0.1 sec...
PG.write('*WAI')
PG.write('OUTP:SEL 1')
PG.write('*WAI')
PG.write('APPLY "%f,DEF"' % 1)
PG.write('*WAI')
PG.write('OUTP:GEN 1')
PG.write('*WAI')
print(PG.query('OUTP:GEN?'))
time.sleep(2)
PG.write('OUTP:GEN 0')
PG.write('*WAI')


#PG.write('INST 1;APPLY "%f,DEF";OUTP:SEL 1;OUTP:GEN 1' % 0) # INST i : selectionne channel i; APPLY "V,A" : choisis la tension et le courant max du channel en V et A (DEF = default)
# OUTP:SEL 1 : output on pour la channel en question (bouton Ch i s'allume) ; OUTP:GEN 1 : output general ON (bouton Ouput s'allume)
PG.write('*WAI') #attend que la commande précédente soit executée


print(PG.query('VOLTage:EASYramp:TIME?'))

print(PG.query('OUTP:GEN?'))

#PG.write("OUTP:GEN 0")
