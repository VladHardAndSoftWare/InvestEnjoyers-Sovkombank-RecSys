import datetime
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval
import matplotlib.pyplot as plt

from Methods.historical_shares_prices import historical_shares_prices_func
from Methods.date_shares_prices import date_shares_prices_func
from Methods.sum_dividends_in_interval import sum_dividends_in_interval_func

# =====Историческая цена акций======
# На вход figi номер акции, начальный тайм стемп, конечный таймстеп, интервал c какой переодичностью беруться данные
# На выход масив таймстемпов, массив цены акции
x, y = historical_shares_prices_func("BBG004730N88", datetime.datetime(2012, 11, 4, tzinfo=datetime.timezone.utc), now(), CandleInterval.CANDLE_INTERVAL_MONTH)

plt.plot(x, y)
plt.show()

# =====Стоимость ценной бумаги в момент времени t=====
# На вход figi номер акции, тайм стемпна момент которого мы хотим узнать цену
# На выход цена акции на момент времени timestamp
C = date_shares_prices_func("BBG004730N88", datetime.datetime(2022, 11, 4, tzinfo=datetime.timezone.utc))

print(C)

# =====Cумма дивидендов в интервали времени=====
sum_div = sum_dividends_in_interval_func("BBG004730N88", datetime.datetime(2012, 11, 4, tzinfo=datetime.timezone.utc), now())

print(sum_div)