# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 08:15:45 2022

@author: robin
"""

# PLOTS MEAN AND COMPARES INSTANTANEOUS FLUCTUATIONS FOR DIFFERENT FILES

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

A1_conf='R24_only';A1_mean=np.loadtxt('profile_6.969_R24_500.txt');A1_u=np.loadtxt('uflc_6.9694_R24_500.txt');

A2_conf='R24+R180_30mm ds';A2_mean=np.loadtxt('profile_8.839_R24_DS30MM_500.txt');A2_u=np.loadtxt('uflc_8.8393_R24_DS30MM_500.txt');

# Uinf and Rms
A1_Uinf=np.mean(A1_mean[-5:,1]);
A2_Uinf=np.mean(A2_mean[-5:,1]);




%matplotlib qt



fig=plt.figure(1)
gs=GridSpec(2,2) 
plt.rcParams['font.size'] = '25'

ax1=fig.add_subplot(gs[0,0])
plt.plot(A1_mean[:,0],A1_mean[:,2]/A1_Uinf,'ok')
plt.plot(A2_mean[:,0],A2_mean[:,2]/A2_Uinf,'or')
plt.xlabel('y(mm)');
plt.ylabel('u$_{rms}$/U$_{\infty}$');
ax1.legend([A1_conf+'  :U='+str(np.round(A1_Uinf,3))+ ' m/s',A2_conf+'  :U='+str(np.round(A2_Uinf,3))+ ' m/s'],frameon=False)
plt.xlim(-1,10);
plt.grid()

ax2=fig.add_subplot(gs[1,0])
plt.plot(A1_mean[:,0],A1_mean[:,1]/A1_Uinf,'ok')
plt.plot(A2_mean[:,0],A2_mean[:,1]/A2_Uinf,'or')
plt.xlabel('y(mm)');
plt.ylabel('U/U$_{\infty}$');
ax2.legend([A1_conf+'  :U='+str(np.round(A1_Uinf,3))+ ' m/s',A2_conf+'  :U='+str(np.round(A2_Uinf,3))+ ' m/s'],frameon=False)
plt.xlim(-1,10);
plt.grid()

ax3=fig.add_subplot(gs[0,1])
plt.plot(A1_u[:,0],A1_u[:,1],'-b')
plt.xlabel('Time(s)');plt.ylabel('u(m/s)');
ax3.legend([A1_conf+'  :U='+str(np.round(A1_Uinf,3))+ ' m/s'],frameon=False)
plt.xlim(0,5);plt.ylim(-4,4)
plt.grid()


ax4=fig.add_subplot(gs[1,1])
plt.plot(A2_u[:,0],A2_u[:,1],'-b')
plt.xlabel('Time(s)');plt.ylabel('u(m/s)');
ax4.legend([A2_conf+'  :U='+str(np.round(A2_Uinf,3))+ ' m/s'],frameon=False)
plt.xlim(0,5);plt.ylim(-4,4)
plt.grid()