import pandas as pd
pd.set_option('display.max_rows', 500)

from services.stock_rate_service import TickerRateService
from datetime import date, timedelta

pd.set_option('max_columns', 500)


since,till = date.today() - timedelta(days=10), date.today()

yahoo = TickerRateService("yahoo")
google = TickerRateService("google")


y = yahoo.get_rate("SPY", since,till)
y = y.drop('Adj Close', 1)


g = google.get_rate("SPY", since,till)
g = g.head(10)

print(y)

print(g)