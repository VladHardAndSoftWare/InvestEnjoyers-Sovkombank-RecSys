import datetime
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval
from tinkoff.invest import InstrumentRequest
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from Methods import invest_tools as it
from Methods import get_data_instruments as gd
from Methods.historical_shares_prices import historical_shares_prices_func
from Methods.get_securities_lists import all_rub_shares, all_rub_bonds

pd.set_option('display.max_rows', None)

from_t=datetime.datetime(2022, 11, 1, tzinfo=datetime.timezone.utc)
to_t=datetime.datetime(2023, 11, 1, tzinfo=datetime.timezone.utc)
N=1.

#x1=gd.get_data_share(from_t, to_t, 1)
#print(x1)
#x1.to_csv('Data/share_data_test1.csv')
#x2 = pd.read_csv('Data/share_data_test1.csv').dropna().reset_index().drop(columns=['Unnamed: 0', 'index'])
#print(x2)
#x2.to_csv('Data/share_data1.csv')



