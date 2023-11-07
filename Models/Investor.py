from Models.Portfolio import Portfolio
from Models.Invest_instrument import Invest_instrument

class Investor:
    investor_counter = 1
    
    all_investors = []
    
    def __init__(self, name, age, profession, financial_knowledge, risk_tolerance, initial_capital, monthly_investment, planning_horizon, goal):
        
        self.investor_id = Investor.investor_counter
        Investor.investor_counter += 1
        self.name = name
        self.age = age
        self.profession = profession
        self.financial_knowledge = financial_knowledge
        self.risk_tolerance = risk_tolerance
        self.initial_capital = initial_capital
        self.monthly_investment = monthly_investment
        self.planning_horizon = planning_horizon
        self.goal = goal
        self.portfolio = None
        
        Investor.all_investors.append(self)
        
    def create_portfolio(self, total_investment):
        self.portfolio = Portfolio(total_investment)
        
    def add_portfolio_invest_instruments(self, invest_instrument):
        if self.portfolio:
            self.portfolio.add_invest_instruments(invest_instrument)
        else:
            raise ValueError("Создайте портфель, что бы добавить в него финансовые инструменты!")


