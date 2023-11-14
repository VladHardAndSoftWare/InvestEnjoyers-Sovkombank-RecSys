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

#l=all_rub_shares()
#print(l)

def all_gov_bonds():
    
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
        if(i.currency=='rub' and i.name.__contains__('ОФЗ')):
            figi.append(i.figi)
            ticker.append(i.ticker)
            name.append(i.name)
            isin.append(i.isin)
            maturity_date.append(i.maturity_date)
            state_reg_date.append(i.state_reg_date)
            duration.append(int((i.maturity_date-i.state_reg_date).days/365))
            #sector.append(i.sector)
    
    return figi, ticker, name, isin, state_reg_date, maturity_date, duration

#x=all_gov_bonds()
#print(x)

def all_rub_metals():
    
    figi = []
    ticker = []
    isin = []
    name = []
    
    with Client(TOKEN) as client:
        currency = client.instruments.currencies(
            instrument_status=1
        )
    for i in currency.instruments:
        if(i.name=='Золото' or i.name=='Серебро'): #Единственные торгующиеся драг. металлы(По крайней мере по запросу к API)
            figi.append(i.figi)
            ticker.append(i.ticker)
            name.append(i.name)
    
    return figi, ticker, name

#print(all_rub_metals())
def all_short_bonds():
    
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
        if(i.currency=='rub'):
            dur=int((i.maturity_date-i.state_reg_date).days/365)
            if(dur<=2 and dur>=0):
                figi.append(i.figi)
                ticker.append(i.ticker)
                name.append(i.name)
                isin.append(i.isin)
                maturity_date.append(i.maturity_date)
                state_reg_date.append(i.state_reg_date)
                duration.append(dur)
            #sector.append(i.sector)
    
    return figi, ticker, name, isin, state_reg_date, maturity_date, duration

#x=all_short_bonds()
#print(x)