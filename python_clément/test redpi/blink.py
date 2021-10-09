import sys
import time
import redpitaya_scpi as scpi

print (sys.argv)
rp_ip='129.199.115.243'
rp_s = scpi.scpi(rp_ip)

if (len(sys.argv) > 2):
	led = int(sys.argv[2])
else:
	led = 0

print ("Blinking LED["+str(led)+"]")

period = 1 # seconds
time_start=time.time()
while time.time() < time_start +10:
    time.sleep(period/2.0)
    rp_s.tx_txt('DIG:PIN LED' + str(led) + ',' + str(1))
    time.sleep(period/2.0)
    rp_s.tx_txt('DIG:PIN LED' + str(led) + ',' + str(0))