class Portfolio:
    portfolio_counter = 1
    
    def __init__(self, total_investment=None):
        self.portfolio_id = Portfolio.portfolio_counter
        Portfolio.portfolio_counter += 1
        self.total_investment = total_investment
        self.invest_instruments = []
        
    def add_invest_instruments(self, invest_instrument):
        self.invest_instruments.append(invest_instrument)