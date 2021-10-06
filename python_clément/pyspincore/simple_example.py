from spincore import *
import time
import signal
import sys

def signal_handler(signal, frame):
    print "Exiting..."
    PB.zero()
    PB.close()
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)


# Initialising the PulseBlaster
PB = SpinCore()

for i in range(50):
    PB.stop()
    PB.start_programming()

    PB.pulse('000',CONTINUE, 0, 1000*ms)
    PB.pulse('100',CONTINUE, 0, 0.3*ms)
    PB.pulse('001',CONTINUE, 0, 0.2*i*ms)
    PB.pulse('010',CONTINUE, 0, 1*ms)

    PB.pulse('0',CONTINUE, 0, 100*ms)
    PB.pulse('0',STOP, 0, 100*ms)
    PB.stop_programming()

    PB.start()
    time.sleep(10)

PB.close()
