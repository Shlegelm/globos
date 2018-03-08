## INITIAL COMMENTS ##

# Try to split up search requests to get daily Google Trend data

## SETUP ##
from datetime import datetime, timedelta
from pytrends.request import TrendReq
import pytrends
import pandas as pd
import os
import sqlalchemy
import pymysql
from numpy import inf
import time




class google():
    def google_dow(self, word):
        
        # The maximum for a timeframe for which we get daily data is 270.
        # Therefore we could go back 269 days. However, since there might
        # be issues when rescaling, e.g. zero entries, we should have an
        # overlap that does not consist of only one period. Therefore,
        # I limit the step size to 250. This leaves 19 periods for overlap.
        #maxstep = 269
        #overlap = 40
        
        maxstep = 250
        overlap = 29
        step    = maxstep - overlap + 1
        kw_list = [word]
        kw_list2 = [word+' stock']
        
        
        
        ## FIRST RUN ##
        
        # Login to Google. Only need to run this once, the rest of requests will use the same session.
        pytrend = TrendReq()
        
        # Run the first time (if we want to start from today, otherwise we need to ask for an end_date as well
        today = datetime.today().date()
        old_date = today
        
        # Go back in time
        new_date = today - timedelta(days=step)
        start_date = new_date
        # Create new timeframe for which we download data
        timeframe = new_date.strftime('%Y-%m-%d')+' '+old_date.strftime('%Y-%m-%d')
        try:
            pytrend.build_payload(kw_list=kw_list, timeframe = timeframe)
        except pytrends.exceptions.ResponseError:
            time.sleep(20)
            try:
                pytrend.build_payload(kw_list=kw_list2, timeframe=timeframe)
            except pytrends.exceptions.ResponseError:
                ag = 0
                if ag == 0:
                    try:
                        time.sleep(1200)
                        print('google attempt')
                        pytrend.build_payload(kw_list=kw_list2, timeframe=timeframe)
                        ag = 1
                    except pytrends.exceptions.ResponseError:
                        ag = 0

        interest_over_time_df = pytrend.interest_over_time()
        
        ## RUN ITERATIONS
        
        
        
        
        
        while new_date>start_date:
        
            ### Save the new date from the previous iteration.
            # Overlap == 1 would mean that we start where we
            # stopped on the iteration before, which gives us
            # indeed overlap == 1.
            old_date = new_date + timedelta(days=overlap-1)
        
            ### Update the new date to take a step into the past
            # Since the timeframe that we can apply for daily data
            # is limited, we use step = maxstep - overlap instead of
            # maxstep.
            new_date = new_date - timedelta(days=step)
            # If we went past our start_date, use it instead
            if new_date < start_date:
                new_date = start_date
        
            # New timeframe
            timeframe = new_date.strftime('%Y-%m-%d')+' '+old_date.strftime('%Y-%m-%d')
            print(timeframe)
        
            # Download data
            pytrend.build_payload(kw_list=kw_list, timeframe = timeframe)
            temp_df = pytrend.interest_over_time()
            if (temp_df.empty):
                raise ValueError('Google sent back an empty dataframe. Possibly there were no searches at all during the this period! Set start_date to a later date.')
            # Renormalize the dataset and drop last line
            for kw in kw_list:
                beg = new_date
                end = old_date - timedelta(days=1)
        
                # Since we might encounter zeros, we loop over the
                # overlap until we find a non-zero element
                #for t in range(1,overlap+1):
                    ##print('t = ',t)
                    ##print(temp_df[kw].iloc[-t])
                    #if temp_df[kw].iloc[-t] != 0:
                        #scaling = interest_over_time_df[kw].iloc[t-1]/temp_df[kw].iloc[-t]
                        ##print('Found non-zero overlap!')
                        #break
                    #elif t == overlap:
                        #print('Did not find non-zero overlap, set scaling to zero! Increase Overlap!')
                        #scaling = 0
                # Apply scaling
                temp_df.loc[beg:end,kw]=temp_df.loc[beg:end,kw]#*scaling
            interest_over_time_df = pd.concat([temp_df[:-overlap],interest_over_time_df])
        
        # Save dataset
        
        #interest_over_time_df.to_csv(word+'.csv')
        
        
        zerocount = interest_over_time_df[interest_over_time_df[word]==0].count()['isPartial']
        
        if zerocount <= 50:
            zerocounter = 'high'
        elif 50 < zerocount < 150:
            zerocounter = 'medium'
        else:
            zerocounter = 'low'
    
       
        monitor = []
        monitor = {'zerocount' : zerocounter,
                   '1-day_step' : interest_over_time_df[word].iloc[-1]-interest_over_time_df[word].iloc[-2],
                   '2-day_step' : interest_over_time_df[word].iloc[-1]-interest_over_time_df[word].iloc[-3],
                   '3-day_step': interest_over_time_df[word].iloc[-1]-interest_over_time_df[word].iloc[-4],
                   'mean_step': interest_over_time_df[word].mean()}
      
        monitordf = pd.DataFrame(monitor, index = [word])
        
        return(monitordf)
    
 

    #interest_over_time_df.to_sql('CymaBay_Therapeutics', engine, if_exists = 'append')
    
#mddf, zzk = google.google_dow('CBAY stock')
#print(mddf)