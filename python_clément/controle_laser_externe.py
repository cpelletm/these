from lab import *

las=pulsedLaserWidget(gate=True,gateChan='/Dev1/PFI0')
GUI=Graphical_interface(las,title='Ctrl laser ext',size='auto')
GUI.run()