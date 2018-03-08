
import json
import sys


import pandas as pd
import requests
import os
import sqlalchemy
import pymysql
engine = sqlalchemy.create_engine("mysql+pymysql://shelg9202:A9v0S1u6@188.225.82.67/firstlook")

url = 'https://api.iextrading.com/1.0//ref-data/symbols'  

data = requests.get(url)

df = pd.DataFrame(data.json())

df.to_sql('list', engine, if_exists = 'append')