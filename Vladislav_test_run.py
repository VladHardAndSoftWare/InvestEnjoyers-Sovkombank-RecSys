import datetime
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval
import matplotlib.pyplot as plt

from Methods.historical_shares_prices import historical_shares_prices_func
from Methods.date_shares_prices import date_shares_prices_func
from Methods.sum_dividends_in_interval import sum_dividends_in_interval_func
from Methods.sum_bond_coupons_in_interval import sum_bond_coupons_in_interval_func, historical_bond_coupons_in_interval_func
from Methods.figi_converter import figi_converter_share_func
from Methods.figi_converter import figi_converter_bond_func
from Methods.figi_converter import figi_converter_currency_func

from Methods.get_securities_lists import all_rub_shares

from Models.Investor import Investor
from Models.Portfolio import Portfolio
from Models.Invest_instrument import Invest_instrument


# =====figi конвертер для акций=====
# На вход идентификатор class_code и тикер акции
# На выход figi номер акции
figi_share_number = figi_converter_share_func("TQBR","MOEX")
figi_bond_number = figi_converter_bond_func("TQOB","SU46012RMFS9")
figi_bond_number2 = figi_converter_bond_func("TQOB","SU26241RMFS8")
figi_currency_number = figi_converter_currency_func("CETS","GLDRUB_TOM")
print("============figi==============")
print(figi_share_number)
print(figi_bond_number)
print(figi_currency_number)
print("==========================")

# =====Историческая цена акций======
# На вход figi номер акции, начальный тайм стемп, конечный таймстеп, интервал c какой переодичностью беруться данные
# На выход масив таймстемпов, массив цены акции
x, y = historical_shares_prices_func("BBG004730N88", datetime.datetime(2012, 11, 4, tzinfo=datetime.timezone.utc), now(), CandleInterval.CANDLE_INTERVAL_MONTH)

# plt.plot(x, y)
# plt.show()

# =====Стоимость ценной бумаги в момент времени t=====
# На вход figi номер акции, тайм стемпна момент которого мы хотим узнать цену
# На выход цена акции на момент времени timestamp
C = date_shares_prices_func("BBG004730N88", datetime.datetime(2022, 11, 4, tzinfo=datetime.timezone.utc))

print(C)

# =====Cумма дивидендов в интервали времени=====
sum_div = sum_dividends_in_interval_func("BBG004730N88", datetime.datetime(2012, 11, 4, tzinfo=datetime.timezone.utc), now())

print(f"sum_div: {sum_div}")

# =====Cумма купонов в интервали времени=====
sum_bond = sum_bond_coupons_in_interval_func(figi_bond_number, datetime.datetime(2012, 11, 4, tzinfo=datetime.timezone.utc), now())

print(f"sum_bonds: {sum_bond}")

#=====Исторические выплаты по купонам=====
# https://www.moex.com/ru/bondization/calendar
x, y = historical_bond_coupons_in_interval_func(figi_bond_number, datetime.datetime(2012, 11, 4, tzinfo=datetime.timezone.utc), now())

# plt.plot(x, y)
# plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~Классы~~~~~~~~~~~~~~~~~~~~~~~~~~~
investor_Petr = Investor("Петрович", 55, "Сантехник", 9, 0.9, 10000000, 1000000, 60, "Хуй знает")
investor_Petr.create_portfolio(200000)
investor_Petr.add_portfolio_invest_instruments(Invest_instrument("MOEX", "TQBR", figi_converter_share_func("TQBR","MOEX"), "share", 1))

investor_Elena = Investor(
    name= "Елена",
    age=30,
    profession="CEO",
    financial_knowledge=3,
    risk_tolerance=0.2,
    initial_capital=100,
    monthly_investment=10,
    planning_horizon=0,
    goal="грудь"
)
Investor.all_investors[1].create_portfolio(200)
MOEX_Elena = Invest_instrument("MOEX", "TQBR", figi_converter_share_func("TQBR","MOEX"), "share", 100)
Investor.all_investors[1].add_portfolio_invest_instruments(MOEX_Elena)

for investor in Investor.all_investors:
    print(investor.name)
    
    
print(all_rub_shares())

