import datetime
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval
from tinkoff.invest import InstrumentRequest
import matplotlib.pyplot as plt
import numpy as np

from Methods import invest_tools as it
from Methods import investor_analysis as ia
from Methods.sum_dividends_in_interval import sum_dividends_in_interval_func, historical_dividends_in_interval_func
from Methods.date_shares_prices import date_shares_prices_func
from Methods.historical_shares_prices import historical_shares_prices_func
from Methods.get_securities_lists import all_rub_shares, all_rub_bonds

from Models.Investor import Investor
from Models.Portfolio import Portfolio

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
from_timestamp_1=datetime.datetime(2020, 11, 1, tzinfo=datetime.timezone.utc)
to_timestamp=datetime.datetime(2023, 11, 1, tzinfo=datetime.timezone.utc)

test_investor=Investor(
    name="Дмитрий",
    age=23,
    profession="teacher",
    financial_knowledge=3.,
    risk_tolerance=7.,#на самом деле меньше
    initial_capital=5000000.,
    monthly_investment=60000,
    planning_horizon=17,
    goal=40000000 #не менее 100000 в месяц. С чистой доходностью 1% в месяц, нужно иметь на счете 10 млн руб.
    #Учитывая среднегодовую инфляцию 8.5%, через 17 лет ему нужно ~40 млн.р 
)
test_investor2=Investor(
    name="ЛжеДмитрий",
    age=23,
    profession="teacher",
    financial_knowledge=3.,
    risk_tolerance=7.,
    initial_capital=100000.,
    monthly_investment=5000,
    #planning_horizon=37,
    goal=200000 
)
dA=0.35 #it.profitability_share_by_n_periods('BBG333333333',3,from_timestamp_1,to_timestamp)#есть только за 3 года
dO=0.09 #it.profitability_bond_by_n_periods('',5,from_timestamp,to_timestamp)
dZ=it.profitability_currency_by_n_periods('BBG000VJ5YR4',5,from_timestamp,to_timestamp)
d=[dA, dO, dZ]
r0=[0.23972445089345876, 0.1569289386, 0.19128898294386373]#Рассчитывается в файле risk_calculation
r=it.normalize_list(r0)
one=[1., 1., 1.]
D=ia.iter_expected_profitability(test_investor)
R=ia.real_risk_tolerance(test_investor)

A=np.array([d, r, one])
b=[D, R, 1.]

alloc=np.linalg.solve(A, b)

print('Доходности:',d, '   Ожидаемая дох-ть:',D)
print('Риски:',r, '   Ожидаемый риск:',R)
print('Аллокация:',alloc)