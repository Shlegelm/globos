import sys
import pandas as pd
print(sys.version)
from sqlalchemy.types import VARCHAR

from sharetest import sharet
import RequestFromGoogle
google = RequestFromGoogle.google()

import RequestFromIEX
iex5days = RequestFromIEX.iex5days()
import json

from itertools import cycle
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text
from datetime import datetime, timedelta


import requests
import os
import sqlalchemy
import pymysql
import time

engine = sqlalchemy.create_engine("mysql+pymysql://shelg9202:A9v0S1u6@188.225.82.67/firstlook")


df_list = pd.read_sql('list', engine, index_col= ['index'])

gd = []
raw_gdf = pd.DataFrame(gd)
zerodf = pd.DataFrame(gd)

def splitter():
    engine = sqlalchemy.create_engine("mysql+pymysql://shelg9202:A9v0S1u6@188.225.82.67/firstlook")
    raw_data = pd.read_sql('raw_monitor', engine, index_col= ['index'])
            
    gd = []
    high_idf = pd.DataFrame(gd)
    medium_idf = pd.DataFrame(gd)
    low_idf = pd.DataFrame(gd)
            
    for row in raw_data.index:
        interest = raw_data.loc[raw_data.index==row,'zerocount'].values[0]
        if interest <=50:
            high_idf = high_idf.append(raw_data.loc[raw_data.index==row])
        if 50 < interest < 150 :
            medium_idf = medium_idf.append(raw_data.loc[raw_data.index==row])
        if interest >=150:
            low_idf = low_idf.append(raw_data.loc[raw_data.index==row])      
        
    with engine.connect() as con:
        rs = con.execute('DELETE FROM high_monitor')         
    high_idf.to_sql('high_monitor', engine, if_exists = 'append', dtype={'None':VARCHAR(200)})
    print('High interest renewed')
    
    with engine.connect() as con:
        rs = con.execute('DELETE FROM medium_monitor')
    medium_idf.to_sql('medium_monitor', engine, if_exists = 'append', dtype={'None':VARCHAR(200)})
    print('Medium interest renewed')
            
    with engine.connect() as con:
        rs = con.execute('DELETE FROM low_monitor')
    low_idf.to_sql('low_monitor', engine, if_exists = 'append', dtype={'None':VARCHAR(200)})
    print('Low interest renewed')


            
                    


while True:    
        print ('start - you can stop')
   
        try:
            
            try:
                raw_gdf = pd.read_sql('raw_monitor', engine, index_col= ['index'])
            except sqlalchemy.exc.ProgrammingError:
                pass
            

            lastshare = raw_gdf.loc[raw_gdf['update']==max(raw_gdf['update'])].index.values[0]
            nextshare = df_list.loc[df_list['symbol']==lastshare].index.values[0]+1
            
            if nextshare in df_list.index:
                indexshare = nextshare
            else:
                indexshare = 0
            
            
            print (indexshare)
            row = df_list.loc[df_list.index==indexshare, 'symbol'].values[0]
            name_notcleared = df_list.loc[df_list.index==indexshare, 'name'].values[0]
            name_cleared = name_notcleared.replace("Inc.","")
            name_cleared = name_cleared.replace("Inc.","")
            name_cleared = name_cleared.replace("Corp.","")
            name_cleared = name_cleared.replace("Ltd.","")
            name_cleared = name_cleared.replace("Ltd","")
            print(row)

            try:
                with engine.connect() as con:
                    rs = con.execute('DELETE FROM raw_monitor_backup')
            except IOError:
                pass
            try:
                raw_gdf.to_sql('raw_monitor_backup', engine, if_exists = 'append', dtype={'None':VARCHAR(200)})
            except sqlalchemy.exc.ProgrammingError:
                pass
            print ('backup rewrite')
            rows = row + ' stock'

            try:
                g_stock = google.google_dow(rows)
            except KeyError:
                monitor = {'zerocount': 0,
                           '1-day_step': 0,
                           '2-day_step': 0,
                           '3-day_step': 0,
                           'mean_step': 0}
                g_stock = pd.DataFrame(monitor, index=[rows])

            try:
                g_name_nc = google.google_dow(name_notcleared)
            except KeyError:
                monitor = {'zerocount': 0,
                           '1-day_step': 0,
                           '2-day_step': 0,
                           '3-day_step': 0,
                           'mean_step': 0}
                g_name_nc = pd.DataFrame(monitor, index=[name_notcleared])

            try:
                g_name_c = google.google_dow(name_cleared)
            except KeyError:
                monitor = {'zerocount': 0,
                           '1-day_step': 0,
                           '2-day_step': 0,
                           '3-day_step': 0,
                           'mean_step': 0}
                g_name_c = pd.DataFrame(monitor, index=[name_cleared])

            gmz1 = g_stock.loc[g_stock.index == rows,'zerocount'].values[0]
            gmz2 = g_name_nc.loc[g_name_nc.index == name_notcleared,'zerocount'].values[0]
            gmz3 = g_name_c.loc[g_name_c.index == name_cleared,'zerocount'].values[0]
            gmz = gmz1 + gmz2 + gmz3

            gm1 = g_stock.loc[g_stock.index == rows,'1-day_step'].values[0]+g_name_nc.loc[g_name_nc.index == name_notcleared,'1-day_step'].values[0]+g_name_c.loc[g_name_c.index == name_cleared,'1-day_step'].values[0]
            gm2 = g_stock.loc[g_stock.index == rows, '2-day_step'].values[0] + g_name_nc.loc[g_name_nc.index == name_notcleared, '2-day_step'].values[0] +g_name_c.loc[g_name_c.index == name_cleared, '2-day_step'].values[0]
            gm3 = g_stock.loc[g_stock.index == rows,'3-day_step'].values[0]+g_name_nc.loc[g_name_nc.index == name_notcleared,'3-day_step'].values[0]+g_name_c.loc[g_name_c.index == name_cleared,'3-day_step'].values[0]
            gmm = g_stock.loc[g_stock.index == rows,'mean_step'].values[0]+g_name_nc.loc[g_name_nc.index == name_notcleared,'mean_step'].values[0]+g_name_c.loc[g_name_c.index == name_cleared,'mean_step'].values[0]
            google_m = {'zerocount': gmz/3,
                        '1-day_step': gm1/3,
                        '2-day_step': gm2/3,
                        '3-day_step': gm3/3,
                        'mean_step': gmm/3}
            monitorgoogle = pd.DataFrame(google_m, index=[row]) 
            print('hooray')
            print(monitorgoogle)
            try:
                monitoriex = iex5days.fivedays(row)
            except IndexError:
                monitor = {
                    '1-day_percent': 0,
                    '2-day_percent': 0,
                    '3-day_percent': 0,
                    '4-day_percent': 0,
                    '5-day_percent': 0,
                    'mean_percent': 0}

                monitoriex = pd.DataFrame(monitor, index=[row])
            monitordf = pd.concat([monitorgoogle,monitoriex],axis=1, join='inner')
            monitordf['update'] = datetime.today()
            a = monitordf.loc[monitordf.index==row,'1-day_step'].values[0]
            b = monitordf.loc[monitordf.index==row,'2-day_step'].values[0]
            c = monitordf.loc[monitordf.index==row,'3-day_step'].values[0]
            d = monitordf.loc[monitordf.index==row,'mean_step'].values[0]
            e = monitordf.loc[monitordf.index==row,'1-day_percent'].values[0]
            f = monitordf.loc[monitordf.index==row,'2-day_percent'].values[0]
            h = monitordf.loc[monitordf.index==row,'3-day_percent'].values[0]
            i = monitordf.loc[monitordf.index==row,'4-day_percent'].values[0]
            g = monitordf.loc[monitordf.index==row,'5-day_percent'].values[0]
            o = monitordf.loc[monitordf.index==row,'mean_percent'].values[0]
            t = monitordf.loc[monitordf.index==row,'update'].values[0]
            z = monitordf.loc[monitordf.index==row,'zerocount'].values[0]

        
            
            if row in raw_gdf.index:
                
                raw_gdf.loc[raw_gdf.index == row, '1-day_step':'2-day_step'] = a,b
                raw_gdf.loc[raw_gdf.index == row, '3-day_step':'mean_step'] = c,d
                raw_gdf.loc[raw_gdf.index == row, '1-day_percent':'2-day_percent'] = e,f
                raw_gdf.loc[raw_gdf.index == row, '3-day_percent':'4-day_percent'] = h,i
                raw_gdf.loc[raw_gdf.index == row, '5-day_percent':'mean_percent'] = g,o
                #raw_gdf.loc[raw_gdf.index == row, 'update':'zerocount'] = t,z
                raw_gdf.loc[raw_gdf.index == row, 'update'] = t
                raw_gdf.loc[raw_gdf.index == row, 'zerocount'] = z
            else:
                raw_gdf = raw_gdf.append(monitordf)

            print(row)

            print ('monitor will be rewritten now')

            with engine.connect() as con:
                rs = con.execute('DELETE FROM raw_monitor')
            
           
            raw_gdf.to_sql('raw_monitor', engine, if_exists = 'append', dtype={'None':VARCHAR(200)})

            if indexshare % 200 ==0:
                print('RENEW OF INTEREST SETS')
                splitter()
                
            else:
                pass


            print('done - you can stop')
            time.sleep(5)
        except sqlalchemy.exc.ProgrammingError:
            pass





    #for row in df_list['symbol']:
    
            
    #try:
    #    with engine.connect() as con:
    #        rs = con.execute('DELETE FROM raw_loop_backup')
    #except IOError:
    #    pass
    #raw_gdf.to_sql('raw_loop_backup', engine, if_exists = 'append', dtype={'None':VARCHAR(200)})
    #print ('loop rewritten')
            
        
    
        
    

#tdf = {'a': [1,2,3,4],
#       'b': [3,4,3,4],
#       'c': [5,6,5,6],
#       'd': [7,7,7,7],
#       'e': [7,7,7,7]}

#ttdf = pd.DataFrame(tdf)
#print(ttdf)

#a = 15
#b = 17
#r = 19
#w = 15

#ttdf.loc[ttdf['a'] == 3, 'b':'c'] = a,b
#ttdf.loc[ttdf['a'] == 3, 'd':'e'] = r,w
#print(ttdf)

 #print(df_list.loc[df_list['symbol']==row,'name'].values[0])
