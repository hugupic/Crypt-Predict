# -*- coding: utf-8 -*-
"""
@author: Adam Eaton

Main Flask Application for Crypt-Predict. Contains the different possible routes
and their associated function calls.

"""

from flask import Flask, render_template, request, Markup

import Generation_Methods as GM
import Data_Check as DC
import Accuracy_Methods as AM

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def return_index():
    return render_template('index.html', 
                           btc_acc = AM.calculate_accuracy("btc"),
                           eth_acc = AM.calculate_accuracy("eth"),
                           ltc_acc = AM.calculate_accuracy("ltc"))


@app.route('/about')
def return_about():
    return render_template('about.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit_form():
    btc = request.form.get('btc-check')
    eth = request.form.get('eth-check')
    ltc = request.form.get('ltc-check')
    method = str(request.form.get('method'))
    time_interval = int(request.form.get('interval'))
    # TODO: Fix data filling issue
    fill_missing = False
    
    btc_graph = False
    eth_graph = False
    ltc_graph = False
    
    if method == "predict":
        if btc == "on":
            data = GM.select_data("btc", time_interval)
            data = DC.run_check(data, time_interval, fill_missing)
            btc_pred = GM.generate_prediction(data)
            btc_time = GM.generate_dates(btc_pred, time_interval)
            btc_graph = GM.generate_graph(method, None, btc_pred, btc_time)
            btc_graph = Markup(btc_graph)
            
        if eth == "on":
            data = GM.select_data("eth", time_interval)
            data = DC.run_check(data, time_interval, fill_missing)
            eth_pred = GM.generate_prediction(data)
            eth_time = GM.generate_dates(eth_pred, time_interval)
            eth_graph = GM.generate_graph(method, None, eth_pred, eth_time)
            eth_graph = Markup(eth_graph)
            
        if ltc == "on":
            data = GM.select_data("ltc", time_interval)
            data = DC.run_check(data, time_interval, fill_missing)
            ltc_pred = GM.generate_prediction(data)
            ltc_time = GM.generate_dates(ltc_pred, time_interval)
            ltc_graph = GM.generate_graph(method, None, ltc_pred, ltc_time)
            ltc_graph = Markup(ltc_graph)
        
        return render_template('results.html',
                               btc_div = btc_graph,
                               eth_div = eth_graph,
                               ltc_div = ltc_graph)
        
    elif method == "test":
        if btc == "on":
            data = GM.select_data("btc", time_interval)
            data = DC.run_check(data, time_interval, fill_missing)
            btc_actual, btc_pred = GM.generate_test(data)
            AM.add_entries("btc", btc_actual, btc_pred)
            btc_time = GM.generate_dates(btc_pred, time_interval)
            btc_graph = GM.generate_graph(method, btc_actual, btc_pred, btc_time)
            btc_graph = Markup(btc_graph)
            
        if eth == "on":
            data = GM.select_data("eth", time_interval)
            data = DC.run_check(data, time_interval, fill_missing)
            eth_actual, eth_pred = GM.generate_test(data)
            AM.add_entries("eth", eth_actual, eth_pred)
            eth_time = GM.generate_dates(eth_pred, time_interval)
            eth_graph = GM.generate_graph(method, eth_actual, eth_pred, eth_time)
            eth_graph = Markup(eth_graph)
            
        if ltc == "on":
            data = GM.select_data("ltc", time_interval)
            data = DC.run_check(data, time_interval, fill_missing)
            ltc_actual, ltc_pred = GM.generate_test(data)
            AM.add_entries("ltc", ltc_actual, ltc_pred)
            ltc_time = GM.generate_dates(ltc_pred, time_interval)
            ltc_graph = GM.generate_graph(method, ltc_actual, ltc_pred, ltc_time)
            ltc_graph = Markup(ltc_graph)
            
        return render_template('results.html',
                               btc_div = btc_graph,
                               eth_div = eth_graph,
                               ltc_div = ltc_graph)

    
if __name__ == '__main__':
    app.run(debug = True)