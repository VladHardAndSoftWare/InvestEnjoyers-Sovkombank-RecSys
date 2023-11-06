from dotenv import load_dotenv
import os

from datetime import timedelta

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now


def historical_shares_prices_func(figi_number, from_timestamp, to_timestamp, interval):
    
    load_dotenv()
    TOKEN = os.environ['TINKOFF_API_KEY']

    candles = []

    with Client(TOKEN) as client:
        for candle in client.get_all_candles(
            figi = figi_number,
            from_ = from_timestamp,
            to = to_timestamp,
            interval = interval, #CandleInterval.CANDLE_INTERVAL_HOUR
        ):
            candles.append(candle)

    timestamp = [candle.time for candle in candles]
    share_price = [candle.open.units + candle.open.nano/1000000000 for candle in candles]

    return timestamp, share_price