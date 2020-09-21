import visa
import serial #il faut installer le module pySerial mais importer serial ....
import time


ser = serial.Serial("COM6", 115200, timeout=1) 

def basique() :
	if ser.isOpen():    # make sure port is open     
		print(ser.name + ' open...')    # tell the user we are starting 
		ser.write(b'*IDN?\n')
		myResponse = ser.readline()    # read the response
		print(b'Device Info: ' + myResponse) # print the unit information
		time.sleep(0.1) #Ca fait office de *WAI
		ser.write(b'FREQ:CW 2801MHZ\n') 
		time.sleep(0.1)
		ser.write(b'POWER 10\n')  #dBm
		time.sleep(0.1)
		ser.write(b'OUTP:STAT ON\n')
		time.sleep(1)
		ser.write(b'OUTP:STAT OFF\n')
		time.sleep(0.1)

def test_ESR() :
	ser.write(b'ABORT\n')
	time.sleep(0.1) 
	ser.write(b'POWER 10\n')
	time.sleep(0.1) 
	ser.write(b'FREQ:START 2801MHZ\n')
	time.sleep(0.1)
	ser.write(b'FREQ:STOP 2950MHZ\n')
	time.sleep(0.1)
	ser.write(b'SWE:POINTS %i\n'%10)
	time.sleep(0.1)
	ser.write(b'INIT:CONT 1\n')
	time.sleep(0.1)
	ser.write(b'TRIG:STEP\n')
	time.sleep(0.1)
	ser.write(b'SWE:MODE SCAN\n')
	time.sleep(0.1)
	ser.write(b'OUTP:STAT ON\n')
	time.sleep(0.1)
	ser.write(b'INIT:IMM\n')
	time.sleep(1)
	ser.write(b'INIT:IMM\n')
	time.sleep(1)
	ser.write(b'INIT:IMM\n')
	time.sleep(1)
	ser.write(b'INIT:IMM\n')
	time.sleep(1)
	ser.write(b'ABORT\n')
	time.sleep(0.1) 
	ser.write(b'OUTP:STAT OFF\n')

test_ESR()
	



