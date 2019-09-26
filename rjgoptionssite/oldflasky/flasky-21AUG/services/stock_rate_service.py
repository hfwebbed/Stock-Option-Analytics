import pandas_datareader.data as web


class TickerRateService():

    def __init__(self,provider):
        self.provider = provider
        pass

    def get_rate(self,stock,start,end):
        try:
            data = web.DataReader(stock,self.provider, start, end)
            return data.reindex(index=data.index[::-1])
        except Exception:
            return None

    def get_rates(self,stocks,start,end):
        data = {}
        for stock in stocks:
            data[stock] = self.get_rate(stock,start,end)
        return data