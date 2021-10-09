import sys
import time
import random
import os
import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system

import numpy as np
import matplotlib.pyplot as plt

import visa

class Photon_Counter():
    def __init__(self):

        
        #Timing Parameter ##
        #The program aquires the total number of photons at a rate defined by real_sampling_rate, but will only display an average of it every dt

        self.unit=1e-5
        self.tecl=200
        self.twait=1000
        self.tread=200
        self.total_PL=False
        

        self.n_per_plot=int(1E5)
        self.voltage=np.arange(0.30,1.,0.02)
        self.tension=self.voltage[0]

        self.dossier="D:/DATA/20200219/scans_t_pola/"
        try :
            os.makedirs(self.dossier)
        except :
            pass
        


        resourceString4 = 'USB0::0x0AAD::0x0197::5601.3800k03-101213::INSTR'  # Pour avoir l'adresse je suis allé regarder le programme RsVisaTester de R&S dans "find ressource"
        rm = visa.ResourceManager()
        self.PG = rm.open_resource( resourceString4 )
        self.PG.write_termination = '\n'
        self.PG.clear()  # Clear instrument io buffers and status



    def update_canvas(self):       
        ##Update the plot and the value of the PL ##
        self.N_iter+=1

        self.sr.read_many_sample_double(self.data,number_of_samples_per_channel=len(self.data)) #read the N value during dt

      
        if self.total_PL :
            temp=self.data
        else :
            temp=self.data[self.tecl+self.twait:]
        temp=(temp[1:]-temp[:-1])*self.sampling_rate


        self.y=temp/self.N_iter+self.y*(1-1/self.N_iter)




    def start_measure(self):
        

        self.sampling_rate=1/self.unit

        
        self.N=self.tecl+self.twait+self.tread

        self.data=np.zeros(self.N)


        #Sample Clock creation (On counter1)

        self.sample_clock=nidaqmx.Task()
        self.sample_clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=self.sampling_rate)
        self.sample_clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) #Else the clock sends a single pulse
        self.sample_clock.start()


        
        self.signal=[True]*self.tecl+[False]*self.twait+[True]*self.tread

        if self.total_PL :
            self.y=np.zeros(self.N-1)
            self.t=np.linspace(0,(self.N-1)*self.unit,self.N-1)
        else :
            self.y=np.zeros(self.tread -1)
            self.t=np.linspace(0,(self.tread-1)*self.unit,self.tread-1)

        self.N_iter=0

        

        

        #Counter creation
        self.counter=nidaqmx.Task()
        self.counter.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        self.counter.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N)
        self.sr=nidaqmx.stream_readers.CounterReader(self.counter.in_stream)

        self.counter.triggers.arm_start_trigger.dig_edge_src='/Dev1/100kHzTimebase'
        self.counter.triggers.arm_start_trigger.trig_type=nidaqmx.constants.TriggerType.DIGITAL_EDGE


        
        
        #Pulse signal creation
        self.pulsed=nidaqmx.Task()
        self.pulsed.do_channels.add_do_chan('Dev1/port0/line0')
        self.pulsed.timing.cfg_samp_clk_timing(self.sampling_rate,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.N)

        self.pulsed.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/Ctr0ArmStartTrigger') 
        self.pulsed.write(self.signal)
        self.pulsed.start()

        
        

   
        for i in range(self.n_per_plot) :
            self.update_canvas()
            if i%100==0 :
                print(i)

        self.pulsed.close()
        self.counter.close()
        self.sample_clock.close()

        self.fname=self.dossier+"%3i.txt"%(int(self.tension*100))
        print(self.fname)
        with open(self.fname,'w') as f :
            for i in range(len(self.y)) :
                f.write("%5.4E \t %5.4E \n"%(self.t[i],self.y[i]))


    def set_tension(self,V):
        self.tension=V

        self.PG.write('OUTP:GEN 0')
        self.PG.write('*WAI')
        time.sleep(1)
        self.PG.write('INST 1')
        self.PG.write('*WAI')
        self.PG.write('VOLTage:RAMP ON')
        self.PG.write('*WAI')
        self.PG.write('VOLTage:EASYramp:TIME %f'% 1)#le temps est en secondes et j'arrive pas à faire 0.1 sec...
        self.PG.write('*WAI')
        self.PG.write('OUTP:SEL 1')
        self.PG.write('*WAI')
        self.PG.write('APPLY "%f,%f"' % (self.tension,1))
        self.PG.write('*WAI')        
        self.PG.write('OUTP:GEN 1')
        self.PG.write('*WAI')
        time.sleep(1.5)



foo=Photon_Counter()
for v in foo.voltage :
    foo.set_tension(v)
    foo.start_measure()