import datetime
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval
from tinkoff.invest import InstrumentRequest
import matplotlib.pyplot as plt
import numpy as np

from Methods import invest_tools as it
from Methods.sum_dividends_in_interval import sum_dividends_in_interval_func, historical_dividends_in_interval_func
from Methods.date_shares_prices import date_shares_prices_func
from Methods.historical_shares_prices import historical_shares_prices_func
from Methods.get_securities_lists import all_rub_shares, all_rub_bonds

from Models import Investor, Portfolio

from tinkoff.invest import CandleInterval, Client
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ['TINKOFF_API_KEY']
#x, y = historical_shares_prices_func("BBG004730N88", datetime.datetime(2023, 11, 1, tzinfo=datetime.timezone.utc), now(), CandleInterval.CANDLE_INTERVAL_DAY)

#x, y = historical_shares_prices_func("BBG004730JJ5", datetime.datetime(2023, 11, 1, tzinfo=datetime.timezone.utc), now(), CandleInterval.CANDLE_INTERVAL_DAY)
#z=it.normalize_list(y)
#plt.plot(x, y)
#plt.show()

#print(it.risk("BBG004730N88", datetime.datetime(2023, 10, 1, tzinfo=datetime.timezone.utc), now()))
#print(it.profitability_by_n_periods('BBG004730N88', 5, datetime.datetime(2018, 11, 5, tzinfo=datetime.timezone.utc), now()))

#indicative_papers=["BBG004730JJ5", "BBG01BJBR2W0", "BBG000VJ5YR4"]#
from_timestamp=datetime.datetime(2018, 11, 1, tzinfo=datetime.timezone.utc)
to_timestamp=datetime.datetime(2023, 11, 1, tzinfo=datetime.timezone.utc)

test_investor=Investor(
    name= "Елена",
    age=30,
    profession="CEO",
    financial_knowledge=3,
    #risk_tolerance=0.2,
    initial_capital=100,
    monthly_investment=10,
    planning_horizon=0,
    goal="грудь"
)

d=[]
r=[[1.0, 0.27205180825510006, 0.0]]
one=[1., 1., 1.0]
D=[]
R=[]

A=np.array([d, r, one])
b=[D, R, 1.]

#alloc=np.linalg.solve(A, b)
