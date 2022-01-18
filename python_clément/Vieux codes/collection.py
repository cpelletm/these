import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.task
import nidaqmx.system

deviceCollection=nidaqmx.system._collections.device_collection.DeviceCollection()
print(deviceCollection.device_names)

# print(nidaqmx.system.device.Device('cDAQ1Mod1').product_type)

print(nidaqmx.system.device.Device('Dev1').product_type)


#print(nidaqmx.system._collections.physical_channel_collection.COPhysicalChannelCollection('Dev1').channel_names)

#print(nidaqmx.system._collections.physical_channel_collection.DOLinesCollection('Dev1').channel_names)





# print(nidaqmx.system._collections.physical_channel_collection.AOPhysicalChannelCollection('cDAQ1Mod1').channel_names)

# print(nidaqmx.system._collections.physical_channel_collection.AOPhysicalChannelCollection('cDAQ1Mod1').channel_names)


# print(nidaqmx.system.device.Device('Dev1').terminals)
# print(nidaqmx.system.device.Device('Dev1').anlg_trig_supported)
#print(nidaqmx.system.device.Device('Dev1').ci_trig_usage)





