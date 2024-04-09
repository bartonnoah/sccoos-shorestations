import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.colors as mcolors

stations = {'Scripps Pier': {'savename': 'SIO',
                             'data': '../data/SIO_TEMP_20230501.xls'}}

#Helper functions
c_to_f = lambda c: (c*(9/5)) + 32

def suffix(day):
    '''
    Gives the suffix to make day of month an ordinal number.
    
    Input: day (int [1,31])
    Output: suffix (str {'st', 'nd', 'rd', 'th'})
    '''
    updated_day = day
    if updated_day == 1:
        suffix = 'st'
    elif updated_day == 2:
        suffix = 'nd'
    elif updated_day == 3:
        suffix = 'rd'
    elif (4 <= updated_day <= 20):
        suffix = 'th'
    elif updated_day == 21:
        suffix = 'st'
    elif updated_day == 22:
        suffix = 'nd'
    elif updated_day == 23:
        suffix = 'rd'
    elif (24 <= updated_day <= 30):
        suffix = 'th'
    elif updated_day == 31:
        suffix = 'st'
    return suffix

months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10:'Oct', 11:'Nov', 12:'Dec'} #TODO this could be done w/ datetime

def trivia_msg(climatology, today_sst, day, month):
    
    trivia_msg = None
    obs_datetime = datetime(year=int(2024), month=int(month), day=int(day)).strftime('%b %-d %Y')
    if today_sst > climatology.SURF_TEMP_C.mean():
        trivia_msg = obs_datetime + ' is warmer than the average of all ' + months[month] + ' ' + str(int(day)) + suffix(day) + 's.'
    elif today_sst < climatology.SURF_TEMP_C.mean():
        trivia_msg = obs_datetime + ' is cooler than the average of all ' + months[month] + ' ' + str(int(day)) + suffix(day) + 's.'
    if today_sst > np.nanpercentile(climatology.SURF_TEMP_C.values,90):
        trivia_msg = obs_datetime + ' is among the hottest 10% of ' + months[month] + ' ' + str(int(day)) + suffix(day) + 's on record.'
    if today_sst < np.nanpercentile(climatology.SURF_TEMP_C.values,10):
        trivia_msg = obs_datetime + ' is among the coldest 10% of ' + months[month] + ' ' + str(int(day)) + suffix(day) + 's on record.'
    if today_sst >= climatology.SURF_TEMP_C.max():
        trivia_msg = obs_datetime + ' is the hottest ' + months[month] + ' ' + str(int(day)) + suffix(day) + ' on record.'
    elif today_sst <= climatology.SURF_TEMP_C.min():
        trivia_msg = obs_datetime + ' is the coldest ' + months[month] + ' ' + str(int(day)) + suffix(day) + ' on record.'
    return trivia_msg
for station in stations:
    sst_hist(data_dir+station[0], station[1])

# data_dir = "ELENA TODO" #e.x. '/Users/noahbarton/Documents/shorestations_nonQCed/
# stations = (("non-QC'd SIO Shore Station Data.csv", 'SIO Pier'),
#             ("non-QC'd San Clemente Shore Station Data.csv", 'San Clemente'),
#             ("non-QC'd Newport Beach Shore Station Data.csv", 'Newport Beach'),
#             ("non-QC'd Zuma Beach Shore Station Data.csv", 'Zuma Beach'),
#             ("non-QC'd Santa Barbara Shore Station Data.csv", 'Santa Barbara'),
#             ("non-QC'd Granite Canyon Station Data.csv", 'Granite Canyon'),
#             ("non-QC'd Pacific Grove Station Data.csv", 'Pacific Grove'),
#             ("non-QC'd Farallon Staion Data.csv", 'SE Farallon Island'),
#             ("non-QC'd Trinidad Beach Data.csv", 'Trinidad Beach'),
#             ("non-QC'd Trinidad Bay Data.csv", 'Trinidad Bay'))
