from pandas import DataFrame as pd
from pandas.formats.style import Styler
import math
import numpy as np

class StockGameService:

    def __init__(self,parameterService,tickerRateService,ticketAnalysisService,priceChangeSimulationService,linearRegressionSerice,rsquareHighlighter):
        self.parameterService = parameterService
        self.tickerRateService = tickerRateService
        self.ticketAnalysisService = ticketAnalysisService
        self.priceChangeSimulationService = priceChangeSimulationService
        self.linearRegressionSerice = linearRegressionSerice
        self.rsquareHighlighter = rsquareHighlighter
        self.timeframe = 365
        self.weeks_to_simul = 51
        self.cache = {}
        pass

    def get_for_tickers(self, tickers):
        _, from_date, till_date = self.parameterService.init_params(self.timeframe)

        table = []
        for ticker_record in tickers:
            ticker_name = ticker_record['name']
            ticker_id = ticker_record['id']
            if ticker_name in self.cache:
                ticker_data = self.cache[ticker_name]
            else:
                ticker_data = self.tickerRateService.get_rate(ticker_name, from_date, till_date)
                #self.cache[ticker] = ticker_data #enable cache for debug

            if ticker_data is not None:
                ticker_data = self.ticketAnalysisService.analyze_dataframe(ticker_data)
                simmul_data = self.priceChangeSimulationService.get_simmulation_data(ticker_data, weeks=self.weeks_to_simul)

                lr_data = self.linearRegressionSerice.calculate_slope_and_rsquare_kernel(simmul_data["weeks"],simmul_data["prices"])

                slope_index = None
                if lr_data["slope"] > 0:
                    slope_index = 1
                if lr_data["slope"] < 0:
                    slope_index = -1

                last_index = 0
                if simmul_data['last'] > simmul_data['start']:
                    last_index = (simmul_data['last'] - simmul_data['start']) / simmul_data['start']
                elif simmul_data['last'] < simmul_data['start']:
                    last_index = (simmul_data['start'] - simmul_data['last']) / simmul_data['start']

                record = {
                    "id":ticker_id,
                    "ticker":ticker_name,
                    "start":simmul_data['start'],
                    "low": simmul_data['low'],
                    "median": simmul_data['median'],
                    "high": simmul_data['high'],
                    "last": simmul_data['last'],
                    "slope":lr_data["slope"],
                    "slope_index":slope_index,
                    "last_index":last_index,
                    "r_squared": lr_data["r_squared"],
                    "rs_measure":self.linearRegressionSerice.rsquare_group(lr_data["r_squared"]),
                    "delete_link":"<a href='/stock_game/delete?id={}'>delete</a>".format(ticker_id)
                }
                table.append(record)

        if len(tickers) > 0:
            df = pd.from_records(table)
            df = df.sort_values(by=['rs_measure', 'slope_index','last_index'], ascending=[0, 0, 0])
            df = df.reset_index(drop=True)
            df = df.reset_index()
            df = df.reindex_axis(["index","ticker", "start", "high","last", "slope", "r_squared",  "delete_link"],axis=1)
            df["index"] += 1
            df.columns = ["rank", "ticker", "start", "high", "last", "slope", "r_squared", "delete_link"]

        else:
            df = pd(data = [], columns=["rank","ticker", "start", "high","last", "slope", "r_squared",  "delete_link"])



        return df

    def apply_styling(self,df):
        styler = Styler(df)
        styler = styler.apply(self.rsquareHighlighter.highlight_rsquare,subset=["r_squared"])
        return styler