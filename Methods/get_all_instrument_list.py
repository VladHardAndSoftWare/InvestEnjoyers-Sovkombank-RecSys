from ast import literal_eval
from dotenv import load_dotenv
import os

from datetime import timedelta

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now

load_dotenv()
TOKEN = os.environ['TINKOFF_API_KEY']

def all_rub_shares():
    
    figi = []
    ticker = []
    isin = []
    name = []
    sector = []
    
    with Client(TOKEN) as client:
        shares = client.instruments.(
            instrument_status=1
        )
    for i in shares.instruments:
        if(i.currency=='rub'):
            figi.append(i.figi)
            ticker.append(i.ticker)
            name.append(i.name)
            isin.append(i.isin)
            sector.append(i.sector)
    
    return figi, ticker, name, isin, sector

#l=all_rub_shares()[0]
#print(l)