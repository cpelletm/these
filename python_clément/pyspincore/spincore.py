#   pyspincore - A Python wrapper for Spin Core's PulseBlaster
#   Copyright (C) 2009  Hamid Ohadi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import spinapi
import string

class SpinCore:
    def __init__(self, board='PB24'):
        if spinapi.pb_init() is not 0:
            print "Error initializing board: " + spinapi.pb_get_error()

        if board is 'PB24':
            spinapi.pb_set_clock(80.0)

    def set_clock(self,clock):
        return spinapi.pb_set_clock(clock)

    def start(self):
        return spinapi.pb_start()

    def stop(self):
        return spinapi.pb_stop()

    def close(self):
        return spinapi.pb_close()

    def read_status(self):
        return spinapi.pb_read_status()

    def start_programming(self):
        return spinapi.pb_start_programming(0)

    def stop_programming(self):
        return spinapi.pb_stop_programming()

    def pulse(self,flags, inst, inst_data, length):
        return spinapi.pb_inst_pbonly(int(flags,2),inst, inst_data,length)

    def zero(self,flag='all'):
        self.stop()
        self.start_programming()

        if flag is 'all':
            self.pulse('0', CONTINUE, 0, 100*ms)
        else:
            self.pulse(flag, CONTINUE, 0, 100*ms)

        self.stop_programming()
        self.start()

    def one(self,flag='all'):
        self.stop()
        self.start_programming()

        if flag is 'all':
            self.pulse('11111111', CONTINUE, 0, 100*ms)
        else:
            self.pulse(flag, CONTINUE, 0, 100*ms)

        self.stop_programming()
        self.start()

CONTINUE = 0
STOP = 1
LOOP = 2
END_LOOP = 3
JSR = 4
RTS = 5
BRANCH = 6
LONG_DELAY = 7
WAIT = 8
RTI = 9

ns = 1.0
us = 1000.0
ms = 1000000.0
