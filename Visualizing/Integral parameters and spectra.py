# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 09:05:52 2022

@author: robin
"""



import time as tp
start = tp.process_time()
import numpy as np
import os
from natsort import natsorted
import matplotlib.pyplot as plt
from scipy import signal
import math

from sklearn.linear_model import LinearRegression
siz=3
with open('address.txt') as f:
    lines = f.readlines()
    
temp=str(lines[0].replace("\\\\","\\"))
file_path = temp.replace("\n","")
file_dat = []
file_all = os.listdir(file_path)

for i in file_all:
    if i.endswith('.txt'):
        file_dat.append(i)
file_dat = natsorted(file_dat)
l=[[0 for j in range(8)]for i in range(len(file_dat))]

for i in list(range(len(file_dat))):
    print(i)
    file_e = np.loadtxt(file_path+'\\'+file_dat[i], dtype=float, skiprows=0)
    y=np.zeros(len(file_e))
    U=np.zeros(len(file_e))
    urms=np.zeros(len(file_e))
    y=file_e[:,0]
    U=file_e[:,1]
    Uinf=np.mean(U[-4:])
    urms=file_e[:,2]
    temp=np.polyfit(y[0:4],U[0:4],1)
    y=y+temp[1]/temp[0]
    y=np.insert(y,0,0,axis=0)
    U=np.insert(U,0,0,axis=0)
    urms=np.insert(urms,0,0,axis=0)
    l[i][7]=file_dat[i]
    l[i][0]=round(temp[1]/temp[0],3)
    l[i][1]=round(Uinf,3)
    l[i][2]=round(np.trapz(1-U/Uinf,y),3)
    l[i][3]=round(np.trapz(np.multiply(U/Uinf,(1-U/Uinf)),y),3)
    l[i][4]=round(l[i][2]/l[i][3],3)
    l[i][5]=round(y[np.searchsorted(U/Uinf,0.99,side='left')],3)
    l[i][6]=round(np.max(urms/Uinf),3)
    

with open('file.txt', 'w') as file:
    for row in l:
        file.write('\t'.join([str(item) for item in row]))
        file.write('\n')

plt.figure(1)
plt.plot(y/np.trapz(1-U/Uinf,y),U/Uinf,'-o')
plt.xlabel('y/$\delta*$')
plt.ylabel('U/U$_{\infty}$')
plt.xlim((0,10))

plt.figure(2)
plt.plot(y/np.trapz(1-U/Uinf,y),urms/Uinf,'-o')
plt.xlabel('y/$\delta*$')
plt.ylabel('u$_{rms}$/U$_{\infty}$')
plt.xlim((0,10))



import scipy
U_flc_filt=np.loadtxt('uflc_10.165_Clean_tunnel_500m_500.txt')
SR=20000
temp=len(U_flc_filt)
pow2=np.fix(math.log2(temp))
n_fft=2**(pow2-5)
PSD_max=scipy.signal.welch(U_flc_filt[:,1], fs=SR, window='hann', nperseg=n_fft/8, noverlap=None, nfft=n_fft)
PSD_wall=scipy.signal.welch(U_flc_filt[:,2], fs=SR, window='hann', nperseg=n_fft/8, noverlap=None, nfft=n_fft)
PSD_fs=scipy.signal.welch(U_flc_filt[:,3], fs=SR, window='hann', nperseg=n_fft/8, noverlap=None, nfft=n_fft)
  
f_wall=PSD_wall[0][:]            
p_wall=PSD_wall[1][:]

f_max=PSD_max[0][:]            
p_max=PSD_max[1][:]

f_fs=PSD_fs[0][:]            
p_fs=PSD_fs[1][:]

plt.figure(2)
plt.loglog(f_wall,p_wall)  
plt.loglog(f_max,p_max)  
plt.loglog(f_fs,p_fs)  
plt.xlabel('F(Hz)')
plt.ylabel('$\Phi_{uu}$')
plt.legend(['Wall','u$_{max}$','freestream'])

plt.figure(3)
plt.semilogx(f_wall,np.multiply(p_wall,f_wall))  
plt.semilogx(f_max,np.multiply(p_max,f_max))  
plt.semilogx(f_fs,np.multiply(p_fs,f_fs))  
plt.xlabel('F(Hz)')
plt.ylabel('F*$\Phi_uu$')
plt.legend(['Wall','u$_{max}$','freestream'])


