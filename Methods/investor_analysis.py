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