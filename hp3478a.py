#!/usr/bin/env python

# Python Imports
import sys
import math
from datetime import datetime
import time

# Python Imports
import prologix_usb
from pylt import PyltError

class hp3478a(prologix_usb.gpib_dev):
    '''Class for talking to HP 3478A bench multimeters'''
	
    def __init__(self, name = "COM3", adr = 23):
        prologix_usb.gpib_dev.__init__(self, name, adr)
        self.id = "HP3478A"
        self.attr("read_tmo_ms", 2000)
        self.attr("rd_mode", "eoi")
        self.attr("eos", 0)
        self.attr("eoi", 1)

    def read_dc_volts(self, ndig=5, nsamples=1):
        print("Measuring %d samples of DC volts at %d.5 digits" % (nsamples, ndig))
        if ndig < 3 or ndig > 5:
            raise PyltError(self.id, "Invalid number of digits (must be 3, 4 or 5")

    def read_ac_volts(self, ndig=5, nsamples=1, dbg=False):
        '''Perform measurements of AC volts. Auto-ranging and auto-zero is turned on.
        The number of digits [ndig, default=5] can be specified as 3, 4 or 5 (equivalent to 3 1/2, 4 1/2 or
        5 1/2 digit display) and the number of samples [nsamples, default=1] can be specified.
        A list of tuples of the UTC date/time and the readings is returned.'''

        print("Measuring %d samples of AC volts at %d.5 digits" % (nsamples, ndig))
        if ndig < 3 or ndig > 5:
            raise PyltError(self.id, "Invalid number of digits (must be 3, 4 or 5")
        # Set command string for AC volts (F2), auto-range (RA), number of digits (N<ndig>), 
        # single trigger (T1), autozero on (Z1)
        command = "F2RAN%dT1Z1" % ndig
        self.wr(command)
        samples = 0
        readings = []
        count = max(nsamples/30,1)
        while samples < nsamples:
            t1 = time.time()
            time_of_read = datetime.utcnow()
            reading = self.rd()
            t2 = time.time()
            time_string = datetime.strftime(time_of_read, "%Y-%m-%d %H:%M:%S.%f")
            if dbg: print("Reading took %5.3f s" % (t2-t1,))
            if (samples % count==0):
                print("Taken %d samples" % samples)
            readings.append((time_of_read, float(reading)))
            samples += 1
        print("Taken %d samples" % samples)
        return readings

if __name__ == "__main__":
	d=hp3478a()
	d.wr("D2HI FROM PYLT")
	print("Device has no ID function")

doc="""
Functions:
----------
	H0 HOME Command. Place into DC volts, autorange, trigger hold 4.5 digits, autozero on.
    H1 Measure DC Volts. As above but a single measure is triggered and reported.
"""
    