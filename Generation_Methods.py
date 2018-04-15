# -*- coding: utf-8 -*-
"""
@author: Adam Eaton

Stores the Functions used to perform tasks related to selecting the data, 
generating the prediction as well as graphing the end result.
However the actual maths based functions are stored in Bayesian_Method.py 

"""
import Bayesian_Methods as BM

from plotly.offline import plot
from plotly.graph_objs import Scatter, Layout, Margin

import statsmodels.formula.api as smf
import datetime
import numpy as np
import pandas as pd
import os


def select_data(coin, interval):
    if coin == "btc":
        dataset = pd.read_csv(os.path.join('data', 'btc_data.csv'))
    elif coin == "eth":
        dataset = pd.read_csv(os.path.join('data', 'eth_data.csv'))
    elif coin == "ltc":
        dataset = pd.read_csv(os.path.join('data', 'ltc_data.csv'))

    if interval == 20:
        data = dataset.tail(27002)
        
    elif interval == 40:
        data = dataset.tail(54004)
        data = data.iloc[::2, :]
        
    elif interval == 60:
        data = dataset.tail(81006)
        data = data.iloc[::3, :]
        
    elif interval == 80:
        data = dataset.tail(108008)
        data = data.iloc[::4, :]
        
    data = data.reset_index(drop=True)
    return data


def conv_prices(start, data, col):
    values = []
    values.append(start)
    count = 1

    for index, row in data.iterrows():
        val = values[count - 1] + row[col]
        values.append(round(val, 2))
        count = count + 1
    return values
    

def generate_dates(data, interval):
    index = 0
    dates = []
    ts = datetime.datetime(2018, 1,1, 0,0,0)
        
    while index < len(data):
        dates.append(datetime.datetime.strftime(ts, '%H:%M:%S'))
        ts += datetime.timedelta(seconds=interval)
        index += 1 
    return dates


def generate_prediction(data):    
    weight = 2
    prices_1, prices_2, prices_3 = BM.split_prices(data)
    
    # Initialising series of dataframes
    train_1_45 = BM.create_dataframe(45)
    train_1_90 = BM.create_dataframe(90)
    train_1_180 = BM.create_dataframe(180)
    
    train_2_45 = BM.create_dataframe(45)
    train_2_90 = BM.create_dataframe(90)
    train_2_180 = BM.create_dataframe(180)
    
    train_3_45 = BM.create_dataframe(45)
    train_3_90 = BM.create_dataframe(90)
    train_3_180 = BM.create_dataframe(180)
        
    
    #Populating the previously created dataframes
    BM.populate_dataframe(train_1_45, prices_1)
    BM.populate_dataframe(train_1_90, prices_1)
    BM.populate_dataframe(train_1_180, prices_1)
    
    BM.populate_dataframe(train_2_45, prices_2)
    BM.populate_dataframe(train_2_90, prices_2)
    BM.populate_dataframe(train_2_180, prices_2)
    
    BM.populate_dataframe(train_3_45, prices_3)
    BM.populate_dataframe(train_3_90, prices_3)
    BM.populate_dataframe(train_3_180, prices_3)
    
    train_delta_45 = BM.set_delta(weight, train_3_45, train_2_45)
    train_delta_90 = BM.set_delta(weight, train_3_90, train_2_90)
    train_delta_180 = BM.set_delta(weight, train_3_180, train_2_180)
    
    train_1_180_Var = train_2_180[['Var']]
    train_2_180_Var = train_3_180[['Var']]
    tr_delta = []

    for index, row in train_1_180_Var.iterrows():
        tr_delta.append(row['Var'])
    
    for index, row in train_2_180_Var.iterrows():
        tr_delta[index-1] += row['Var']
        
    train_delta = np.asarray(tr_delta)
    train_delta = np.reshape(tr_delta, -1)

    # Combine all the training data
    training_data = BM.combine_data(train_delta, train_delta_45, 
                              train_delta_90, train_delta_180)
    
    # Using the delta_X data to train the linear model
    formula_s = 'delta ~ delta_45 + delta_90 + delta_180'
    model = smf.ols(formula = formula_s, data = training_data).fit()

    # Predict price variation on the training data set.
    predict = model.predict(training_data)
        
    predictions = { 'Predicted Values': predict }
    predictions_DF = pd.DataFrame(predictions)

    # start denotes the point at which the prices should be converted 
    start = prices_3[len(prices_3) - 1]
    predicted_vals = conv_prices(start, predictions_DF, 'Predicted Values')
    
    return predicted_vals


def generate_test(data):
    weight = 2
    prices_1, prices_2, prices_3 = BM.split_prices(data)
    
    # Initialising series of dataframes
    train_1_45 = BM.create_dataframe(45)
    train_1_90 = BM.create_dataframe(90)
    train_1_180 = BM.create_dataframe(180)
    
    train_2_45 = BM.create_dataframe(45)
    train_2_90 = BM.create_dataframe(90)
    train_2_180 = BM.create_dataframe(180)
    
    test_45 = BM.create_dataframe(45)
    test_90 = BM.create_dataframe(90)
    test_180 = BM.create_dataframe(180)
        
    
    #Populating the previously created dataframes
    BM.populate_dataframe(train_1_45, prices_1)
    BM.populate_dataframe(train_1_90, prices_1)
    BM.populate_dataframe(train_1_180, prices_1)
    
    BM.populate_dataframe(train_2_45, prices_2)
    BM.populate_dataframe(train_2_90, prices_2)
    BM.populate_dataframe(train_2_180, prices_2)

    BM.populate_dataframe(test_45, prices_3)
    BM.populate_dataframe(test_90, prices_3)
    BM.populate_dataframe(test_180, prices_3)
    
    
    # Populating training sets
    train_delta_45 = BM.set_delta(weight, train_2_45, train_1_45)
    train_delta_90 = BM.set_delta(weight, train_2_90, train_1_90)
    train_delta_180 = BM.set_delta(weight, train_2_180, train_1_180)
    
    test_delta_45 = BM.set_delta(weight, test_45, train_1_45)
    test_delta_90 = BM.set_delta(weight, test_90, train_1_90)
    test_delta_180 = BM.set_delta(weight, test_180, train_1_180)
    
    
    # Calculating train_delta by combiningthe variance values of both sets
    train_1_180_Var = train_1_180[['Var']]
    train_2_180_Var = train_2_180[['Var']]
    tr_delta = []

    for index, row in train_1_180_Var.iterrows():
        tr_delta.append(row['Var'])
    
    for index, row in train_2_180_Var.iterrows():
        tr_delta[index-1] += row['Var']
	
    # Actual delta values for training data
    train_delta = np.asarray(tr_delta)
    train_delta = np.reshape(tr_delta, -1)
    
    # Actual delta values for test data.
    test_delta = np.asarray(test_180[['Var']])
    test_delta = np.reshape(test_delta, -1)
    
    # Combine all the training data
    training_data = BM.combine_data(train_delta, train_delta_45, 
                              train_delta_90, train_delta_180)
    
    
    # Combine all the test data
    testing_data = BM.combine_data(test_delta, test_delta_45,
                                   test_delta_90, test_delta_180)
        
    # Using the delta_X data to train the linear model
    formula_s = 'delta ~ delta_45 + delta_90 + delta_180'
    model = smf.ols(formula = formula_s, data = training_data).fit()
        
    predict = model.predict(testing_data)
        
    comparison = { 'Actual Values': test_delta,
                  'Predicted Values': predict }

    comparison_DF = pd.DataFrame(comparison)
    start = prices_3[len(prices_3) - 1]
    actual_vals = conv_prices(start, comparison_DF, 'Actual Values')
    predicted_vals = conv_prices(start, comparison_DF, 'Predicted Values')
    
    return actual_vals, predicted_vals
    


def generate_graph(method, act_data, pred_data, time):
    if method == "predict":
        graph = plot({"data": [Scatter(x=time, y=pred_data)],
                    "layout": Layout(width="800", height="500", margin=Margin(t="20"))},
                    output_type='div')
    
    elif method == "test":
        graph = plot({"data": [Scatter(showlegend=True, name="Predicted", x=time, y=pred_data),Scatter(showlegend=True, name="Actual", x=time, y=act_data) ],
                    "layout": Layout(width="800", height="500", margin=Margin(t="20"),showlegend=True)},
                    output_type='div')
    return graph
