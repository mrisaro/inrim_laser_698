#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 15:22:35 2020
Auxiliary functions to the data analysis
@author: matias
"""
from datetime import datetime,timedelta
import pytz # to attribute timezone info to a date
cet = pytz.timezone('CET')
utc = pytz.timezone('UTC')

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
