
import json
import sys


import pandas as pd
import requests
import os
import sqlalchemy
import pymysql



class iex5days:
    def fivedays(self,share):
        
        data = requests.get('https://api.iextrading.com/1.0/stock/'+share+'/chart/1m')
        iexdf = pd.DataFrame(data.json())

        try:
            ch1 = iexdf['changePercent'].iloc[-1]
        except KeyError:
            ch1 = 0
        try:
            ch2 = iexdf['changePercent'].iloc[-2]
        except KeyError:
            ch2 = 0
        try:
            ch3 = iexdf['changePercent'].iloc[-3]
        except KeyError:
            ch3 = 0
        try:
            ch4 = iexdf['changePercent'].iloc[-4]
        except KeyError:
            ch4 = 0
        try:
            ch5 = iexdf['changePercent'].iloc[-5]
        except KeyError:
            ch5 = 0
        try:
            chm = iexdf['changePercent'].mean()
        except KeyError:
            chm = 0

        monitor = []
        monitor = {
                   '1-day_percent' : ch1,
                   '2-day_percent' : ch2,
                   '3-day_percent' : ch3,
                   '4-day_percent' : ch4,
                   '5-day_percent' : ch5,
                   'mean_percent': chm}
        
        monitordf = pd.DataFrame(monitor, index = [share])
        
        return monitordf

#print(iex5days.fivedays('CBAY'))