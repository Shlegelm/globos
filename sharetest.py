

import json
import sys
import numpy as np

import pandas as pd
import requests
import os
import sqlalchemy
import pymysql

class sharet:
    def startend(share):
        engine = sqlalchemy.create_engine("mysql+pymysql://shelg9202:A9v0S1u6@188.225.82.67/firstpool")
        df = pd.read_sql(share, engine)
        print(share)
       
        def se_count(df, sdate, edate):
            try:
                start = df.loc[df['date'] == sdate]
                s_val = start.at[start.index[0],'open']
            except IndexError:
                s_val = 0
            try:
                end = df.loc[df['date'] == edate]
                e_val = end.at[end.index[0],'close']
            except IndexError:
                e_val = 0
            if s_val == 0:
                a = (e_val - s_val)*100
            else:
                a = ((e_val - s_val)/s_val)*100
            return a
        
        a = se_count(df,'2013-02-04 00:00:00','2013-12-31 00:00:00')
        b = se_count(df,'2014-01-02 00:00:00','2014-12-31 00:00:00')
        c = se_count(df,'2015-01-02 00:00:00','2015-12-31 00:00:00')
        d = se_count(df,'2016-01-04 00:00:00','2016-12-30 00:00:00')
        e = se_count(df,'2017-01-03 00:00:00','2017-12-29 00:00:00')
        f = se_count(df,'2018-01-02 00:00:00','2018-02-02 00:00:00')

        d = {'share' : share,
             '2013' : a,
             '2014' : b,
             '2015' : c,
             '2016' : d,
             '2017' : e,
             '2018' : f}
            
        dfd=pd.DataFrame(d, index = [0])
        return dfd

    def test(share):
        engine = sqlalchemy.create_engine("mysql+pymysql://shelg9202:A9v0S1u6@188.225.82.67/firstpool")
        df = pd.read_sql(share, engine)
        df['year'] = df['date'].dt.year
        dfnew = df.groupby(["year"])["changePercent"].sum()
        dfnew.name = share
        print(dfnew.name)
        return dfnew
    
  
#sharet.startend('ABCB')
        
        
        
       
        
        




