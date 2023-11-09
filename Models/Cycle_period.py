class Period:
    period_counter = 1
    
    def __init__(self, period_type, value, period_type_ru, extrema):
        self.period_id = Period.period_counter
        Period.period_counter += 1
        self.period_type = period_type
        self.value = value  
        self.period_type_ru = period_type_ru
        self.extrema = extrema