# -*- coding: utf-8 -*-
"""
@author: Adam Eaton

Stores the functions used to split data, creating dataframes as well as
make the mathematical calculations involved in the algorithm. 

"""
import Slack_Notify as SN

import pandas as pd
import numpy as np
import math

def split_prices(df):
    prices_1 = []
    prices_2 = []
    prices_3 = []
    
    dfVal = df["price"].values
    count = 0 
    
    try:
        for x in dfVal:
            if(count < 9001):
                prices_1.append(x)  
            if(count > 9000 and count <= 18001):
                prices_2.append(x) 
            if(count > 18000 and count < 27002):
                prices_3.append(x)
            count = count+1
            
    except:
        raise ValueError('Issue splitting dataframe into individual price arrays')
        SN.send_notification("Bayesian_Methods.py - split_prices() -- ")
        pass
    
    return prices_1, prices_2, prices_3


def create_dataframe(l):
    index_list= []
    column_list = []
    
    for x in range(50):
        index_list.append(x+1)
        
    for x in range(l):
        column_list.append("priceDiff"+str(x+1))
    column_list.append("Var")

    df = pd.DataFrame(index=index_list, columns=column_list)
    df = df.fillna(0.0)

    return df


def populate_dataframe(data_frame, data_source):
    col_num = len(data_frame.columns)
    value_count = 1
    
    if(col_num == 46):
        value_count = 181
    if(col_num == 91):
        value_count = 91
    
    for index, row in data_frame.iterrows():
        row_contents = []
        counter = 1
        while(counter <= col_num):
            if(counter == col_num):
                row['Var'] = np.mean(row_contents)
                break
            
            price_diff = data_source[value_count] - data_source[value_count-1]
            

            row["priceDiff"+str(counter)] = price_diff
            
            row_contents.append(price_diff)
            value_count = value_count+1
            counter = counter+1
    
    return col_num


def calculate_similarity(x, y):
    similarity = 0
    mean_1 = np.mean(x)
    mean_2 = np.mean(y)
    sum_m = 0
    
    for i in range(0, len(x)):
        m_x = (x[i] - mean_1)
        m_y = (y[i] - mean_2)
        sum_m += m_x * m_y

    m_std = float(len(x) * np.std(x) * np.std(y))
    
    try:
        similarity = float(sum_m) / float(m_std)
    except ZeroDivisionError:
        similarity = 0.1
        
    return similarity


def calculate_delta(row, df, weight):
    x0 = 0 
    x1 = 0

    for i in range(0,len(df)):
        y = df.iloc[i][-1]
        z = df.iloc[i][:-1]
        sli = row[:-1]
        
        similarity = calculate_similarity(sli, z)
        
        x1 += y * math.exp(similarity * weight)
        x0 += math.exp(similarity * weight)
        
    return float(x1 / x0)


def set_delta(weight, train_1, train_2):
    t_delta = np.empty(0)
    index = len(train_2.index)
    
    for x in range(0, index):
        delta = calculate_delta(train_1.iloc[x], train_2, weight)
        t_delta = np.append(t_delta, delta)
        
    return t_delta


def combine_data(d1, d2, d3, d4):
    data = {'delta': d1, 'delta_45': d2,
            'delta_90': d3, 'delta_180': d4}
    
    data_df = pd.DataFrame(data)
    
    return data_df

