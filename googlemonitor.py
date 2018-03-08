from sqlalchemy.types import VARCHAR
from iex import ieximport
from sharetest import sharet
from RequestFromGoogle import google
from RequestFromIEX import iex5days
import json
import sys
from itertools import cycle
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text


import pandas as pd
import requests
import os
import sqlalchemy
import pymysql

engine = sqlalchemy.create_engine("mysql+pymysql://shelg9202:A9v0S1u6@188.225.82.67/firstlook")


df_list = pd.read_sql('list', engine)

gd = []
raw_gdf = pd.DataFrame(gd)
zerodf = pd.DataFrame(gd)

gen = cycle([0])


for elt in gen:
    for row in df_list['symbol']:
        
        try:
            
            raw_gdf = pd.read_sql('raw_monitor', engine, index_col= ['index'])
            
            
            with engine.connect() as con:
                rs = con.execute('DELETE FROM raw_monitor_backup')
            raw_gdf.to_sql('raw_monitor_backup', engine, if_exists = 'append', dtype={'None':VARCHAR(200)})
            

            monitorgoogle, zerocounter = google.google_dow(row)
            monitoriex = iex5days.fivedays(row)
            monitordf = pd.concat([monitorgoogle,monitoriex],axis=1, join='inner')
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
            
            if row in raw_gdf.index:
                pass
                raw_gdf.loc[raw_gdf.index == row, '1-day_step':'2-day_step'] = a,b
                raw_gdf.loc[raw_gdf.index == row, '3-day_step':'mean_step'] = c,d
                raw_gdf.loc[raw_gdf.index == row, '1-day_percent':'2-day_percent'] = e,f
                raw_gdf.loc[raw_gdf.index == row, '3-day_percent':'4-day_percent'] = h,i
                raw_gdf.loc[raw_gdf.index == row, '5-day_percent':'mean_percent'] = g,o
            else:
                raw_gdf = raw_gdf.append(monitordf)

            print(row)

            

            with engine.connect() as con:
                rs = con.execute('DELETE FROM raw_monitor')
           
            raw_gdf.to_sql('raw_monitor', engine, if_exists = 'append', dtype={'None':VARCHAR(200)})
            print('done')
        except sqlalchemy.exc.ProgrammingError:
            pass
            
    with engine.connect() as con:
                rs = con.execute('DELETE FROM raw_loop_backup')
    raw_gdf.to_sql('raw_loop_backup', engine, if_exists = 'append', dtype={'None':VARCHAR(200)})     
            
        
    
        
    

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