import datetime
import matplotlib.pyplot as plt
import numpy as np

from Models.Investor import Investor
#Рассчет процента "периодической" ожидаемой доходности по задачам пользователя.
#initial_capital - S0, regular_investments - Sr, horizon - H, final_goal - S, period - T

#Расчет финальной суммы капитала при известном проценте доходности 
def expected_capital(investor: Investor, r):
    n=investor.planning_horizon
    S=investor.initial_capital  
    for k in range(n):
        S=(S+investor.monthly_investment)*(r+1)
    return S

#Расчет процента доходности по сумме капитала(Численный)
def iter_expected_profitability(investor: Investor):
    n=investor.planning_horizon
    h=0.001 #Необходимая точность 
    A=-2; B=2 #границы r
    Siter=0
    #k=0
    while(np.abs(investor.goal-Siter)>=investor.goal*h):
        middle=A+((B-A)/2)
        Siter=expected_capital(investor, middle)
        if (investor.goal-Siter>=0): A=middle
        else: B=middle
        #k+=1
        #print(k, Siter, middle)
    return middle

#Расчет процента доходности по сумме капитала(Алгебраический, по приближенной формуле)
#Работает плохо, погрешность становится слишком большой при r>0.01 
def native_expected_profitability(S0, Sr, S, H, T):
    n=H/T
    r=((S-S0-Sr*n)/(S0+Sr*n))*(1/(n-1))
    return r

#Расчет допустимого риска для инвестора
#Cамооценка уровня риска[1:10], Уровень знаний, опыт[1:5]
def real_risk_tolerance(investor: Investor, R_max, R_min):
    min_risk=R_min #Минимальный риск по всем типам бумаг
    max_risk=R_max #Максимальный
    k=0.5+0.1*investor.financial_knowledge #Поправка на знания инвестора
    r=min_risk+(max_risk-min_risk)/10*k*investor.risk_tolerance 
    return r
