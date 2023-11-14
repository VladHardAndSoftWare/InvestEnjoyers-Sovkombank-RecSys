import datetime
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval
from tinkoff.invest import InstrumentRequest
import matplotlib.pyplot as plt
import numpy as np
import time

from Methods import invest_tools as it
from Methods.historical_shares_prices import historical_shares_prices_func
from Methods.get_securities_lists import all_rub_shares, all_gov_bonds

#from_timestamp=datetime.datetime(2018, 11, 1, tzinfo=datetime.timezone.utc)
#to_timestamp=datetime.datetime(2023, 11, 1, tzinfo=datetime.timezone.utc)

def find_middle_risk_shares(from_timestamp, to_timestamp):
    shares=all_rub_shares()[0]
    risk_list=[]
    k=0
    for share in shares:
        time.sleep(1.5) #Обход ограничения числа запросов в мин(
        x, y = historical_shares_prices_func(share, from_timestamp, to_timestamp, CandleInterval.CANDLE_INTERVAL_WEEK)
        y_norm=it.normalize_list(y)
        if y_norm!=None:
            risk_list.append(np.std(np.asarray(y_norm)))
        k+=1
        print(k)
        #plt.plot(x, y_norm)
        #plt.show()
    mean_shares_risk=np.mean(np.asarray(risk_list))  
    return mean_shares_risk 

def find_middle_risk_government_bonds(from_timestamp, to_timestamp):
    bonds,_,bonds_name,_,_,_,bonds_duration=all_gov_bonds()
    risk_list=[]
    k=1
    for bond in bonds:
        time.sleep(1.5) #Обход ограничения числа запросов в мин(
        x, y = historical_shares_prices_func(bond, from_timestamp, to_timestamp, CandleInterval.CANDLE_INTERVAL_WEEK)
        y_norm=it.normalize_list(y)
        if y_norm!=None:
            std=np.std(np.asarray(y_norm))
            risk_list.append(std)
        print(k,bonds_name[k-1], bonds_duration[k-1], std)
        k+=1
        #plt.plot(x, y_norm)
        #plt.show()
    mean_bonds_risk=np.mean(np.asarray(risk_list))  
    mean_bonds_risk
    return mean_bonds_risk

def find_risk_gold(from_timestamp, to_timestamp): #Можно заменить средний по товарам/валютам, но нужно придумать принцип выбора: что включать, а что нет
    _,y = historical_shares_prices_func("BBG000VJ5YR4", from_timestamp, to_timestamp, CandleInterval.CANDLE_INTERVAL_WEEK)
    y_norm=it.normalize_list(y)
    std=np.std(np.asarray(y_norm))
    print(std) 
    return std

#risks=[]
#risks.append(find_middle_risk_shares())
#risks.append(find_middle_risk_government_bonds())
#risks.append(find_risk_gold())
#print(risks)
#print(it.normalize_list(risks))

#РЕЗУЛЬТАТ
#[0.23972445089345876, 0.204465939583233, 0.19128898294386373] ##0,1569289386 - среднее по 20 наименее рисковым облигациям
#[1.0, 0.27205180825510006, 0.0]

[0.23972445089345876, 0.1569289386, 0.19128898294386373]
