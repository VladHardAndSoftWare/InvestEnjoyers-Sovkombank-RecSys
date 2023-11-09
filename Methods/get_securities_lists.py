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
        shares = client.instruments.shares(
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

def all_rub_bonds():
    
    figi = []
    ticker = []
    isin = []
    name = []
    maturity_date = []
    state_reg_date = []
    duration = []
    
    with Client(TOKEN) as client:
        bonds = client.instruments.bonds(
            instrument_status=1
        )
    for i in bonds.instruments:
        if(i.currency=='rub' and i.sector=='government'):
            print(i)
            figi.append(i.figi)
            ticker.append(i.ticker)
            name.append(i.name)
            isin.append(i.isin)
            maturity_date.append(i.maturity_date)
            state_reg_date.append(i.state_reg_date)
            duration.append(int((i.maturity_date-i.state_reg_date).days/365))
            #sector.append(i.sector)
    
    return figi, ticker, name, isin, state_reg_date, maturity_date, duration

#x=all_rub_bonds()
#print(x)