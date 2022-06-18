#####################LT2 acquiring data#####################

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
from tkinter import *
import time
###############################################################################
#Inputs
SR = 20000 #Sampling rate
AT = 1 #Sampling time
n = SR*AT #Number of samples to read
v = np.zeros(n) #Creating an array to store samples
pulse_freq = 12800 #12800 steps for 1mm linear motion
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

Y = np.loadtxt("C:\\Users\\Sai\\Desktop\\y.txt", dtype=float)
y = 0
for i in list(range(len(Y))):
    dy = Y[i]-y
    task_pulse = nidaqmx.Task() #task created for pulse generation for both X and Y motor
    task_dir = nidaqmx.Task() #task created for direction of both X and Y motor.
    tasky_ena = nidaqmx.Task() #task created for enabling the Y motor.
    task_signal = nidaqmx.Task() #task created for acquiring the signal.

    task_pulse.co_channels.add_co_pulse_chan_time("Dev2/ctr0", units=TimeUnits.SECONDS, high_time = 1/(2*pulse_freq), low_time = 1/(2*pulse_freq)) #Assigned channel for pulse generation for both X and Y motor
    task_dir.do_channels.add_do_chan("Dev2/port0/line2") #Assigned channel for direction of both X and Y motor.
    tasky_ena.do_channels.add_do_chan("Dev2/port0/line1") #Assigned Channel to enable the Y motor direction.
    task_signal.ai_channels.add_ai_voltage_chan("Dev2/ai0") #Assigned Channel to acquire the signal.
    if dy>0:
        pulse_count = int(dy*pulse_freq)
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
         
    time.sleep(5)
    task_signal.timing.cfg_samp_clk_timing(SR, source='', active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=n)
    task_signal.start()
    v = task_signal.read(number_of_samples_per_channel=n,timeout = 60)
    plt.plot(v)
    plt.show()
    task_signal.stop()
    task_signal.close()
    file = "C:\\Users\\Sai\\Desktop\\sai\\"+str(Y[i])+"mm.txt"
    np.savetxt(file, v)
    time.sleep(5)
    y = Y[i]
    print(str(y)+'mm')
