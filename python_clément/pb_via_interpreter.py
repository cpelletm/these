import os
from subprocess import call, Popen, check_output
import time



check_output('spbicl load pb_instructions.txt 500.0')
check_output('spbicl start')
time.sleep(5)
check_output('spbicl stop')

# check_output ca marche, on va pas chercher plus loin
# subprocess.call("spbicl load consigne_pb.txt 100.0", shell=False) #J'ai pas vu de diff avec os.system