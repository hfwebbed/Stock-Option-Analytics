from pandas import DataFrame as pd
import math

class StockGameService:

    def __init__(self,parameterService,tickerRateService,ticketAnalysisService,priceChangeSimulationService,linearRegressionSerice):
        self.parameterService = parameterService
        self.tickerRateService = tickerRateService
        self.ticketAnalysisService = ticketAnalysisService
        self.priceChangeSimulationService = priceChangeSimulationService
        self.linearRegressionSerice = linearRegressionSerice
        self.timeframe = 365
        self.weeks_to_simul = 51

        self.cache = {}

        pass


    def get_for_tickers(self, tickers):
        _ , from_date, till_date = self.parameterService.init_params(self.timeframe)

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

                record = {
                    "id":ticker_id,
                    "ticker":ticker_name,
                    "start":simmul_data['start'],
                    "low": simmul_data['low'],
                    "median": simmul_data['median'],
                    "high": simmul_data['high'],
                    "slope":lr_data["slope"],
                    "abs_slope":math.fabs(lr_data["slope"]),
                    "r_squared": lr_data["r_squared"],
                    "rs_measure":self.linearRegressionSerice.rsquare_group(lr_data["r_squared"]),
                    "delete_link":"<a href='/stock_game/delete?id={}'>delete</a>".format(ticker_id)
                }

                table.append(record)

        df = pd.from_records(table)
        df = df.reindex_axis(["ticker", "start", "median", "high", "slope","abs_slope", "r_squared","rs_measure","delete_link"], axis=1)
        df = df.sort_values(by=['rs_measure', 'abs_slope'], ascending=[0, 0])
        df = df.reset_index(drop=True)

        return df