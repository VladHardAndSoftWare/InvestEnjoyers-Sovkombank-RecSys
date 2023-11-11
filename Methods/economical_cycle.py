import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.signal import find_peaks
from Methods.figi_converter import figi_converter_share_func

from Methods.get_securities_lists import all_rub_shares
from Methods.historical_shares_prices import historical_shares_prices_func

from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval

from Models.Cycle_period import Period

# Загрузка исторических данных цен на акции (замените эту часть на свой источник данных)
# Пример данных в формате CSV: дата и цена закрытия
# data = pd.read_csv('stock_prices.csv')
# data['Date'] = pd.to_datetime(data['Date'])
# data.set_index('Date', inplace=True)

# # Построение временного ряда цен на акции
# prices = data['Close']

# IMOEX_figi = figi_converter__func("TQBR","MOEX")
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


def economicle_cycle_graph():
	x, y = historical_shares_prices_func("BBG333333333", datetime.datetime(1999, 11, 4, tzinfo=datetime.timezone.utc), now(), CandleInterval.CANDLE_INTERVAL_MONTH)
# pandas
# pdImoex = pd.read_csv('data.csv')  

	time_series = pd.Series(y)
# x = pd.Series(x).set_index('Date', inplace=True)
# Вычисление скользящей средней
	rolling_mean = time_series.rolling(window=20).mean()

	peaks, peaks_details = find_peaks(rolling_mean, height=0)
	valleys, valleys_details = find_peaks(-rolling_mean, height=0)

	extrema_max, extrema_min = find_local_extrema(rolling_mean)

	import dateutil.relativedelta

	cycle_period = dateutil.relativedelta.relativedelta(months=6)
	bottom_period_begin = [min - cycle_period for min in np.array(x)[extrema_min]]
	bottom_period_end = [min + cycle_period  for min in np.array(x)[extrema_min]]
	top_period_begin = [min - cycle_period  for min in np.array(x)[peaks]]
	top_period_end = [min + cycle_period  for min in np.array(x)[peaks]]

	periods = []
	i = 0

	for period in bottom_period_begin:
		periods.append(Period("bottom_period_begin", period, "Дно", extrema_min[i]))
		i =+ 1
	i = 0
	for period in bottom_period_end:
		periods.append(Period("bottom_period_end", period, "Восстановление", extrema_min[i]))
		i =+ 1
	i = 0
	for period in top_period_begin:
		periods.append(Period("top_period_begin", period, "Пик", peaks[i]))
		i =+ 1
	i = 0
	for period in top_period_end:
		periods.append(Period("top_period_end", period, "Спад", peaks[i]))
		i =+ 1
	
	periods = sorted(periods, key=lambda item: item.value)
	period_line = []
	extrema_array = []
	for period in periods:
		print(period.extrema)
		period_line.append(period.value)
		extrema_array.append(period.extrema)
	print(period_line)

	# print(extrema_max)
	print(extrema_min)
	print(peaks)
	print(peaks_details)
	print(valleys)
	print(valleys_details)

	plt.figure(figsize=(12, 6))
	plt.plot(x, time_series, label='IMOEX')
	plt.plot(x, rolling_mean, label='Скользящая средняя (20 месяцев)')

	plt.title(f'Анализ циклов по IMOEX; Текущий экономический период: {periods[-1].period_type_ru}')
	plt.xlabel('Дата')
	plt.ylabel('Цена, ₽')

	plt.plot(np.array(x)[peaks], rolling_mean.iloc[peaks], 'ro', label='Пики экономического цикла')
	plt.plot(np.array(x)[extrema_min], rolling_mean.iloc[extrema_min], 'go', label='Спады экономического цикла')
	plt.plot(period_line, rolling_mean.iloc[extrema_array], 'red', label='Экономический период')
	# Локатор по конкретным датам
	# plt.gca().xaxis.set_major_locator(x.DayLocator(bymonthday=[d.day for d in period_line]))
	# plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
	
	# plt.plot(np.array(x)[extrema_max], rolling_mean.iloc[extrema_max], 'ro')
	# plt.plot(np.array(x)[valleys], rolling_mean.iloc[valleys], 'go')
	plt.legend()
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
	plt.plot(rolling_mean, label='Цены на акции')
	plt.legend()
	plt.subplot(412)
	plt.plot(trend, label='Тренд')
	plt.legend()
	plt.subplot(413)
	plt.plot(seasonal, label='Сезонные колебания')
	plt.legend()
	plt.subplot(414)
	plt.plot(residual, label='Остатки')
	plt.legend()
	plt.tight_layout()
	plt.show()
	

def economicle_cycle_by_timestamp(timestamp_el : datetime.datetime):
	x, y = historical_shares_prices_func("BBG333333333", datetime.datetime(1999, 11, 4, tzinfo=datetime.timezone.utc), now(), CandleInterval.CANDLE_INTERVAL_MONTH) 

	time_series = pd.Series(y)

	# Вычисление скользящей средней
	rolling_mean = time_series.rolling(window=20).mean()

	peaks, peaks_details = find_peaks(rolling_mean, height=0)
	extrema_max, extrema_min = find_local_extrema(rolling_mean)

	import dateutil.relativedelta

	cycle_period = dateutil.relativedelta.relativedelta(months=6)
	bottom_period_begin = [min - cycle_period for min in np.array(x)[extrema_min]]
	bottom_period_end = [min + cycle_period  for min in np.array(x)[extrema_min]]
	top_period_begin = [min - cycle_period  for min in np.array(x)[peaks]]
	top_period_end = [min + cycle_period  for min in np.array(x)[peaks]]

	periods = []
	i = 0

	for period in bottom_period_begin:
		periods.append(Period("bottom_period_begin", period, "Дно", extrema_min[i]))
		i =+ 1
	i = 0
	for period in bottom_period_end:
		periods.append(Period("bottom_period_end", period, "Восстановление", extrema_min[i]))
		i =+ 1
	i = 0
	for period in top_period_begin:
		periods.append(Period("top_period_begin", period, "Пик", peaks[i]))
		i =+ 1
	i = 0
	for period in top_period_end:
		periods.append(Period("top_period_end", period, "Спад", peaks[i]))
		i =+ 1
	
	periods = sorted(periods, key=lambda item: item.value)
	
	for period in periods:
		if (period.value <= timestamp_el):
			return period.period_type_ru
		# print(period.value)

# economicle_cycle_graph()
