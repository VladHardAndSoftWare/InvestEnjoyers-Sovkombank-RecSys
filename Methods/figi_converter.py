from dotenv import load_dotenv
import os

from datetime import timedelta

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now

load_dotenv()
TOKEN = os.environ['TINKOFF_API_KEY']


def figi_converter_share_func(class_code_value, id_value):
    
    with Client(TOKEN) as client:
        share = client.instruments.share_by(
            id_type=2,
            class_code=class_code_value,
            id=id_value
        )
            
    return share.instrument.figi

def figi_converter_bond_func(class_code_value, id_value):
    
    with Client(TOKEN) as client:
        bond = client.instruments.bond_by(
            id_type=2,
            class_code=class_code_value,
            id=id_value
        )
            
    return bond.instrument.figi

def figi_converter_currency_func(class_code_value, id_value):
    
    with Client(TOKEN) as client:
        currency = client.instruments.currency_by(
            id_type=2,
            class_code=class_code_value,
            id=id_value
        )
            
    return currency.instrument.figi
    
    # sum_div = 0
    
    # for dividend in dividends.dividends:
    #     sum_div += dividend.dividend_net.units + dividend.dividend_net.nano/1000000000

    # return sum_div