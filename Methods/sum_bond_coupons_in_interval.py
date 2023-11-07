from dotenv import load_dotenv
import os

from datetime import timedelta

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now

load_dotenv()
TOKEN = os.environ['TINKOFF_API_KEY']

def sum_bond_coupons_in_interval_func(figi_number, from_timestamp, to_timestamp):

    # dividends = []

    with Client(TOKEN) as client:
        bond_coupons = client.instruments.get_bond_coupons(
            figi = figi_number,
            from_ = from_timestamp,
            to = to_timestamp
        )
    
    sum_div = 0
    
    for coupon in bond_coupons.events:
        sum_div += coupon.pay_one_bond.units + coupon.pay_one_bond.nano/1000000000

    return sum_div

def historical_bond_coupons_in_interval_func(figi_number, from_timestamp, to_timestamp):

    #dividends = []

    with Client(TOKEN) as client:
        bond_coupons = client.instruments.get_bond_coupons(
            figi = figi_number,
            from_ = from_timestamp,
            to = to_timestamp
        )

    timestamp = [i.coupon_date for i in bond_coupons.events]
    dividend_price = [coupon.pay_one_bond.units + coupon.pay_one_bond.nano/1000000000 for coupon in bond_coupons.events]
    
    return timestamp, dividend_price