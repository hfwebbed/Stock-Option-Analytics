import pandas_datareader.data as web
from pandas_datareader.data import Options
import datetime
import pandas as pd
pd.set_option('display.width', 300)

#data = web.DataReader(stock,self.provider, start, end)

#data = web.DataReader("AAPL","google", "01/01/2017", "05/05/2017")
#print(data)

expiry = datetime.date(2017, 2, 2)
aapl = Options('aapl','yahoo')
data = aapl.get_call_data(expiry=expiry)

print(data)

