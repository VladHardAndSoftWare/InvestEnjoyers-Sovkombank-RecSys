import datetime
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval
from tinkoff.invest import InstrumentRequest
import matplotlib.pyplot as plt
import numpy as np

from Methods import invest_tools as it
from Methods import investor_analysis as ia
import risk_calculation as rc
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
from_t=datetime.datetime(2020, 11, 1, tzinfo=datetime.timezone.utc)
to_t=datetime.datetime(2023, 11, 1, tzinfo=datetime.timezone.utc)
cycle=[1,1]
cycle_positive_factor=0.7
cycle_negative_factor=0.3

def recommendation_model(investor: Investor, cycle, from_timestamp, to_timestamp):
    D=ia.iter_expected_profitability(investor)
    R=ia.real_risk_tolerance(investor)
    
    D_sh=it.profitability_share_by_n_periods('BBG333333333',3,from_timestamp,to_timestamp)#есть только за 3 года
    R_sh=rc.find_middle_risk_shares(from_timestamp,to_timestamp)
    
    D_cu=it.profitability_currency_by_n_periods(from_timestamp,to_timestamp)
    R_cu=rc.find_risk_gold(from_timestamp,to_timestamp)
    
    D_sb=0.1 #it.profitability_short_bonds_by_n_periods
    R_sb=0.1 #rc.find_middle_risk_short_bonds
    
    D_lb=0.05 #it.profitability_long_bonds_by_n_periods
    R_lb=0.05 #rc.find_middle_risk_long_bonds
    
    if (cycle==[1, 1]):
        alloc_sh, alloc_cu, D_opti_pos = it.Simplex_Method(D_sh, R_sh, D_cu, R_cu, D, R)*cycle_positive_factor
        alloc_sb, alloc_lb, D_opti_neg = it.Simplex_Method(D_sb, R_sb, D_lb, R_lb, D, R)*cycle_negative_factor
    elif (cycle==[1, 0]):
        alloc_sh, alloc_lb, D_opti_pos = it.Simplex_Method(D_sh, R_sh, D_lb, R_lb, D, R)*cycle_positive_factor
        alloc_sb, alloc_cu, D_opti_neg = it.Simplex_Method(D_sb, R_sb, D_cu, R_cu, D, R)*cycle_negative_factor
    elif (cycle==[0, 1]):
        alloc_sb, alloc_cu, D_opti_pos = it.Simplex_Method(D_sb, R_sb, D_cu, R_cu, D, R)*cycle_positive_factor
        alloc_sh, alloc_lb, D_opti_neg = it.Simplex_Method(D_sh, R_sh, D_lb, R_lb, D, R)*cycle_negative_factor
    elif (cycle==[0, 0]):
        alloc_sb, alloc_lb, D_opti_pos = it.Simplex_Method(D_sb, R_sb, D_lb, R_lb, D, R)*cycle_positive_factor
        alloc_sh, alloc_cu, D_opti_neg = it.Simplex_Method(D_sh, R_sh, D_cu, R_cu, D, R)*cycle_negative_factor
    
    allocation=[alloc_sh, alloc_sb, alloc_cu, alloc_lb]
    D_opti=D_opti_neg+D_opti_pos
    if (D_opti<D):
        print('С установленным уровнем риска, доходность портфеля ожидается = ', D_opti,'. Пожалуйста скорректируйте вашу цель или уровень риска.')
        #доходность пересчитать в конечную цель
        return
    
    portfolio=[]
    allocation=[]
    diversification=[]
    return portfolio, allocation, D_opti, diversification

#recommendation_model(test_investor, cycle, from_t, to_t)
print(it.Simplex_Method1())