# -*- coding: utf-8 -*-
"""
@author: Adam Eaton

Contains the fucntions used to perform the Data Check on the selected Data
whether that be to drop rows with missing data or to interpolate it based on 
previous data.

"""
import Slack_Notify as SN

import numpy as np
import pandas as pd

# Interpolate np.NaN values within the supplied dataframe
def interp_values(data):
    interp_data = data.interpolate(method='values')
    return interp_data


# Check for missing values based on the epoch values in the 'date' column
def fill_data(data, freq):
    data_len = len(data.index)
    count = 1
    missing_count = 0
    
    # For each element in DataFrame, check its date against the predecessor
    # If difference is greater than freq, insert new row with appropriate time 
    # and initialise NaN values for other columns
    while(count < data_len):
        curr_row = data.iloc[count]['date']
        prev_row = data.iloc[count-1]['date']
        diff = curr_row - prev_row

        # Fault tolerant up to freq seconds 
        # if the difference in values is greater than freq seconds then mark is as missing
        # otherwise ignore it and move on
        if(int(diff-freq) > freq):
            missing_count = missing_count+1
            missing_vals = int(diff/freq)
            
            while(missing_vals >= 0):
                line = pd.DataFrame({"date": prev_row+freq, "price": np.NaN, 
                                     "vAsk": np.NaN, "vBid": np.NaN}, index=[count])
                data = pd.concat([data.ix[:count-1], line, data.ix[count:]]).reset_index(drop=True)
                missing_vals = missing_vals - 1
        
        count = count + 1
    
    if(missing_count != 0):
        data = interp_values(data)
        
    return data


# Drops any rows containing a NaN value 
def drop_data(data):
    drop = data.dropna(axis=1, how='any')
    return drop


def run_check(data, freq, fill):
    if fill == True:
        data = fill_data(data, freq)
    
    elif fill == False:
        data = drop_data(data)
    
    else:
        SN.send_notification("Data_Check.py - run_check() -- ")
        pass
    return data