# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 12:57:57 2022

@author: Sai
"""


#####################LT2 Calibration data#####################

###############################################################################
#Importing libraries
import nidaqmx
from nidaqmx.stream_writers import CounterWriter
from nidaqmx.constants import *
import math
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType
import numpy as np
import matplotlib.pyplot as plt
###############################################################################
#Inputs
SR = 20000 #Sampling rate
AT = 5 #Sampling time
n = SR*AT #Number of samples to read
v = np.zeros(n) #Creating an array to store samples
Vel = 11.22
file = "C:\\Users\\Sai\\Desktop\\sai\\"+str(Vel)+"_mpersec.txt"
###############################################################################
# #Assigning NI DAQ channels
# task_pulse = nidaqmx.Task() #task created for pulse generation for both X and Y motor
# task_dir = nidaqmx.Task() #task created for direction of both X and Y motor.
# tasky_ena = nidaqmx.Task() #task created for enabling the Y motor.
# task_signal = nidaqmx.Task() #task created for acquiring the signal.

# task_pulse.co_channels.add_co_pulse_chan_time("Dev2/ctr0", units=TimeUnits.SECONDS, high_time = 1/(2*pulse_freq), low_time = 1/(2*pulse_freq)) #Assigned channel for pulse generation for both X and Y motor
# task_dir.do_channels.add_do_chan("Dev2/port0/line2") #Assigned channel for direction of both X and Y motor.
# tasky_ena.do_channels.add_do_chan("Dev2/port0/line1") #Assigned Channel to enable the Y motor direction.
# task_signal.ai_channels.add_ai_voltage_chan("Dev2/ai0") #Assigned Channel to acquire the signal.
###############################################################################
task_signal = nidaqmx.Task() #task created for acquiring the signal.


task_signal.ai_channels.add_ai_voltage_chan("Dev2/ai0") #Assigned Channel to acquire the signal.


task_signal.timing.cfg_samp_clk_timing(SR, source='', active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=n)
task_signal.start()
v = task_signal.read(number_of_samples_per_channel=n,timeout = 60)
plt.plot(v)
plt.show()
task_signal.stop()
task_signal.close()
np.savetxt(file, v)

