import datetime
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval
from tinkoff.invest import InstrumentRequest
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from Methods import invest_tools as it
from Methods.historical_shares_prices import historical_shares_prices_func
from Methods.get_securities_lists import all_rub_shares, all_rub_bonds


def get_data_share(from_timestamp, to_timestamp, N):
    data=pd.DataFrame(columns=['figi', 'ticker','name','sector', 'yarly_mean_profiit', 'risk'])
    
    shares_list=all_rub_shares()
    data['figi']=shares_list[0]
    data['ticker']=shares_list[1]
    data['name']=shares_list[2]
    data['sector']=shares_list[4]
    
    yarly_mean_profiit=[]
    risk=[]
    k=0
    for share in data['figi']:
        profit=it.profitability_share_by_n_periods(share, N, from_timestamp, to_timestamp)
        yarly_mean_profiit.append(profit)
        
        _, y = historical_shares_prices_func(share, from_timestamp, to_timestamp, CandleInterval.CANDLE_INTERVAL_WEEK)
        y_norm=it.normalize_list(y)
        if y_norm!=None:
            risk.append(np.std(np.asarray(y_norm)))
        else: risk.append(None)
        
        time.sleep(1)
        #print(k)
        #k+=1
    data['yarly_mean_profiit']=yarly_mean_profiit
    data['risk']=risk
    data=data.dropna().reset_index().drop(columns=['Unnamed: 0', 'index'])
    
    return data

