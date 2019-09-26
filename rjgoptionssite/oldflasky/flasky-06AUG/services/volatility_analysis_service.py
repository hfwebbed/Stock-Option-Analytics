import math

class VolatilityAnalysisService:

    def __init__(self):
        self.TRADE_DAYS_IN_YEAR = 250
        self.SQUARE_ROOT_TRADE_DAYS_IN_YEAR = math.sqrt(254)
        self.SQUARE_ROOT_OF_TRADE_DAYS_IN_MONTH = math.sqrt(254 / 12)

    def calculate_volatility(self,df):
        df = df[1:]
        df = df[:self.TRADE_DAYS_IN_YEAR]['adjclosediff']
        std_dev = df.std()
        year_volatility = std_dev * self.SQUARE_ROOT_TRADE_DAYS_IN_YEAR
        day_volatility = year_volatility / self.SQUARE_ROOT_TRADE_DAYS_IN_YEAR
        month_volatility = year_volatility / self.SQUARE_ROOT_OF_TRADE_DAYS_IN_MONTH
        return {"year":year_volatility,"month":month_volatility,"day":day_volatility}

