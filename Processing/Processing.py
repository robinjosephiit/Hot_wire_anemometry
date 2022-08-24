# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:14:48 2022

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
#Reading all files

with open('process_list.txt') as f:
    lines = f.readlines()
siz=np.shape(lines)[0]
print('Total profiles to be processed=',siz)
pmet=np.loadtxt('Cal.txt')
with open('Conf.txt') as y:
    Config = y.readlines()
for k in range(0,siz):
    print(k+1)
    temp=str(lines[k].replace("\\\\","\\"))
    file_path = temp.replace("\n","")
    file_dat = []
    file_all = os.listdir(file_path)
    for i in file_all:
        if i.endswith('.txt'):
            file_dat.append(i)
    file_dat = natsorted(file_dat)
    
    n=pmet[k,0];
    A = pmet[k,1]
    B = pmet[k,2]
    SR= int(pmet[k,3])
    time=int(pmet[k,4])   
    xloc=int(pmet[k,5])
    con=Config[k]
    y = np.zeros(len(file_dat))
    Vel = np.zeros(len(file_dat))
    E = np.zeros((SR*time,len(file_dat)))
    Time=np.arange(0,time,1/SR)
    U = np.zeros((SR*time,len(file_dat)))
    E_avg = np.zeros(len(file_dat))
    Vel_cal = np.zeros(len(file_dat))
    for i in list(range(len(file_all))):
        y[i]=float(file_dat[i].partition("m")[0])

#Opening files
    for i in list(range(len(Vel))):
        
        file_v = open(file_path+'\\'+file_dat[i],'r')
        g = file_v.readlines()
        # y[i] = float(g[1][15:])
        # Vel[i] = float(g[2][15:-1])
        file_e = np.loadtxt(file_path+'\\'+file_dat[i], dtype=float, skiprows=0)
        E[:,i] = (file_e[:])
        U[:,i] = (((E[:,i]**2)-A)/B)**(1/n)
        E_avg[i] = np.mean(E[:,i])
        Vel_cal[i] = (((E_avg[i]**2)-A)/B)**(1/n)

    print('Location=',xloc)
    Dim=np.shape(U)
    Samples=Dim[0]
    locations=Dim[1]

    Umean=np.zeros(locations)
    Urms=np.zeros(locations)
    Urmsp=np.zeros(locations)
    Urmsn=np.zeros(locations)
    Urms_filt=np.zeros(locations)
    Uflc=np.zeros((Samples,locations))
    Uflc_filt=np.zeros((Samples,locations))
    Uflc_filtp=np.zeros((Samples,locations))
    Uflc_filtn=np.zeros((Samples,locations))
    for i in range(0,locations):
        Umean[i]=np.mean(U[:,i])
        Uflc[:,i]=U[:,i]-Umean[i]
    Uinf=np.mean(Umean[-5:])




#High pass filtering

    fc = 1  # Cut-off frequency of the filter
    w = fc / (SR / 2) # Normalize the frequency
    order =4
    bb, aa = signal.butter(order, w, 'high')

    for i in range(0,locations):
        Uflc_filt[:,i] = signal.filtfilt(bb, aa, Uflc[:,i])

    for i in range(0,locations):
        Urms_filt[i]=np.std(Uflc_filt[:,i])
        Urms[i]=np.std(Uflc[:,i])
    
    
   
#Calculating integral parameters: Adding zero to the array first
    y_corr = np.insert(y,0,0,axis=0)
    Vel = np.insert(Umean,0,0,axis=0)
    Urms=np.insert(Urms,0,0,axis=0)
    Urms_filt=np.insert(Urms_filt,0,0,axis=0)
    Urmsp=np.insert(Urmsp,0,0,axis=0)
    Urmsn=np.insert(Urmsn,0,0,axis=0)
    U_norm=np.zeros(len(Vel))
    U_norm1=np.zeros(len(Vel))
    U_sub=np.zeros(len(Vel))
    U_norm = Vel/Uinf 
    U_norm1= Umean/Uinf
    U_norm1 = np.insert(U_norm1,0,0,axis=0)
    U_sub=1-U_norm
    disp_t=np.trapz(U_sub,y_corr)
    mom_t=np.trapz(np.multiply(U_norm,U_sub),y_corr)
    H=disp_t/mom_t
    # print('displacement thickness=',disp_t)
    
    for i in range(1,30):
        if U_norm1[i]>0.99:
            break
    
    f=np.zeros((Samples,locations))
    P=np.zeros((Samples,locations))

 




    plt.figure(1)
    plt.plot(y_corr/disp_t,U_norm,'-o')
    plt.xlabel('y/$\delta$',fontsize=18)
    plt.ylabel('U/U$_\infty$',fontsize=18)

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.grid()
    

    
    plt.figure(2)
    plt.plot(y_corr/disp_t,Urms_filt*100/Uinf,'-o')
    plt.xlabel('y/$\delta$*',fontsize=18)
    plt.ylabel('(Urms/U$_\infty)*100$',fontsize=18)
    plt.legend(['Urms'])
    plt.xlim((-1,10))

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.grid()



#     plt.figure(4)   
#     plt.subplot(5,1,1)
#     plt.plot(Time,Uflc_filt[:,0])
#     plt.title('Wall');plt.xlim(0,3);plt.ylim(-1,2)
#     plt.subplot(5,1,2)
#     plt.plot(Time,Uflc_filt[:,4])
#     plt.title('Close to Wall');plt.xlim(0,3);plt.ylim(-1,2)
#     plt.subplot(5,1,3)
#     plt.plot(Time,Uflc_filt[:,9])
#     plt.title('Medium height from Wall');plt.xlim(0,3);plt.ylim(-1,2)
#     plt.subplot(5,1,4)
#     plt.plot(Time,Uflc_filt[:,19])
#     plt.title('Away from Wall');plt.xlim(0,3);plt.ylim(-1,2)
#     plt.subplot(5,1,5)
#     plt.plot(Time,Uflc_filt[:,25])
#     plt.title('Freestream');plt.xlim(0,3);plt.ylim(-1,2)

    loc=np.argmax(Urms_filt,axis=0)
    
    umaxinst=np.zeros((SR*time,4))
    umaxinst[:,0]=Time
    umaxinst[:,1]=Uflc_filt[:,loc]
    umaxinst[:,2]=Uflc_filt[:,0]
    umaxinst[:,3]=Uflc_filt[:,-1]
    
    
    a=str(Uinf)
    np.savetxt('uflc_' + a[0:6] + '_'+str(con[:-1])+'_'+str(xloc)+'.txt',umaxinst,delimiter =' ')
    profile=np.zeros((len(U_norm),3))
    profile[:,0]=y_corr
    profile[:,1]=U_norm*Uinf
    profile[:,2]=Urms_filt

    np.savetxt('profile_' + a[0:5] + '_'+str(con[:-1])+'_'+str(xloc)+'.txt',profile,delimiter =' ')
    print('Time elapsed=',tp.process_time() - start)
