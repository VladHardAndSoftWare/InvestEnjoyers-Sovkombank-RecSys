import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.signal import find_peaks
from figi_converter import figi_converter_share_func

from get_securities_lists import all_rub_shares
from historical_shares_prices import historical_shares_prices_func

from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval

# Загрузка исторических данных цен на акции (замените эту часть на свой источник данных)
# Пример данных в формате CSV: дата и цена закрытия
# data = pd.read_csv('stock_prices.csv')
# data['Date'] = pd.to_datetime(data['Date'])
# data.set_index('Date', inplace=True)

# # Построение временного ряда цен на акции
# prices = data['Close']

IMOEX_figi = figi_converter_share_func("TQBR","MOEX")

x, y = historical_shares_prices_func(IMOEX_figi, datetime.datetime(2012, 11, 4, tzinfo=datetime.timezone.utc), now(), CandleInterval.CANDLE_INTERVAL_MONTH)

time_series = pd.Series(y)
# x = pd.Series(x).set_index('Date', inplace=True)
# Вычисление скользящей средней
rolling_mean = time_series.rolling(window=20).mean()

peaks, peaks_details = find_peaks(rolling_mean, height=0)
valleys, valleys_details = find_peaks(-rolling_mean, height=0)

def find_local_extrema(nums):
    extrema_max = []
    extrema_min = []

    if len(nums) < 3:
        return extrema_max, extrema_min

    for i in range(1, len(nums) - 1):
        if nums[i] > nums[i - 1] and nums[i] > nums[i + 1]:
            extrema_max.append(i)
        elif nums[i] < nums[i - 1] and nums[i] < nums[i + 1]:
            extrema_min.append(i)

    return extrema_max, extrema_min

extrema_max, extrema_min = find_local_extrema(rolling_mean)

# print(extrema_max)
print(extrema_min)
print(peaks)
print(peaks_details)
print(valleys)
print(valleys_details)

plt.figure(figsize=(12, 6))
plt.plot(x, time_series, label='IMOEX')
plt.plot(x, rolling_mean, label='Скользящая средняя (20 дней)')
plt.legend()
plt.title('Анализ циклов по IMOEX')
plt.xlabel('Дата')
plt.ylabel('Цена, ₽')

plt.plot(np.array(x)[peaks], rolling_mean.iloc[peaks], 'ro')
# plt.plot(np.array(x)[extrema_max], rolling_mean.iloc[extrema_max], 'ro')
# plt.plot(np.array(x)[valleys], rolling_mean.iloc[valleys], 'go')
plt.plot(np.array(x)[extrema_min], rolling_mean.iloc[extrema_min], 'go')

plt.show()

# Расчет циклических компонентов
correlation = np.correlate(time_series, time_series, mode='full')
decomposition = sm.tsa.seasonal_decompose(rolling_mean.dropna(), model='additive', period=4)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid
print(decomposition.nobs)

plt.figure(figsize=(12, 6))
plt.subplot(411)
plt.plot(x, rolling_mean, label='Цены на акции')
plt.legend()
plt.subplot(412)
plt.plot(x, trend, label='Тренд')
plt.legend()
plt.subplot(413)
plt.plot(x, seasonal, label='Сезонные колебания')
plt.legend()
plt.subplot(414)
plt.plot(x, residual, label='Остатки')
plt.legend()
plt.tight_layout()
plt.show()


