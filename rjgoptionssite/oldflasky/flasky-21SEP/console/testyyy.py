from pandas_datareader import data as pdr


# download dataframe
data = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")

print(data)