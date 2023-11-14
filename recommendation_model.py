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
from Methods.get_securities_lists import all_rub_shares, all_gov_bonds

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
    profession='consumer',#Пустое = None
    preference='energy',#Пустое = None
    financial_knowledge=5.,
    risk_tolerance=9.,
    initial_capital=5000000.,
    monthly_investment=60000,
    planning_horizon=17,
    goal=40000000 #не менее 100000 в месяц. С чистой доходностью 1% в месяц, нужно иметь на счете 10 млн руб.
    #Учитывая среднегодовую инфляцию 8.5%, через 17 лет ему нужно ~40 млн.р 
)

#Тестовый временной промежуток. Портфель собирается в момент to_t
from_t=datetime.datetime(2022, 11, 1, tzinfo=datetime.timezone.utc)
to_t=datetime.datetime(2023, 11, 1, tzinfo=datetime.timezone.utc)
N=1

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
    #data_share=pd.read_csv('Data/share_data1.csv') #gd.get_data_share(from_timestamp, to_timestamp, N)
    #data_metals=pd.read_csv('Data/metals_data1.csv') #gd.get_data_metals(from_timestamp, to_timestamp, N)
    #data_short_bonds=pd.read_csv('Data/short_bonds_data1.csv') #gd.get_data_metals(from_timestamp, to_timestamp, N)
    #data_long_bond=pd.read_csv('Data/gov_bond_data1.csv') #gd.get_data_long_bond(from_timestamp, to_timestamp, N)
    
    print('Расчет доходностей акций. Ожидайте ~3 мин')
    data_share=gd.get_data_share(from_timestamp, to_timestamp, N)
    print('Расчет доходностей металлов')
    data_metals=gd.get_data_metals(from_timestamp, to_timestamp, N)
    print('Расчет доходностей облигаций. Ожидайте ~2 мин')
    data_short_bonds=gd.get_data_metals(from_timestamp, to_timestamp, N)
    print('Расчет доходностей государственных облигаций. Ожидайте ~2 мин')
    data_long_bond=gd.get_data_long_bond(from_timestamp, to_timestamp, N)
    
    #АЛЛОКАЦИЯ
    #Ожидаемые риски и доходности типов бумаг
    D_sh=np.mean(data_share['yarly_mean_profiit']) 
    R_sh=np.mean(data_share['risk']) 
    
    D_cu=np.mean(data_metals['yarly_mean_profiit']) 
    R_cu=np.mean(data_metals['risk']) 
    
    D_sb=np.mean(data_short_bonds['yarly_mean_profiit']) 
    R_sb=np.mean(data_short_bonds['risk']) 
    
    D_lb=np.mean(data_long_bond['yarly_mean_profiit']) 
    R_lb=np.mean(data_long_bond['risk']) 
    
    #Ожидаемая ежегодная доходность и предпологаемый риск инвестора
    D=ia.iter_expected_profitability(investor)
    R_max=max(R_sh,R_sb,R_cu,R_lb)
    R_min=min(R_sh,R_sb,R_cu,R_lb)
    R=ia.real_risk_tolerance(investor, R_max, R_min)
    
    #Решение оптимизационной задачи - рассчет аллокации, и наилучшей ожидаемой доходности
    if (cycle==[1, 1]):
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
    allocation_df=pd.DataFrame({'Процент акций в портфеле': [allocation[0]],
                                    'Процент краткосрочных облигаций в портфеле': [allocation[1]],
                                    'Процент драгоценных металлов в портфеле': [allocation[2]],
                                    'Процент долгосрочных облигаций в портфеле': [allocation[3]],
        }).T
    
    #ДИВЕРСИФИКАЦИЯ
    number_actives=it.number_actives(allocation, investor.initial_capital)
    number_common, number_profession, number_preference=it.preference_adjustment(number_actives[0], test_investor.profession, test_investor.preference)
    diversification_df=pd.DataFrame({'Число различных акций по отрасли профессии': [number_profession],
                                    'Число различных акций по предпочтениям': [number_preference],
                                    'Число различных акций по наибольшей доходности': [number_common],
                                    'Общее число различных акций': [number_actives[0]],
                                    'Общее число различных краткосрочных облигаций': [number_actives[1]],
                                    'Общее число различных драг. металлов': [number_actives[2]],
                                    'Общее число различных долгосрочных облигаций': [number_actives[3]],
        }).T

    #CОСТАВЛЕНИЕ ТЕСТОВОГО ПОРТФЕЛЯ
    portfolio=pd.DataFrame(columns=['figi', 'ticker','name','sector', 'persent', 'type'])
    
    #Добавление акций с наилучшей доходностью, по отрасли профессии
    if test_investor.profession!=None:
        exept_prof=[]
        df=data_share.loc[data_share['sector'] == test_investor.profession]
        df=df.sort_values(by = ['yarly_mean_profiit'], ascending = [ False ]).reset_index().drop(columns=['index'])
        for i in range(number_profession):
            portfolio.loc[len(portfolio.index)] = [df.loc[i, 'figi'], df.loc[i, 'ticker'], df.loc[i, 'name'],
                                               df.loc[i, 'sector'], allocation[0]/number_actives[0]*100, 'share']
            exept_prof.append(df.loc[i, 'figi'])
        for i in exept_prof:
            data_share=data_share.loc[data_share['figi'] != i].reset_index().drop(columns=['index'])
    
    #Добавление акций с наилучшей доходностью, по предпочтениям
    if test_investor.preference!=None:
        exept_prof=[]
        df=data_share.loc[data_share['sector'] == test_investor.preference]
        df=df.sort_values(by = ['yarly_mean_profiit'], ascending = [ False ]).reset_index().drop(columns=['index'])
        for i in range(number_preference):
            portfolio.loc[len(portfolio.index)] = [df.loc[i, 'figi'], df.loc[i, 'ticker'], df.loc[i, 'name'],
                                               df.loc[i, 'sector'], allocation[0]/number_actives[0]*100, 'share']
            exept_prof.append(df.loc[i, 'figi'])
        for i in exept_prof:
            data_share=data_share.loc[data_share['figi'] != i].reset_index().drop(columns=['index'])
    
    #Добавление остальных акций с наилучшей доходностью
    df=data_share.sort_values(by = ['yarly_mean_profiit'], ascending = [ False ]).reset_index().drop(columns=['index'])
    for i in range(number_common):
        portfolio.loc[len(portfolio.index)] = [df.loc[i, 'figi'], df.loc[i, 'ticker'], df.loc[i, 'name'],
                                               df.loc[i, 'sector'], allocation[0]/number_actives[0]*100, 'share']
    
    #Добавление краткосрочных облигаций с наилучшей доходностью
    df=data_short_bonds.sort_values(by = ['yarly_mean_profiit'], ascending = [ False ]).reset_index().drop(columns=['index'])
    for i in range(number_actives[1]):
        portfolio.loc[len(portfolio.index)] = [df.loc[i, 'figi'], df.loc[i, 'ticker'], df.loc[i, 'name'],
                                               'short', allocation[1]/number_actives[1]*100, 'bond']
    
    #Добавление драгоценных металлов с наилучшей доходностью
    df=data_metals.sort_values(by = ['yarly_mean_profiit'], ascending = [ False ]).reset_index().drop(columns=['index'])
    for i in range(number_actives[2]):
        portfolio.loc[len(portfolio.index)] = [df.loc[i, 'figi'], df.loc[i, 'ticker'], df.loc[i, 'name'],
                                               'precious metals', allocation[2]/number_actives[2]*100, 'currency']
    
    #Добавление долгосрочных государственных облигаций с наилучшей доходностью
    df=data_long_bond.sort_values(by = ['yarly_mean_profiit'], ascending = [ False ]).reset_index().drop(columns=['index'])
    for i in range(number_actives[3]):
        portfolio.loc[len(portfolio.index)] = [df.loc[i, 'figi'], df.loc[i, 'ticker'], df.loc[i, 'name'],
                                               'governments', allocation[3]/number_actives[3]*100, 'bond']
    
    return portfolio, allocation_df, D_opti, diversification_df

portfolio, allocation_df, D_opti, diversification_df = recommendation_model(test_investor, cycle, from_t, to_t)
print("\nОЖИДАЕМАЯ ГОДОВАЯ ДОХОДНОСТЬ ПОРТФЕЛЯ, % = ",D_opti*100)
print("\nРЕКОМЕНДУЕМАЯ АЛЛОКАЦИЯ",allocation_df)
print("\nРЕКОМЕНДУЕМАЯ ДИВЕРСИФИКАЦИЯ",diversification_df)
print("\nПРИМЕР ПОРТФЕЛЯ\n",portfolio)
