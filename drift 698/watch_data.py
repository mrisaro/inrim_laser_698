####################################################
######  PSD: DSP internal vs DAC phase comparison ##
####################################################
from numpy import *
import allantools
from datetime import datetime,timedelta
import julian # to find mjd
import pytz # to attribute timezone info to a date
cet = pytz.timezone('CET')
utc = pytz.timezone('UTC')
from scipy.interpolate import interp1d

# from scipy import signal
# from scipy.optimize import curve_fit

# from scipy.signal import butter, lfilter
# from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,mark_inset)
# from matplotlib.ticker import FuncFormatter

from matplotlib import pyplot as plt

def sec_since_start(s,tstart):
    s=s.decode('utf-8')
    date = datetime.strptime(s, "%y%m%d*%H%M%S.%f")
    Date = cet.localize(date)
    date_start =  datetime.strptime(tstart, "%y%m%d*%H%M%S.%f")
    Date_start = cet.localize(date_start)
    # Dateutc=Date.astimezone(pytz.timezone('UTC'))
    #round to integer seconds
    secondi=int(round(Date.second+1.e-6*Date.microsecond,0))
    Date=Date.replace(second=0,microsecond=0)
    Date=Date+timedelta(seconds=secondi)
    
    # mjdd=julian.to_jd(Dateutc,fmt='mjd')
    return (Date - Date_start).total_seconds()

sec_since_start=vectorize(sec_since_start)

file=[
   '201019_2_Frequ',
   '201020_1_Frequ',
   ]

gt=1.e0 # gate time in s
tstart ='201019*153000.0' # arbitrary origin
# plt.figure()
tarray=array([])
frarray=array([])
for f in file:
    data=genfromtxt(f+'.txt',delimiter=(17,22),dtype='|S17,f8',unpack=True,skip_header=10)
    kktime=data['f0']
    fr=data['f1']
    t=sec_since_start(kktime,tstart)
    incr=arange(0,len(fr),1)*gt
    tarray=concatenate((tarray,t))
    frarray=concatenate((frarray,fr))
 
plt.figure(1,figsize=(10,6))
plt.plot(tarray,frarray-59.590e6,color='blue')
plt.tick_params(axis='both',labelsize=16)
plt.xlabel('Time /s', fontsize=16)
plt.ylabel('( Frequency - 59590000 ) / Hz', fontsize=16)
plt.grid(linestyle='--')
plt.tight_layout()
plt.show()
savetxt(file[0]+'.csv', column_stack((tarray,frarray)),delimiter=',')


tmin=5000 #s
tmax=10000 #s

tsel=tarray[(tarray>tmin) & (tarray<tmax)]
frsel=frarray[(tarray>tmin) & (tarray<tmax)]
mask=(abs(diff(frsel))< 500.)
mask=mask  & roll(mask,1) & roll(mask,-1)
plt.plot(tsel[1:][mask],frsel[1:][mask]-59.590e6,color='red')

deglitch=interp1d(tsel[1:][mask],frsel[1:][mask])
frsel_deglitch=deglitch(tsel[1:])

plt.scatter(tsel[1:],frsel_deglitch-59.590e6,color='red')

tau,adev,inutile,inutile=allantools.oadev(frsel_deglitch/429e12,rate=1.,data_type='freq')
plt.figure()
plt.loglog(tau,adev)
plt.xlabel('Time /s', fontsize=26)
plt.ylabel('overlapping Allan deviation', fontsize=26)
plt.grid(True,'both')

