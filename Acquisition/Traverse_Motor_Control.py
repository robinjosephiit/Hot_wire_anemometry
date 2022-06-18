# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 12:29:17 2022

@author: Sai
"""

#####################LT2 Traverse motor control#####################

###############################################################################
#Importing libraries
import nidaqmx
from nidaqmx.stream_writers import CounterWriter
from nidaqmx.constants import *
import math
###############################################################################
#inputs
X = 0 #in mm +ve if front -ve is back
Y = 0 #in mm +ve is up -ve is down
pulse_freq = 12800 #12800 steps for 1mm linear motion
###############################################################################
#Assigning NI DAQ channels
task_pulse = nidaqmx.Task() #task created for pulse generation for both X and Y motor
task_dir = nidaqmx.Task() #task created for direction of both X and Y motor.
taskx_ena = nidaqmx.Task() #task created for enabling the X motor.
tasky_ena = nidaqmx.Task() #task created for enabling the Y motor.

task_pulse.co_channels.add_co_pulse_chan_time("Dev2/ctr0", units=TimeUnits.SECONDS, high_time = 1/(2*pulse_freq), low_time = 1/(2*pulse_freq)) #Assigned channel for pulse generation for both X and Y motor
task_dir.do_channels.add_do_chan("Dev2/port0/line2") #Assigned channel for direction of both X and Y motor.
taskx_ena.do_channels.add_do_chan("Dev2/port0/line0") #Assigned Channel to enable the X motor direction.
tasky_ena.do_channels.add_do_chan("Dev2/port0/line1") #Assigned Channel to enable the Y motor direction.
###############################################################################
#Moving motors
x = X
if x>0:
    pulse_count = int(x*pulse_freq)
    task_pulse.timing.cfg_implicit_timing(sample_mode=AcquisitionType.FINITE, samps_per_chan=pulse_count)
    task_dir.start()
    taskx_ena.start()
    taskx_ena.write(True)
    task_dir.write(True)
    task_pulse.start()
    task_pulse.wait_until_done(timeout = math.inf)
    task_pulse.stop()
    task_dir.write(False)
    taskx_ena.write(False)
    task_dir.stop()
    taskx_ena.stop()
    task_pulse.close()
    task_dir.close()
    taskx_ena.close()
if x<0:
    pulse_count = int(-x*pulse_freq)
    task_pulse.timing.cfg_implicit_timing(sample_mode=AcquisitionType.FINITE, samps_per_chan=pulse_count)
    task_dir.start()
    taskx_ena.start()
    taskx_ena.write(True)
    task_dir.write(False)
    task_pulse.start()
    task_pulse.wait_until_done(timeout = math.inf)
    task_pulse.stop()
    task_dir.write(False)
    taskx_ena.write(False)
    task_dir.stop()
    taskx_ena.stop()
    task_pulse.close()
    task_dir.close()
    taskx_ena.close()
y = Y
if y>0:
    pulse_count = int(y*pulse_freq)
    task_pulse.timing.cfg_implicit_timing(sample_mode=AcquisitionType.FINITE, samps_per_chan=pulse_count)
    task_dir.start()
    tasky_ena.start()
    tasky_ena.write(True)
    task_dir.write(True)
    task_pulse.start()
    task_pulse.wait_until_done(timeout = math.inf)
    task_pulse.stop()
    task_dir.write(False)
    tasky_ena.write(False)
    # task_dir.stop()
    # tasky_ena.stop()
    task_pulse.close()
    task_dir.close()
    tasky_ena.close()
if y<0:
    pulse_count = int(-y*pulse_freq)
    task_pulse.timing.cfg_implicit_timing(sample_mode=AcquisitionType.FINITE, samps_per_chan=pulse_count)
    task_dir.start()
    tasky_ena.start()
    tasky_ena.write(True)
    task_dir.write(False)
    task_pulse.start()
    task_pulse.wait_until_done(timeout = math.inf)
    task_pulse.stop()
    task_dir.write(False)
    tasky_ena.write(False)
    task_dir.stop()
    tasky_ena.stop()
    task_pulse.close()
    task_dir.close()
    tasky_ena.close()
###############################################################################
#Closing every channel
if x==0 and y==0:
    task_dir.start()
    taskx_ena.start()
    tasky_ena.start()
    task_dir.write(False)
    taskx_ena.write(False)
    tasky_ena.write(False)
    tasky_ena.stop()
    taskx_ena.stop()
    task_dir.stop()
    tasky_ena.close()
    taskx_ena.close()
    task_dir.close()