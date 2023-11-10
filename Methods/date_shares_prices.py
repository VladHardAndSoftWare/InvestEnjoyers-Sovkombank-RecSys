from dotenv import load_dotenv
import os

from datetime import timedelta

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now


def date_shares_prices_func(figi_number, timestamp):
    
    load_dotenv()
    TOKEN = os.environ['TINKOFF_API_KEY']

    candles = []

    with Client(TOKEN) as client:
        for candle in client.get_all_candles(
            figi = figi_number,
            from_ = timestamp,
            to = timestamp + timedelta(days=1),
            interval = CandleInterval.CANDLE_INTERVAL_DAY
        ):
            candles.append(candle)

    share_price = [candle.close.units + candle.close.nano/1000000000 for candle in candles][0]

    return share_price


