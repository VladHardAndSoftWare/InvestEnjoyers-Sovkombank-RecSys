import datetime
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog

from Methods.sum_dividends_in_interval import sum_dividends_in_interval_func, historical_dividends_in_interval_func
from Methods.date_shares_prices import date_shares_prices_func
from Methods.sum_bond_coupons_in_interval import sum_bond_coupons_in_interval_func
from Methods.historical_shares_prices import historical_shares_prices_func

def profitability_share_by_n_periods(ticker, n, from_timestemp, to_timestemp):
    Div=sum_dividends_in_interval_func(ticker, from_timestemp, to_timestemp)
    C1=date_shares_prices_func(ticker, to_timestemp)
    C0=date_shares_prices_func(ticker, from_timestemp)
    if C1!=None and C0!=None: 
        middle_profit=(C1-C0+Div)/C0/n
    else: middle_profit=None
    return middle_profit

def profitability_long_bonds_by_n_periods(ticker, n, from_timestemp, to_timestemp):
    Div=sum_bond_coupons_in_interval_func(ticker, from_timestemp, to_timestemp)
    C1=date_shares_prices_func(ticker, to_timestemp)
    C0=date_shares_prices_func(ticker, from_timestemp)
    if C1!=None and C0!=None: 
        middle_profit=(C1-C0+Div)/C0/n
    else: middle_profit=None
    return middle_profit

def profitability_metal_by_n_periods(ticker, n, from_timestemp, to_timestemp):
    C1=date_shares_prices_func(ticker, to_timestemp)
    C0=date_shares_prices_func(ticker, from_timestemp)
    middle_profit=(C1-C0)/C0/n
    return middle_profit

def risk(ticker, from_timestemp, to_timestemp):
    _, y = historical_shares_prices_func(ticker, from_timestemp, to_timestemp, CandleInterval.CANDLE_INTERVAL_WEEK)
    std=np.std(np.asarray(y))
    return std

def normalize_list(x: list):
    if x==[]: return None 
    x_min=min(x)
    x_max=max(x)
    if x_max==x_min: return None
    norm=[]
    for i in x:
        norm.append((i-x_min)/(x_max-x_min))
    return norm

def Simplex_Method(D1,R1,D2,R2,D,R):
    obj = [-D1,-D2]
    
    lhs_ineq = [[ R1,  R2]]
    rhs_ineq = [R]  # правая сторона неравенства

    lhs_eq = [[1., 1.]]  # левая сторона равенства
    rhs_eq = [1.]       # правая сторона равенства
    
    bnd = [(0, float("inf")), (0, float("inf"))]  # Границы
    
    opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
              A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
              method="revised simplex")
    if opt.success==False:
        print('Оптимизационная задача неразрешима. Пожалуйста подкорректируйте значение risk_tolerance')
        return
    return opt.x[0], opt.x[1], -opt.fun

def number_actives(allocation, inishial_capital):
    allocation_sum=[]
    for i in allocation:
        allocation_sum.append(i*inishial_capital)
    number_actives=[]
    max_price_actives=[50000.,50000., 50000., 50000.]#Рассчитать максимальную стоимость актива*10
    for i in range(4):
        k=int(allocation_sum[i]/max_price_actives[i])
        if k>10: k=10
        number_actives.append(k)
    if(number_actives[2]!=0):number_actives[2]=2# На бирже только 2 драг. металла
    return number_actives

def preference_adjustment(number_shares, profession, preference):
    if profession!=None: number_profession=int(number_shares*0.2) #20% акций аналогичных отрасли профессии
    else: number_profession=0
    if preference!=None:number_preference=int(number_shares*0.3) #30% акций по отраслевым предпочтениям
    else: number_preference=0
    number_common=number_shares-number_profession-number_preference #50 наиболее доходных из всех
    return number_common, number_profession, number_preference