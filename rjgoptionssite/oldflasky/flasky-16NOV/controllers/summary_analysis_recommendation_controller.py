from flask import render_template,redirect


class SummaryAnalysisRecommendationController:

    def __init__(self, parameterService, tickerRateService, ticketAnalysisService , bullishVsBearishAnalysisService ,linearRegressionSerice, priceChangeAnalysisService, template):
        self.time_frame = 1500
        self.parameterService = parameterService
        self.tickerRateService = tickerRateService
        self.ticketAnalysisService = ticketAnalysisService
        self.bullishVsBearishAnalysisService = bullishVsBearishAnalysisService
        self.linearRegressionSerice = linearRegressionSerice
        self.priceChangeAnalysisService = priceChangeAnalysisService
        self.template = template

    def dispatch(self,request):
        model = {}
        ticker = None

        if "tickers" in request.form:
            ticker = request.form.get("tickers")
        elif "ticker" in request.args:
            ticker = request.args["ticker"]

        if ticker is not None:
            foo , from_date, till_date = self.parameterService.init_params(self.time_frame)
            bullish_vs_bearish_totals = None
            slope_and_rsquare_totals = None
            price_changes = None

            ticker_data = self.tickerRateService.get_rate(ticker, from_date, till_date)
            if ticker_data is not None:

                ticker_data = self.ticketAnalysisService.analyze_dataframe(ticker_data)
                price_changes = self.priceChangeAnalysisService.calculate_price_change(ticker_data)
                bullish_vs_bearish_totals = self.bullishVsBearishAnalysisService.analyze_dataframe(ticker_data)
                slope_and_rsquare_totals = self.linearRegressionSerice.calculate_slope_and_rsquare(ticker_data,styling=False)

                model["last_close"] = ticker_data.iloc[0]['Close']
                model["past3month_timeframe_start"],model["past3month_timeframe_finish"]  = self.bullishVsBearishAnalysisService.get_used_range(ticker_data,"past3month")
                model["past9month_timeframe_start"], model["past9month_timeframe_finish"] = self.bullishVsBearishAnalysisService.get_used_range(ticker_data,"past9month")
                model["past1year_timeframe_start"], model["past1year_timeframe_finish"] = self.bullishVsBearishAnalysisService.get_used_range(ticker_data,"past1year")
                model["past9month_start_closeprice"],model["past9month_finish_closeprice"] = self.bullishVsBearishAnalysisService.get_edge_values(ticker_data,"past9month","Close")
                model["past1year_start_closeprice"], model["past1year_finish_closeprice"] = self.bullishVsBearishAnalysisService.get_edge_values(ticker_data,"past1year","Close")

            return render_template(self.template, ticker=ticker,
                                   bullish_vs_bearish_totals=bullish_vs_bearish_totals,
                                   slope_and_rsquare_totals=slope_and_rsquare_totals,
                                   price_changes=price_changes,
                                   model=model)
        else:
            return render_template(self.template,ticker=None)