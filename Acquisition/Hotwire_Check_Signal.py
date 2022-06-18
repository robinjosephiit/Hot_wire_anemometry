# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 19:31:43 2022

@author: Sai
"""

#############Checking signals###########################

###############################################################################
#Importing libraries
import nidaqmx
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType
import numpy as np
import matplotlib.pyplot as plt
###############################################################################
#Inputs
SR = 20000 #Sampling rate
n = SR #Number of samples to read
v = np.zeros(n) #Creating an array to store samples
###############################################################################
#Creating a loop to see realtime signal
plt.figure(1)
while True:
    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan("Dev2/ai2")
    task.timing.cfg_samp_clk_timing(SR, source='', active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=n)
    task.start()
    v = task.read(number_of_samples_per_channel=n,timeout = 60)
    plt.plot(v, linewidth=0.4)
    plt.show()
    plt.grid(True)
    # plt.ylim([1.4, 1.75])
    task.stop
    task.close()
###############################################################################
print('Completed')
