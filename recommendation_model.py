import datetime
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval
from tinkoff.invest import InstrumentRequest
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Methods import invest_tools as it
from Methods import investor_analysis as ia
import risk_calculation as rc
from Methods import get_data_instruments as gd
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
TOKEN = os.environ['TINKOFF_API_KEY']#Ключ для доступа к ТинькоффAPI, из которого мы выгружаем бумаги и котировки

#ВВОД ТЕСТОВЫХ ДАННЫХ
#Данные от инвестора
test_investor=Investor(
    name="Дмитрий",
    age=23,
    profession='',
    preference='',
    financial_knowledge=3.,
    risk_tolerance=7.,
    initial_capital=5000000.,
    monthly_investment=60000,
    planning_horizon=17,
    goal=40000000 #не менее 100000 в месяц. С чистой доходностью 1% в месяц, нужно иметь на счете 10 млн руб.
    #Учитывая среднегодовую инфляцию 8.5%, через 17 лет ему нужно ~40 млн.р 
)

#Тестовый временной промежуток. Портфель собирается в момент to_t
from_t=datetime.datetime(2022, 11, 1, tzinfo=datetime.timezone.utc)
to_t=datetime.datetime(2023, 11, 1, tzinfo=datetime.timezone.utc)

#Текущий экономический цикл: 
#   Экономика растет? - Да(1)/Нет(0)
#   Инфляция растет? - Да(1)/Нет(0)
cycle=[1,1]

#Процент влияния экономического цикла на аллокацию. Выбран интуитивно. 
#Можно, и вероятно нужно, найти оптимальный эксперементально.(Предложение по развитию!)
cycle_positive_factor=0.7
cycle_negative_factor=0.3

#ОСНОВНАЯ ФУНКЦИЯ
def recommendation_model(investor: Investor, cycle, from_timestamp, to_timestamp):
    #ЗАГРУЗКА ВСЕХ ДОСТУПНЫХ БУМАГ. РАССЧЕТ ИХ ДОХОДНОСТЕЙ И РИСКОВ
    data_share=pd.read_csv('Data/share_data1.csv') #gd.get_data_share(from_timestamp, to_timestamp, N)
    data_currency=[]
    data_short_bond=[]
    data_long_bond=[]
    
    #РАССЧЕТ АЛЛОКАЦИИ
    #Ожидаемая ежегодная доходность и предпологаемый риск инвестора
    D=ia.iter_expected_profitability(investor)
    R=ia.real_risk_tolerance(investor)
    
    #Ожидаемые риски и доходности типов бумаг
    D_sh=np.mean(data_share['yarly_mean_profiit']) #it.profitability_share_by_n_periods('BBG333333333',3,from_timestamp,to_timestamp)#есть только за 3 года
    R_sh=np.mean(data_share['risk']) #rc.find_middle_risk_shares(from_timestamp,to_timestamp)
    
    D_cu=0.2 #it.profitability_currency_by_n_periods(from_timestamp,to_timestamp)
    R_cu=0.1 #rc.find_risk_gold(from_timestamp,to_timestamp)
    
    D_sb=0.15 #it.profitability_short_bonds_by_n_periods
    R_sb=0.1 #rc.find_middle_risk_short_bonds
    
    D_lb=0.1 #it.profitability_long_bonds_by_n_periods
    R_lb=0.05 #rc.find_middle_risk_long_bonds
    
    #Решение оптимизационной задачи - рассчет аллокации, и наилучшей ожидаемой доходности
    if (cycle==[1, 1]):
        x=it.Simplex_Method(D_sh, R_sh, D_cu, R_cu, D, R)
        alloc_sh, alloc_cu, D_opti_pos = np.asarray(it.Simplex_Method(D_sh, R_sh, D_cu, R_cu, D, R))*cycle_positive_factor
        alloc_sb, alloc_lb, D_opti_neg = np.asarray(it.Simplex_Method(D_sb, R_sb, D_lb, R_lb, D, R))*cycle_negative_factor
    elif (cycle==[1, 0]):
        alloc_sh, alloc_lb, D_opti_pos = np.asarray(it.Simplex_Method(D_sh, R_sh, D_lb, R_lb, D, R))*cycle_positive_factor
        alloc_sb, alloc_cu, D_opti_neg = np.asarray(it.Simplex_Method(D_sb, R_sb, D_cu, R_cu, D, R))*cycle_negative_factor
    elif (cycle==[0, 1]):
        alloc_sb, alloc_cu, D_opti_pos = np.asarray(it.Simplex_Method(D_sb, R_sb, D_cu, R_cu, D, R))*cycle_positive_factor
        alloc_sh, alloc_lb, D_opti_neg = np.asarray(it.Simplex_Method(D_sh, R_sh, D_lb, R_lb, D, R))*cycle_negative_factor
    elif (cycle==[0, 0]):
        alloc_sb, alloc_lb, D_opti_pos = np.asarray(it.Simplex_Method(D_sb, R_sb, D_lb, R_lb, D, R))*cycle_positive_factor
        alloc_sh, alloc_cu, D_opti_neg = np.asarray(it.Simplex_Method(D_sh, R_sh, D_cu, R_cu, D, R))*cycle_negative_factor
    
    allocation=[alloc_sh, alloc_sb, alloc_cu, alloc_lb]
    D_opti=D_opti_neg+D_opti_pos
    if (D_opti<D):
        print('С установленным уровнем риска, доходность портфеля ожидается = ', D_opti,'. Пожалуйста скорректируйте вашу цель или уровень риска.')
        #доходность пересчитать в конечную цель
        return
    
    #ОПРЕДЕЛЕНИЕ ЧИСЛА РАЗЛИЧНЫХ БУМАГ ОДНОГО ТИПА
    number_actives=it.number_actives(allocation, investor.initial_capital)
    number_shares_by_preferences=it.preference_adjustment(number_actives[0], test_investor.profession, test_investor.preference)
    
    #CОСТАВЛЕНИЕ ТЕСТОВОГО ПОРТФЕЛЯ
    #Добавление акций с наилучшей доходностью
    df=data_share.sort_values(by = ['yarly_mean_profiit'], ascending = [ False ]).reset_index().drop(columns=['Unnamed: 0', 'index'])
    portfolio=pd.DataFrame(columns=['figi', 'ticker','name','sector', 'persent', 'type'])
    for i in range(number_actives[0]):
        portfolio.loc[len(portfolio.index)] = [df.loc[i, 'figi'], df.loc[i, 'ticker'], df.loc[i, 'name'],
                                               df.loc[i, 'sector'], allocation[0]/number_actives[0]*100, 'share']

    print(portfolio)    
        
    portfolio=[]
    diversification=[]
    return portfolio, allocation, D_opti, diversification

print(recommendation_model(test_investor, cycle, from_t, to_t))

