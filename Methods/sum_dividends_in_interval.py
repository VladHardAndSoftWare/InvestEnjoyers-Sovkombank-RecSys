from dotenv import load_dotenv
import os

from datetime import timedelta

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now


def sum_dividends_in_interval_func(figi_number, from_timestamp, to_timestamp):
    
    load_dotenv()
    TOKEN = os.environ['TINKOFF_API_KEY']

    # dividends = []

    with Client(TOKEN) as client:
        dividends = client.instruments.get_dividends(
            figi = figi_number,
            from_ = from_timestamp,
            to = to_timestamp
        )
    
    sum_div = 0
    
    for dividend in dividends.dividends:
        sum_div += dividend.dividend_net.units + dividend.dividend_net.nano/1000000000

    return sum_div