import datetime
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval
import matplotlib.pyplot as plt

from Methods.historical_shares_prices import historical_shares_prices_func

# На вход figi номер акции, начальный тайм стемп, конечный таймстеп, интервал c какой переодичностью беруться данные
# На выход масив таймстемпов, массив цены акции
x, y = historical_shares_prices_func("BBG004730N88", datetime.datetime(2022, 11, 4, tzinfo=datetime.timezone.utc), now(), CandleInterval.CANDLE_INTERVAL_HOUR)

plt.plot(x, y)
plt.show()