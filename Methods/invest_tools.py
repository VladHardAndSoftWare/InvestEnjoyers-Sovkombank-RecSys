import datetime
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog

from Methods.sum_dividends_in_interval import sum_dividends_in_interval_func, historical_dividends_in_interval_func
from Methods.date_shares_prices import date_shares_prices_func
from Methods.historical_shares_prices import historical_shares_prices_func

def profitability_share_by_n_periods(ticker, n, from_timestemp, to_timestemp):
    Div=sum_dividends_in_interval_func(ticker, from_timestemp, to_timestemp)
    C1=date_shares_prices_func(ticker, to_timestemp)
    C0=date_shares_prices_func(ticker, from_timestemp)
    middle_profit=(C1-C0+Div)/C0/n
    return middle_profit

def profitability_currency_by_n_periods(ticker, n, from_timestemp, to_timestemp):
    C1=date_shares_prices_func(ticker, to_timestemp)
    C0=date_shares_prices_func(ticker, from_timestemp)
    middle_profit=(C1-C0)/C0/n
    return middle_profit

def risk(ticker, from_timestemp, to_timestemp):
    _, y = historical_shares_prices_func(ticker, from_timestemp, to_timestemp, CandleInterval.CANDLE_INTERVAL_WEEK)
    std=np.std(np.asarray(y))
    return std

def normalize_list(x: list):
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
    return opt.x[0], opt.x[1], opt.fun