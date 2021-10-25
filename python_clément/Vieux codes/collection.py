import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.task
import nidaqmx.system



#print(nidaqmx.system._collections.physical_channel_collection.COPhysicalChannelCollection('Dev1').channel_names)

#print(nidaqmx.system._collections.physical_channel_collection.DOLinesCollection('Dev1').channel_names)

print(nidaqmx.system.device.Device('Dev1').terminals)
print(nidaqmx.system.device.Device('Dev1').anlg_trig_supported)
#print(nidaqmx.system.device.Device('Dev1').ci_trig_usage)





