from spinapi import *
import platform
import time

print(platform.architecture())
# Enable the log file
pb_set_debug(1)

print("Copyright (c) 2015 SpinCore Technologies, Inc.");
print("Using SpinAPI Library version %s" % pb_get_version())
print("Found %d boards in the system.\n" % pb_count_boards())
 
print("This example program tests the TTL outputs of the PBDDS-II.\n\n");
print("All parameters related to the analog outputs are set to zero. "\
      "The main pulse program will generate a pulse train with all Flag "\
      "Bits High for 10 us and then LOW for 20 us.\n"); 
 

pb_select_board(0)


if pb_init() != 0:
	print("Error initializing board: %s" % pb_get_error())
	input("Please press a key to continue.")
	exit(-1)
pb_reset()

# Configure the core clock
pb_core_clock(75.0)

# Program the pulse program
pb_start_programming(PULSE_PROGRAM)
start = pb_inst_dds2(0,0,0,0,0,0,0,0,0,0, 0xfff, CONTINUE, 0, 20.0*us)
pb_inst_dds2(0,0,0,0,0,0,0,0,0,0, 0x0, 
	BRANCH, start, 20.0 * us)
pb_stop_programming()

# Trigger the board
pb_start()
print("Continuing will stop program execution\n");
time.sleep(5)
pb_stop()

pb_close()
