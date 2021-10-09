from pyrpl import RedPitaya,Pyrpl
import time
import sys
sys.path.append('D:\\These Clément\\these\\python_clément')
import lab
import matplotlib.pyplot as plt

HOSTNAME = '129.199.115.243' #rp-levitation
# HOSTNAME = '129.199.114.192' #redpitaya3
# p = Pyrpl(hostname=HOSTNAME) #pyrpl instance
p=Pyrpl('test')
r=p.rp #redpitaya instance
s=r.scope #scope instance
s.average=True

#input sources : 'in1/2', 'out1/2', 'iq0/1/2/2_2', 'pid0/1/2', 'asg0/1', 'trig', 'lir' (?), 'off'
#potential trigger sources : "off", "immediately", "ch1_positive_edge" (ch1/2 et positive/negative), "ext_positive_edge" (pos/neg, c'est la pin DIO0P), "asg0", "asg1", "dsp" (le trigger du module dsp)
#trigger delay in s ? can be positive or negative

s.setup(duration=0.05,trigger_delay=0.,input1='in1',ch1_active=True,ch2_active=True,rolling_mode=True,trace_average=1,running_state="stopped")

#duration : il prend la puissance de 2 la plus proche qui permette de mesurer sur toute la duration (et plus)
#decimation : la redpi fait une mesure toutes les 8 ns et renvoie 2^14 (~16 000) points. Tu peux décider que chaque point moyenne sur s.decimation (équivalent nAvg chez moi)
dt=8*1e-9*s.decimation
n=2**14

s.single()

#le pb de save_curve, bah c'est qu'il save la curve (en .dat illisible en plus)
# curves=s.save_curve() #Quand tu utilises single (et tu devrais), il ne garde que le dernier call de s.single() (enfin j'espère)
# x=curves[0].data[0] #curves[i] : ch1 et ch2, data[i] : x et y
# y=curves[0].data[1]

x=s._run_future.data_x
y=s._run_future.data_avg[0]

# x=lab.average(x,2**6)
# y=lab.average(y,2**6)
plt.plot(x,y)

plt.show()
