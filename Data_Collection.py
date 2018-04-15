# -*- coding: utf-8 -*-
"""
@author: Adam Eaton

Contains functions to retrieve and store data for the three Cryptocurrencies.
Doesn't run as part of the main application but instead runs in it's own instance.

"""
import Slack_Notify as SN

import time 
import requests
import csv

BTC_Ticker_Add = "https://www.okcoin.com/api/v1/ticker.do?symbol=btc_usd"
BTC_Depth_Add = "https://www.okcoin.com/api/v1/depth.do?symbol=btc_usd&size=60"

ETH_Ticker_Add = "https://www.okcoin.com/api/v1/ticker.do?symbol=eth_usd"
ETH_Depth_Add = "https://www.okcoin.com/api/v1/depth.do?symbol=eth_usd&size=60"

LTC_Ticker_Add = "https://www.okcoin.com/api/v1/ticker.do?symbol=ltc_usd"
LTC_Depth_Add = "https://www.okcoin.com/api/v1/depth.do?symbol=ltc_usd&size=60"

currency_Add = "https://api.fixer.io/latest?base=USD"


def run_queries():
    btc_data = BTC_query()
    eth_data = ETH_query()
    ltc_data = LTC_query()
    
    btc_str = str(btc_data)
    eth_str = str(eth_data)
    ltc_str = str(ltc_data)
    
    if(btc_str[:1] == "[" and eth_str[:1] == "[" and ltc_str[:1] == "[" ):
        with open(r'btc_data.csv', 'a', newline = '') as btc:
            writer = csv.writer(btc)
            writer.writerow(btc_data)
    
        with open(r'eth_data.csv', 'a', newline = '') as eth:
            writer = csv.writer(eth)
            writer.writerow(eth_data)
        
        with open(r'ltc_data.csv', 'a', newline = '') as ltc:
            writer = csv.writer(ltc)
            writer.writerow(ltc_data)
        
        print("Tick")
    else:
        raise ValueError('Error has occured when querying OKCoin API')
        SN.send_notification("Data_Collection.py - run_queries() -- ")
    return

# Possibly look into re-implementing later on, as of now (18/01/18) it's providing innacurate results
"""
def currency_query(val_usd):
    currency_response = requests.get(currency_Add).json()
    currency_value = currency_response['rates']['EUR']
    return float(val_usd) * float(currency_value)
"""

def BTC_query(): 
    BTC_Ticker = requests.get(BTC_Ticker_Add).json()
    BTC_Depth = requests.get(BTC_Depth_Add).json()
    
    BTC_Price_USD = float(BTC_Ticker['ticker']['last'])
   # BTC_Price_EUR = currency_query(BTC_Price_USD)
    
    BTC_Date = BTC_Ticker['date']
    BTC_vBid = sum([bid[1] for bid in BTC_Depth['bids']])
    BTC_vAsk = sum([ask[1] for ask in BTC_Depth['asks']])
    values = [BTC_Date, BTC_Price_USD, BTC_vBid, BTC_vAsk]
    return values


def ETH_query(): 
    ETH_Ticker = requests.get(ETH_Ticker_Add).json()
    ETH_Depth = requests.get(ETH_Depth_Add).json()
    
    ETH_Price_USD = float(ETH_Ticker['ticker']['last'])
    #ETH_Price_EUR = currency_query(ETH_Price_USD)
    
    ETH_Date = ETH_Ticker['date']
    ETH_vBid = sum([bid[1] for bid in ETH_Depth['bids']])
    ETH_vAsk = sum([ask[1] for ask in ETH_Depth['asks']])
    values = [ETH_Date, ETH_Price_USD, ETH_vBid, ETH_vAsk]
    return values
    

def LTC_query(): 
    LTC_Ticker = requests.get(LTC_Ticker_Add).json()
    LTC_Depth = requests.get(LTC_Depth_Add).json()
    
    LTC_Price_USD = float(LTC_Ticker['ticker']['last'])
    #LTC_Price_EUR = currency_query(LTC_Price_USD)
    
    LTC_Date = LTC_Ticker['date']
    LTC_vBid = sum([bid[1] for bid in LTC_Depth['bids']])
    LTC_vAsk = sum([ask[1] for ask in LTC_Depth['asks']])
    values = [LTC_Date, LTC_Price_USD, LTC_vBid, LTC_vAsk]
    return values


def main():
    start_time = time.time()
    
    while True:
        try:
            run_queries()
            time.sleep(20.0 - ((time.time() - start_time) % 20.0))
        except:
            raise ValueError('Error occured when attempting to run Data Collection queries')
            SN.send_notification("Data_Collection.py - run_queries() -- ")
            pass

if __name__ == '__main__':
    main()