
class PriceChangeAnalysisService:

    def __init__(self,volatilityAnalysisService):
        self.volatilityAnalysisService = volatilityAnalysisService

    def calculate_price_change(self,df):

        last_close = df.iloc[0]['Close']
        volatilities = self.volatilityAnalysisService.calculate_volatility(df)

        expected_monthly_shift = last_close * volatilities['month'] / 100
        expected_yearly_shift  = last_close * volatilities['year']  / 100

        expected_monthly_grow = last_close + expected_monthly_shift
        expected_monthly_drop = last_close - expected_monthly_shift
        expected_yearly_grow = last_close + expected_yearly_shift
        expected_yearly_drop = last_close - expected_yearly_shift

        return {
            "last_close":last_close,
            "expected_monthly_grow":round(expected_monthly_grow,2),
            "expected_monthly_drop":round(expected_monthly_drop,2),
            "expected_yearly_grow":round(expected_yearly_grow,2),
            "expected_yearly_drop":round(expected_yearly_drop,2)
        }


