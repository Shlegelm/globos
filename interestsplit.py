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
from datetime import datetime, timedelta


import pandas as pd
import requests
import os
import sqlalchemy
import pymysql
import time

class interest():
    def splitter():
        engine = sqlalchemy.create_engine("mysql+pymysql://shelg9202:A9v0S1u6@188.225.82.67/firstlook")
            
            
            raw_data = pd.read_sql('raw_monitor', engine, index_col= ['index'])
            
            gd = []
            high_idf = pd.DataFrame(gd)
            medium_idf = pd.DataFrame(gd)
            low_idf = pd.DataFrame(gd)
            
            for row in raw_data.index:
                
                interest = raw_data.loc[raw_data.index==row,'zerocount'].values[0]
            
            
                if interest == 'high':
                    high_idf = high_idf.append(raw_data.loc[raw_data.index==row])
            
                if interest == 'medium':
                    medium_idf = medium_idf.append(raw_data.loc[raw_data.index==row])
            
                if interest == 'low':
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
        



