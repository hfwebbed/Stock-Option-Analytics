
from pandas_datareader.yahoo import daily

import pandas as pd
pd.set_option('display.width', 300)


foo = daily.YahooDailyReader('AAPL',start="01/01/2017",end="05/05/2017")
foo.read()
print(foo)






