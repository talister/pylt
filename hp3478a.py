#!/usr/bin/env python
# -*- coding: utf8 -*-

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

    def _setup_dmm(self, command, delay=3.0):
        '''Clear the adaptor, send the command, sleep for settling and throw 
        away the first 2 readings'''
        self.clear()
        self.wr(command)
        # Sleep to allow autorange to happen and throw first readings away
        time.sleep(delay)
        self.rd()
        self.rd()
        
        return
        
    def _take_samples(self, nsamples, dbg=False):
        samples = 0
        readings = []
        count = max(nsamples/30,1)
        while samples < nsamples:
            t1 = time.time()
            time_of_read = datetime.utcnow()
            reading = self.rd()
            t2 = time.time()
            time_string = datetime.strftime(time_of_read, "%Y-%m-%d %H:%M:%S.%f")
            if dbg: print("Reading took %5.3fs %f" % (t2-t1, float(reading)))
            if (samples % count==0):
                print("Taken %d samples" % samples)
            readings.append((time_of_read, float(reading)))
            samples += 1
        print("Taken %d samples" % samples)
        return readings

    def read_dc_volts(self, ndig=5, nsamples=1, dbg=False):
        '''Perform measurements of DC volts. Auto-ranging and auto-zero is turned on.
        The number of digits [ndig, default=5] can be specified as 3, 4 or 5 (equivalent to 3 1/2, 4 1/2 or
        5 1/2 digit display) and the number of samples [nsamples, default=1] can be specified.
        A list of tuples of the UTC date/time and the readings is returned.'''
    
        print("Measuring %d samples of DC volts at %d.5 digits" % (nsamples, ndig))
        if ndig < 3 or ndig > 5:
            raise PyltError(self.id, "Invalid number of digits (must be 3, 4 or 5")
        # Set command string for DC volts (F1), auto-range (RA), number of digits (N<ndig>), 
        # single trigger (T1), autozero on (Z1)
        command = "F1RAN%dT1Z1" % ndig
        self.wr(command)
        self._setup_dmm(command)

        # Take readings and return them
        readings = self._take_samples(nsamples, dbg)
        return readings

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
        self._setup_dmm(command)

        # Take readings and return them
        readings = self._take_samples(nsamples, dbg)
        return readings

    def read_2wire_ohms(self, ndig=5, nsamples=1, dbg=False):
        '''Perform measurements of 2-wire resistance. Auto-ranging and auto-zero is turned on.
        The number of digits [ndig, default=5] can be specified as 3, 4 or 5 (equivalent to 3 1/2, 4 1/2 or
        5 1/2 digit display) and the number of samples [nsamples, default=1] can be specified.
        A list of tuples of the UTC date/time and the readings is returned.'''

        print("Measuring %d samples of 2-wire resistance at %d.5 digits" % (nsamples, ndig))
        if ndig < 3 or ndig > 5:
            raise PyltError(self.id, "Invalid number of digits (must be 3, 4 or 5")
        # Set command string for 2-wire ohms (F3), auto-range (RA), number of digits (N<ndig>), 
        # single trigger (T1), autozero on (Z1)
        command = "F3RAN%dT1Z1" % ndig
        self._setup_dmm(command)

        # Take readings and return them
        readings = self._take_samples(nsamples, dbg)
        return readings

    def read_4wire_ohms(self, ndig=5, nsamples=1, dbg=False):
        '''Perform measurements of 4-wire resistance. Auto-ranging and auto-zero is turned on.
        The number of digits [ndig, default=5] can be specified as 3, 4 or 5 (equivalent to 3 1/2, 4 1/2 or
        5 1/2 digit display) and the number of samples [nsamples, default=1] can be specified.
        A list of tuples of the UTC date/time and the readings is returned.'''

        print("Measuring %d samples of 4-wire resistance at %d.5 digits" % (nsamples, ndig))
        if ndig < 3 or ndig > 5:
            raise PyltError(self.id, "Invalid number of digits (must be 3, 4 or 5")
        # Set command string for 4-wire resistance (F4), auto-range (RA), number of digits (N<ndig>), 
        # single trigger (T1), autozero on (Z1)
        command = "F4RAN%dT1Z1" % ndig
        self._setup_dmm(command)

        # Take readings and return them
        readings = self._take_samples(nsamples, dbg)
        return readings

    def read_dc_amps(self, ndig=5, nsamples=1, dbg=False):
        '''Perform measurements of DC amps. Auto-ranging and auto-zero is turned on.
        The number of digits [ndig, default=5] can be specified as 3, 4 or 5 (equivalent to 3 1/2, 4 1/2 or
        5 1/2 digit display) and the number of samples [nsamples, default=1] can be specified.
        A list of tuples of the UTC date/time and the readings is returned.'''
    
        print("Measuring %d samples of DC amps at %d.5 digits" % (nsamples, ndig))
        if ndig < 3 or ndig > 5:
            raise PyltError(self.id, "Invalid number of digits (must be 3, 4 or 5")
        # Set command string for DC amps (F5), auto-range (RA), number of digits (N<ndig>), 
        # single trigger (T1), autozero on (Z1)
        command = "F5RAN%dT1Z1" % ndig
        self._setup_dmm(command)

        # Take readings and return them
        readings = self._take_samples(nsamples, dbg)
        return readings

    def read_ac_amps(self, ndig=5, nsamples=1, dbg=False):
        '''Perform measurements of AC amps. Auto-ranging and auto-zero is turned on.
        The number of digits [ndig, default=5] can be specified as 3, 4 or 5 (equivalent to 3 1/2, 4 1/2 or
        5 1/2 digit display) and the number of samples [nsamples, default=1] can be specified.
        A list of tuples of the UTC date/time and the readings is returned.'''

        print("Measuring %d samples of AC amps at %d.5 digits" % (nsamples, ndig))
        if ndig < 3 or ndig > 5:
            raise PyltError(self.id, "Invalid number of digits (must be 3, 4 or 5")
        # Set command string for AC amps (F6), auto-range (RA), number of digits (N<ndig>), 
        # single trigger (T1), autozero on (Z1)
        command = "F6RAN%dT1Z1" % ndig
        self._setup_dmm(command, delay=3.0)

        # Take readings and return them
        readings = self._take_samples(nsamples, dbg)
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
    H2 Measure AC Volts. As H1, but AC voltage measurement is taken.
    H3 Measure 2-wire Ohms. As H1, but 2-wire resistance measurement is taken.
    H4 Measure 4-wire Ohms. As H1, but 4-wire resistance measurement is taken.
    H5 Measure DC Amps. As H1, but DC current measurement is taken.
    H6 Measure AC Amps. As H1, but AC current measurement is taken.
    H7 Measure Extended ohms. As H1, but extended resistance (>30 Mohms) measurement is taken.

    N{3,4,5} Select number of digits on display.
    T[1-5]   Select trigger mode:
                1: Internal trigger mode
                2: External trigger mode
                3: Single trigger mode
                4: Trigger hold mode
                5: Fast trigger (omit settling delay on AC volts and current and 2 highest ohm ranges)
    Z{0,1}   Autozero off/on
    D{1,3}   Display: 1: normal display, D2[text]: display [text] (12 chars max), 3: off

    Functions and ranges:
                                Range Codes
    Function  Code  R-2  R-1   R0 R1  R2   R3  R4   R5    R6  R7   RA
    DC Volts  F1    30mV 300mV 3V 30V 300V  +   +    +     +   +   Auto
    AC Volts  F1     *   300mV 3V 30V 300V  +   +    +     +   +   Auto
    2-W Ohms  F3     *     *   *  30Ω 300Ω 3kΩ 30kΩ 300kΩ 3MΩ 30MΩ Auto
    4-W Ohms  F4     *     *   *  30Ω 300Ω 3kΩ 30kΩ 300kΩ 3MΩ 30MΩ Auto
    DC Amps   F5     *   300mA 3A  +   +    +   +    +     +   +   Auto
    AC Amps   F5     *   300mA 3A  +   +    +   +    +     +   +   Auto
    ExtendedΩ F7
    * indicates code selects lowest (most sensitive) range
    + indicates code selects highest (least sensitive) range
"""

