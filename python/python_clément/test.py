import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.stream_readers
import nidaqmx.task
import nidaqmx.system
import time
import numpy as np
import matplotlib.pyplot as plt
def voltmetre():
    with nidaqmx.Task() as task :
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        V=task.read()
        print(V)



def signal_out():
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan('Dev1/ao0')
        out_stream=nidaqmx._task_modules.out_stream.OutStream(task)
        out=nidaqmx.stream_writers.AnalogSingleChannelWriter(out_stream,auto_start=True)
        task.timing.cfg_samp_clk_timing(10000,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
        signal=np.arange(0,3,0.1)
        signal[-1]=0
        out.write_many_sample(signal)
        time.sleep(10)
        

def digital2d_out():
    with nidaqmx.Task() as task:

        task.do_channels.add_do_chan('Dev1/port0/line1')
        task.do_channels.add_do_chan('Dev1/port0/line0')

        out_stream=nidaqmx._task_modules.out_stream.OutStream(task)
        out=nidaqmx.stream_writers.DigitalMultiChannelWriter(out_stream,auto_start=True)
        signal=np.zeros(100)
        for i in range(100) :
            if i%3==0 :
                signal[i]=1
        signal=np.uint8(signal)
        signal2=1-signal
        signal2d=np.vstack((signal,signal2))
        for i in range(100) :
            out.write_many_sample_port_byte(signal2d)

def digital_out():
    with nidaqmx.Task() as task:

        task.do_channels.add_do_chan('Dev1/port0/line0')       
        task.timing.cfg_samp_clk_timing(100,sample_mode=nidaqmx.constants.AcquisitionType.FINITE,samps_per_chan=200)
        signal=[True,False]*5
        task.write(signal)
        task.start()
        while not task.is_task_done() :
            pass

        
def do2() :
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan('Dev1/port0/line1')
        out_stream=nidaqmx._task_modules.out_stream.OutStream(task)
        task.timing.cfg_samp_clk_timing(10000,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
        signal=np.zeros(100)
        for i in range(len(signal)): 
            if i%2 == 0:
                signal[i]=1
        signal=np.float64(signal) 
        #print (signal[0].dtype)       
        task.write([False,True],auto_start=True)
        


def apd() :
    with nidaqmx.Task() as clock:
        with nidaqmx.Task() as trig:
            with nidaqmx.Task() as shutter :
                with nidaqmx.Task() as task:
                    clock.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=2000)
                    clock.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
                    clock.start()

                    trig.co_channels.add_co_pulse_chan_freq('Dev1/ctr2', freq=1)
                    trig.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
                    trig.start()

                    shutter.do_channels.add_do_chan('Dev1/port0/line0')
                    shutter.timing.cfg_samp_clk_timing(2000,sample_mode=nidaqmx.constants.AcquisitionType.FINITE,samps_per_chan=2000)
                    sw=nidaqmx.stream_writers.DigitalSingleChannelWriter(shutter.out_stream)
                    shutter.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/Ctr2InternalOutput')


                    shutter_out=[True]*500+[False]*1000+[True]*500


                    task.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')

                    #ci=nidaqmx._task_modules.channels.ci_channel.CIChannel(task._handle,'Dev1/ctr0')
                    #task.timing.cfg_samp_clk_timing(100000,source='/Dev1/100kHzTimebase',sample_mode=nidaqmx.constants.AcquisitionType.FINITE)
                    task.timing.cfg_samp_clk_timing(2000,source='/Dev1/Ctr1InternalOutput',sample_mode=nidaqmx.constants.AcquisitionType.FINITE,samps_per_chan=2000)
                    sr=nidaqmx.stream_readers.CounterReader(task.in_stream)
                    data=np.zeros(2000)
                    #print(ci.ci_count)

                    task.triggers.arm_start_trigger.dig_edge_src='/Dev1/Ctr2InternalOutput'
                    task.triggers.arm_start_trigger.trig_type=nidaqmx.constants.TriggerType.DIGITAL_EDGE

                    #sw.write_many_sample_port_uint32(shutter_out)
                    shutter.write(shutter_out)
                    
                    
                    shutter.start()
                    sr.read_many_sample_double(data,number_of_samples_per_channel=2000)


                    
                    
                    
                    return(data)

            

            
            #print(ci.ci_count)
            
def apd_loop():
    data=np.zeros(2000)
    for i in range(50):
        data=data+apd()

    #plt.plot(data[2:2000]-2*data[1:1999]+data[0:1998])
    plt.plot(data[2:2000]-data[0:1998])
    plt.show()

def sample_clock() :
    with nidaqmx.Task() as task:
        task.co_channels.add_co_pulse_chan_freq('Dev1/ctr1', freq=100000.0, idle_state=nidaqmx.constants.Level.LOW, duty_cycle=0.5)
        task.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)


        co=nidaqmx._task_modules.channels.co_channel.COChannel(task._handle,'Dev1/ctr1')

        
        task.start()
        #print(ci.ci_count)
        time.sleep(3)
        #print(ci.ci_count)

        

def test_sample_clock() :
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan('Dev1/port2/line4')
        task.write(True)
        task.start()

def device() :
    ni=nidaqmx.system.device.Device('Dev1')
    print(ni.ci_physical_chans.channel_names)
    print(ni.ci_samp_clk_supported)
    print(ni.terminals)

def trigger() :
    with nidaqmx.Task() as trig:
        with nidaqmx.Task() as task:
            trig.co_channels.add_co_pulse_chan_freq('Dev1/ctr2', freq=0.2)
            trig.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)


            trig.start()
            task.do_channels.add_do_chan('Dev1/port0/line0')
            task.timing.cfg_samp_clk_timing(1,sample_mode=nidaqmx.constants.AcquisitionType.FINITE,samps_per_chan=2)
            task.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/Ctr2InternalOutput')
            task.write([True,False])
            task.start()
            while not task.is_task_done() :
                pass



def open_shutter():
    with nidaqmx.Task() as shutter:
        shutter.do_channels.add_do_chan('Dev1/port0/line0')
        shutter.timing.cfg_samp_clk_timing(100,sample_mode=nidaqmx.constants.AcquisitionType.FINITE,samps_per_chan=400)
        #sw=nidaqmx.stream_writers.DigitalSingleChannelWriter(shutter.out_stream)
        shutter_out=[False]*100+[True]*200+[False]*100
        #print(shutter_out)
        #sw.write_many_sample_port_uint32(shutter_out)
        shutter.write(shutter_out)
        shutter.start()
        while not shutter.is_task_done() :
            pass



def trigger_digital_input():
    with nidaqmx.Task() as read :
        with nidaqmx.Task() as write :
            write.do_channels.add_do_chan('Dev1/port0/line3')
            read.di_channels.add_di_chan('Dev1/port0/line4')

            write.timing.cfg_samp_clk_timing(1000,sample_mode=nidaqmx.constants.AcquisitionType.FINITE,samps_per_chan=400)
            read.timing.cfg_samp_clk_timing(1000,sample_mode=nidaqmx.constants.AcquisitionType.FINITE,samps_per_chan=400)

            signal=[False]*100+[True]*200+[False]*100

            write.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/di/StartTrigger')
            #read.triggers.start_trigger.cfg_dig_edge_start_trig('Dev1/port0/line5')

            

            write.write(signal)

            write.start()

            
            data=read.read(nidaqmx.constants.READ_ALL_AVAILABLE)
            time.sleep(2)

            

                
            #read.start()


            plt.plot(data)
            plt.show()

def trigger_counter_input(): #non fonctionnel
    with nidaqmx.Task() as counter :
        with nidaqmx.Task() as read :
            with nidaqmx.Task() as write :
                write.do_channels.add_do_chan('Dev1/port0/line3')
                read.di_channels.add_di_chan('Dev1/port0/line4')
                counter.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')

                write.timing.cfg_samp_clk_timing(1000,sample_mode=nidaqmx.constants.AcquisitionType.FINITE,samps_per_chan=400)
                read.timing.cfg_samp_clk_timing(1000,sample_mode=nidaqmx.constants.AcquisitionType.FINITE,samps_per_chan=400)
                

                signal=[False]*100+[True]*200+[False]*100

                write.triggers.start_trigger.cfg_dig_edge_start_trig('/Dev1/di/StartTrigger')

                

                write.write(signal)

                write.start()

                data=read.read(nidaqmx.constants.READ_ALL_AVAILABLE)
                time.sleep(2)

                

                    

                plt.plot(data)
                plt.show() 

def test_frequenecy_measurement():
    with nidaqmx.Task() as ctf :
        ctf.ci_channels.add_ci_freq_chan('Dev1/ctr0')
        #ctf.ci_channels.add_ci_count_edges_chan('Dev1/ctr0')
        #ctf.timing.cfg_implicit_timing(sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
        ctf.start()
        print (ctf.read(10))


def writing_file():
    with open("toto.csv", "w") as file:
        a=[1,2,3]
        file.write(str(a))

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def servo():
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan('Dev1/ao1')
        angle=20
        tension=angle*5./180.
        task.write(tension)
        time.sleep(0.5)



servo()




 




