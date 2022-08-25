# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 19:31:43 2022

@author: Robin
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
paramet=np.loadtxt('D:\Robin_24th_Aug\Calibration_1130am_25.02_deg\Constants.dat')
nn=paramet[0]
aa=paramet[1]
bb=paramet[2]
Uinf=2.88 # Make sure to correct Uinf here


SR = 40000 #Sampling rate
n = SR #Number of samples to read
E = np.zeros(n) #Creating an array to store samples
v = np.zeros(n) #Creating an array to store samples
###############################################################################
#Creating a loop to see realtime signal
plt.figure(1)
while True:
    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    task.timing.cfg_samp_clk_timing(SR, source='', active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=n)
    task.start()
    E = task.read(number_of_samples_per_channel=n,timeout = 60)
    for i in range(len(E)):
        v[i]=(((E[i]**2)-aa)/bb)**(1/nn)
    plt.plot(v, linewidth=0.4)
    temp=np.round((np.mean(v)),2)
    temp=str('U=')+str(temp)+str('  urms/U=')+str(np.round(np.std(v-np.mean(v))/Uinf,3))
    
    plt.legend([temp])
    plt.show()
    plt.grid(True)
    plt.ylim([2, 4])
    task.stop
    task.close()
    
###############################################################################
print('Completed')



    





