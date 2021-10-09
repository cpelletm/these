from pyrpl import RedPitaya,Pyrpl
from time import sleep
import matplotlib.pyplot as plt

HOSTNAME = '129.199.115.243'
p = Pyrpl('test')
r=p.rp
asg = r.asg1
s = r.scope

s.setup(duration=0.05,trigger_delay=0.,input1='in1',ch1_active=True,ch2_active=True,rolling_mode=True,trace_average=1,running_state="stopped")
dt=8*1e-9*s.decimation
n=2**14

s.single()
curves=s.save_curve() #Quand tu utilises single (et tu devrais), il ne garde que le dernier call de s.single() (enfin j'espère)
plt.plot(curves[0].data[0],curves[0].data[1])
print(len(curves[0].data[0]))
plt.show()