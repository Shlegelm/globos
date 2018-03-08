
from iexfinance import Share
import json
import sys
import numpy as np

import pandas as pd
import requests
import os
import sqlalchemy
import pymysql
engine_s = sqlalchemy.create_engine("mysql+pymysql://shelg9202:A9v0S1u6@188.225.82.67/netease_s")
engine_g = sqlalchemy.create_engine("mysql+pymysql://shelg9202:A9v0S1u6@188.225.82.67/netease_g")
engine_sg = sqlalchemy.create_engine("mysql+pymysql://shelg9202:A9v0S1u6@188.225.82.67/netease_sg")

dfs = pd.read_sql('netease_st4', engine_s)
dfg = pd.read_sql('netease_g3', engine_g)

dfsg = pd.merge(dfs, dfg, how='outer', on='date')

googlechange = []
googlechange = dfsg['netease']-dfsg['netease'].shift()
googlechange = googlechange/dfsg['netease'].shift()


dfsg['googchange'] = googlechange
dfsg['googchange']=dfsg['googchange'].replace([np.inf, -np.inf], np.nan)

#dfsg['Jump2'] = dfsg['Jump2']*(dfsg['googchange'].shift()+dfsg['googchange'].shift(2)+dfsg['googchange'].shift(3)+dfsg['googchange'].shift(4)+dfsg['googchange'].shift(5))
#dfsg['Jump3'] = dfsg['Jump3']*(dfsg['googchange'].shift()+dfsg['googchange'].shift(2)+dfsg['googchange'].shift(3)+dfsg['googchange'].shift(4)+dfsg['googchange'].shift(5))
#dfsg['Jump4'] = dfsg['Jump4']*(dfsg['googchange'].shift()+dfsg['googchange'].shift(2)+dfsg['googchange'].shift(3)+dfsg['googchange'].shift(4)+dfsg['googchange'].shift(5))
#dfsg['Jump5'] = dfsg['Jump5']*(dfsg['googchange'].shift()+dfsg['googchange'].shift(2)+dfsg['googchange'].shift(3)+dfsg['googchange'].shift(4)+dfsg['googchange'].shift(5))

dfsg['Jump2'] = dfsg['Jump2']*((dfsg['netease'].shift(3)-dfsg['netease'].shift(7))/dfsg['netease'].shift(7)).replace([np.inf, -np.inf], np.nan)
dfsg['Jump3'] = dfsg['Jump3']*((dfsg['netease'].shift(3)-dfsg['netease'].shift(7))/dfsg['netease'].shift(7)).replace([np.inf, -np.inf], np.nan)
dfsg['Jump4'] = dfsg['Jump4']*((dfsg['netease'].shift(3)-dfsg['netease'].shift(7))/dfsg['netease'].shift(7)).replace([np.inf, -np.inf], np.nan)
dfsg['Jump5'] = dfsg['Jump5']*((dfsg['netease'].shift(3)-dfsg['netease'].shift(7))/dfsg['netease'].shift(7)).replace([np.inf, -np.inf], np.nan)


dfsg.to_sql('netease_sg14', engine_sg, if_exists = 'append')
