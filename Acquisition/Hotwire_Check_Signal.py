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
n = SR*1 #Number of samples to read
v = np.zeros(n) #Creating an array to store samples
E = np.zeros(n) 
U= np.zeros(n) 
A = 1.79563355
B=  0.82300445
NN= 0.46
###############################################################################
#Creating a loop to see realtime signal
plt.figure(1)
while True:
    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    task.timing.cfg_samp_clk_timing(SR, source='', active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=n)
    task.start()
    v = task.read(number_of_samples_per_channel=n,timeout = 60)
    E=np.array(v)
    U=((E**2 - A)/B)**(1/NN)
    plt.plot(U, linewidth=0.4)
    Um=np.mean(U);Urms=np.std(U-Um);
    plt.legend(['Um=  '+str(np.round(Um,2))+'  '+'urms=  '+str(np.round(Urms,5))])
    plt.show()
    plt.grid(True)
    plt.ylim([0, 8])
    task.stop
    task.close()
###############################################################################
print('Completed')
