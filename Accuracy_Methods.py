# -*- coding: utf-8 -*-
"""
@author: Adam Eaton

Stores Functions used to add entries to the accuracy table, as well as a 
Function to calculate the overall percentage accuracy of a given Cryptocurrency

"""
import Slack_Notify as SN

import csv
import os
import pandas as pd

def add_entries(crypto, act_vals, pred_vals):
    index = 0
    
    while index < len(pred_vals):
        if act_vals[index] == pred_vals[index]:
            acc = 0.0
        
        try:
            x = pred_vals[index] - act_vals[index]
            y = (pred_vals[index] + act_vals[index]) / 2
            acc = round((x / y) * 1000, 2)
             
            values = [crypto, act_vals[index], pred_vals[index], x, acc]
    
            with open(os.path.join('data',r'accuracy_data.csv'), 'a', newline='') as acc_csv:
                writer = csv.writer(acc_csv)
                writer.writerow(values)
        
            index += 1
        
        except:
            SN.send_notification("Accuracy_Methods.py - add_entries() -- ")
            pass
        
    
def calculate_accuracy(crypto):
    try:
        acc_data = pd.read_csv(os.path.join('data', 'accuracy_data.csv'))
        predicted_vals = []
        accuracy_vals = []
        
        for index, row in acc_data.iterrows():
            if row['crypto'] == crypto:
                predicted_vals.append(row['predicted'])
                accuracy_vals.append(row['accuracy'])
                
        avg_pred = sum(predicted_vals) / len(predicted_vals)
        avg_acc = sum(accuracy_vals) / len(accuracy_vals)
        
        x = avg_pred - avg_acc
        y = (avg_pred + avg_acc) / 2
        z = abs((x / y) * 10)
        overall_acc = round(100 - z, 2)
        
        return overall_acc
    
    except:
        SN.send_notification("Accuracy_Methods.py - calculate_accuracy() -- ")
        pass
