class Invest_instrument:
    invest_instrument_counter = 1
    
    def __init__(self, ticket, class_code, figi, type, percent):
        self.id = Invest_instrument.invest_instrument_counter
        Invest_instrument.invest_instrument_counter += 1
        self.ticket = ticket
        self.class_code = class_code
        self.figi = figi
        self.type = type
        self.percent = percent
    
    