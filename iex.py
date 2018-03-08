
import json
import sys


import pandas as pd
import requests
import os
import sqlalchemy
import pymysql



class ieximport:
    def import_iex(share):
        engine = sqlalchemy.create_engine('mysql+pymysql://shelg9202:A9v0S1u6@188.225.82.67/firstpool')
        
        data = requests.get('https://api.iextrading.com/1.0/stock/'+share+'/chart/1m')
        print(share)
        df = pd.DataFrame(data.json())
        #PercerntMod = []
        #for row in df['changePercent']:
        #    if row < 0:
        #        PercerntMod.append(-1)
        #    else:
        #        PercerntMod.append(1)
        
        #df['PModule'] = PercerntMod * df['changePercent']
        #Pmean = df['PModule'].mean()
        #print(Pmean)
        #PMeanCleaner2 = []
        #for row in df['PModule']:
        #    if row > Pmean*2:
        #        PMeanCleaner2.append(1)
        #    else:
        #        PMeanCleaner2.append(0)
        # 
        #df['Jump2'] = PMeanCleaner2
        #PMeanCleaner3 = []

        #for row in df['PModule']:
        #    if row > Pmean*3:
        #        PMeanCleaner3.append(1)
        #    else:
        #        PMeanCleaner3.append(0)
        
        #df['Jump3'] = PMeanCleaner3
        #PMeanCleaner4 = []
        
        #for row in df['PModule']:
        #    if row > Pmean*4:
        #       PMeanCleaner4.append(1)
        #    else:
        #       PMeanCleaner4.append(0)
         
        #df['Jump4'] = PMeanCleaner4
        #PMeanCleaner5 = []
        
        #for row in df['PModule']:
        #    if row > Pmean*5:
        #        PMeanCleaner5.append(1)
        #    else:
        #        PMeanCleaner5.append(0)
         
        #df['Jump5'] = PMeanCleaner5
        df['date'] = pd.to_datetime(df['date'],errors = 'ignore')
        df.to_sql(share, engine, if_exists = 'append')






#df['MA5'] = pd.rolling_mean(df['open'], window=5)
#df['MA15'] = pd.rolling_mean(df['open'], window=15)
#df['MA30'] = pd.rolling_mean(df['open'], window=30)

#M3015 = []
#M3015 = df['MA30']-df['MA15']
#M305 = []
#M305 = df['MA30']-df['MA5']
#M155 = []
#M155 = df['MA15']-df['MA5']
#M30155 = []
#df['M30155'] = M3015 + M305 + M155

#Trendchange = []
#for row in df['M30155']:
#    if (-0.1)< row < 0.1:
 #       Trendchange.append(1)
 #   else:
  #      Trendchange.append(0)

#df['Trendchange'] = Trendchange * df['date']
#df['clo-40'] = df.close - df.MA40
#df['clo-10'] = df.close - df.MA10

#df['eve'] = (df['clo-40'] - df['clo-40'].shift())/df['clo-40'].shift()
#speed40 = []
#speed10 = []

# For each row in the column,
#for row in df['clo-40']:
#    if row > 40:
#        speed40.append(1)
#    else:
#        speed40.append(0)

#for row in df['clo-10']:
#    if row <0:
#        speed10.append(0)
#    else:
#        speed10.append(1)
        
# Create a column from the list
#df['speed40'] = speed40
#df['speed10'] = speed10

#df['growth'] = df['speed10']*df['speed40']

