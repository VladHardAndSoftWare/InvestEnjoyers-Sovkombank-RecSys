class Invest_instrument:
    invest_instrument_counter = 1
    
    def __init__(self, ticket=None, class_code=None, figi=None, type=None, percent=None):
        self.id = Invest_instrument.invest_instrument_counter
        Invest_instrument.invest_instrument_counter += 1
        self.ticket = ticket
        self.class_code = class_code
        self.figi = figi
        self.type = type
        self.percent = percent
    
    