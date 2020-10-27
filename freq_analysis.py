#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 15:19:45 2020
Script to analyze laser 698 allan deviation
@author: matias
"""

#%% Import some libraries
import numpy as np
import matplotlib.pyplot as plt
import allantools
from datetime import datetime,timedelta
import julian # to find mjd
import pytz # to attribute timezone info to a date
cet = pytz.timezone('CET')
utc = pytz.timezone('UTC')
from scipy.interpolate import interp1d
import auxiliary as aux

# from scipy import signal
# from scipy.optimize import curve_fit

# from scipy.signal import butter, lfilter
# from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,mark_inset)
# from matplotlib.ticker import FuncFormatter


# begin the analysis
aux.sec_since_start=np.vectorize(aux.sec_since_start)

#
path = 'drift 698/'
file = ['201019_2_Frequ','201020_1_Frequ']

gt=1.e0 # gate time in s
tstart ='201019*153000.0' # arbitrary origin

# define some empty arrays
tarray=np.array([])
frarray=np.array([])

for f in file:
    f = path+f
    data=np.genfromtxt(f+'.txt',delimiter=(17,22),dtype='|S17,f8',unpack=True,
                    skip_header=10)
    
    kktime = data['f0']                     # Time data
    fr = data['f1']                         # Freq data
    t = aux.sec_since_start(kktime,tstart)        # current time respect to tstart        
    incr = np.arange(0,len(fr),1)*gt             # increment
    tarray = np.concatenate((tarray,t))          # add data to time array
    frarray = np.concatenate((frarray,fr))       # add data to freq array

np.savetxt(path+file[0]+'.csv', np.column_stack((tarray,frarray)),delimiter=',')
 
#%% Some plots
f0 = 59.590e6

# Frequency timeline.
fig = plt.figure(1,figsize=(10,6))
ax = fig.add_subplot(111)
ax.plot(tarray,frarray,color='C0')
ax.set_ylim(f0-5e6,f0+5e6)
# Zoom region 1
axins = ax.inset_axes([0.1, 0.62, 0.3, 0.3])
axins.plot(tarray,frarray,color='C0')
# sub region of the original image
x1, x2, y1, y2 = 5000, 10000, f0-4000, f0+2000
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
ax.indicate_inset_zoom(axins)
# zoom region 2
# Zoom region 1
axins1 = ax.inset_axes([0.1, 0.1, 0.3, 0.3])
axins1.plot(tarray,frarray,color='C0')
# sub region of the original image
x1, x2, y1, y2 = 5000, 28000, f0-10000, f0+10000
axins1.set_xlim(x1, x2)
axins1.set_ylim(y1, y2)
ax.indicate_inset_zoom(axins1)
# Data
ax.set_xlabel('Time /s', fontsize=16)
ax.set_ylabel('Frequency (Hz)', fontsize=16)
ax.grid(linestyle='--')
fig.tight_layout()

#%% Select a frequency range

tmin=5000 #s
tmax=10000 #s

tsel = tarray[(tarray>tmin) & (tarray<tmax)]
frsel = frarray[(tarray>tmin) & (tarray<tmax)]
mask = (abs(np.diff(frsel))< 500.)
mask = mask  & np.roll(mask,1) & np.roll(mask,-1)

plt.plot(tsel[1:][mask],frsel[1:][mask]-59.590e6,color='red')

deglitch=interp1d(tsel[1:][mask],frsel[1:][mask])
frsel_deglitch=deglitch(tsel[1:])

plt.scatter(tsel[1:],frsel_deglitch-59.590e6,color='red')

tau,adev,inutile,inutile=allantools.oadev(frsel_deglitch/429e12,rate=1.,
                                          data_type='freq')
fig = plt.figure(2,figsize=(10,6))
ax = fig.add_subplot(111)
ax.loglog(tau,adev,'-o',label='Laser 698',linewidth=2,markersize=8)
ax.loglog(tau,1.5e-13/tau,'--',linewidth=1,label=r'$\sigma_{t}\propto \tau^{-1}$')
ax.loglog(tau,2e-14*np.sqrt(tau),'--',linewidth=1,label=r'$\sigma_{t}\propto \tau^{1/2}$')
ax.loglog(tau,1.0e-15*tau,'--',linewidth=1,label=r'$\sigma_{t}\propto \tau$')
ax.set_ylim(4e-14,2.5e-12)
ax.set_xlabel(r'Time /s', fontsize=16)
ax.set_ylabel(r'Overlapping Allan deviation', fontsize=16)
ax.tick_params(labelsize=14)
ax.legend(fontsize=15)
ax.grid(True,'both',linestyle='--')
fig.tight_layout()




