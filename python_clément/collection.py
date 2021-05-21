import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.task
import nidaqmx.system
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt



#print(nidaqmx.system._collections.physical_channel_collection.COPhysicalChannelCollection('Dev1').channel_names)

#print(nidaqmx.system._collections.physical_channel_collection.DOLinesCollection('Dev1').channel_names)

print(nidaqmx.system.device.Device('Dev1').terminals)
#print(nidaqmx.system.device.Device('Dev1').ci_trig_usage)


# fig,ax=plt.subplots()
# print(dir(ax))
# x=range(100)
# ax.plot(x,x)
# ax.plot(x,x)
# lines=ax.get_lines()
# print(dir(lines[0]))
# for line in lines :
# 	line.remove()
# plt.show()


