import datetime
import matplotlib.pyplot as plt
import numpy as np

#Рассчет процента "периодической" ожидаемой доходности по задачам пользователя.
#initial_capital - S0, regular_investments - Sr, horizon - H, final_goal - S, period - T

#Расчет финальной суммы капитала при известном проценте доходности 
def expected_capital(S0, Sr, r, H, T):
    n=int(H/T)
    S=S0  
    for k in range(n):
        S=(S+Sr)*(r+1)
    return S

#Расчет процента доходности по сумме капитала(Численный)
def iter_expected_profitability(S0, Sr, S, H, T):
    n=H/T
    h=0.001 #Необходимая точность 
    A=-2; B=2 #границы r
    Siter=0
    #k=0
    while(np.abs(S-Siter)>=S*h):
        middle=A+((B-A)/2)
        Siter=expected_capital(S0, Sr, middle, H, T)
        if (S-Siter>=0): A=middle
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
#r0 - самооценка уровня риска[1:10], k0 - уровень знаний, опыт[1:5]
r0=7
k0=3
def real_risk_tolerance(r0, k0):
    min_risk=3#Минимальный риск по всем типам бумаг(нормированный)
    max_risk=10#Максимальный
    k1=0.5+0.1*k0 #Поправка на знания инвестора
    r1=(max_risk-min_risk)/10*r0*k1 
    return r1
