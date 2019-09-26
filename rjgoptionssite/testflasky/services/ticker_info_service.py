
class TickerInfoService():
    def __init__(self,source_file):
        self.UNKNOWN_TICKER = {"name": "unknown"}
        self.data = {}
        file = open(source_file)
        for line in file:
            info = line.split(",")
            self.data[info[0].upper()] = {"name":info[1] }

    def get_ticker_data(self,ticker):
        if ticker.upper() in self.data:
            return self.data[ticker.upper()]
        else:
            return self.UNKNOWN_TICKER

    def get_tickers_data(self,tickers):
        data = {}
        for ticker in tickers:
            data[ticker] = self.get_ticker_data(ticker)
        return data