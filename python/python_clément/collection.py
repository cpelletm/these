import nidaqmx
import nidaqmx.stream_writers
import nidaqmx.task
import nidaqmx.system
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


#print(nidaqmx.system._collections.physical_channel_collection.COPhysicalChannelCollection('Dev1').channel_names)

#print(nidaqmx.system._collections.physical_channel_collection.DOLinesCollection('Dev1').channel_names)
#print(nidaqmx.system.device.Device('Dev1').terminals)
