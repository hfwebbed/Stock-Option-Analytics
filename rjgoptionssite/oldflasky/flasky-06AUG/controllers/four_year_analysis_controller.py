from flask import render_template


class FourYearAnalysisController:

    def __init__(self, parameterService, tickerRateService, ticketAnalysisService , tickerFourYearAnalysisService ,linearRegressionSerice, priceChangeAnalysisService, template):
        self.time_frame = 1500
        self.parameterService = parameterService
        self.tickerRateService = tickerRateService
        self.ticketAnalysisService = ticketAnalysisService
        self.tickerFourYearAnalysisService = tickerFourYearAnalysisService
        self.linearRegressionSerice = linearRegressionSerice
        self.priceChangeAnalysisService = priceChangeAnalysisService
        self.template = template

    def dispatch(self, request):
        tickers, from_date, till_date = self.parameterService.init_params(self.time_frame)
        bullish_vs_bearish_totals = None
        slope_and_rsquare_totals = None
        price_changes = None

        if request.method == 'POST':
            tickers, from_date, till_date = self.parameterService.process_params(request)
            tickers = tickers[0]
            if not (tickers is None or from_date is None or till_date is None):
                ticker_data = self.tickerRateService.get_rate(tickers, from_date, till_date)
                if ticker_data is not None:
                    ticker_data = self.ticketAnalysisService.analyze_dataframe(ticker_data)
                    price_changes = self.priceChangeAnalysisService.calculate_price_change(ticker_data)

                    bullish_vs_bearish_totals = self.tickerFourYearAnalysisService.analyze_dataframe(ticker_data)
                    slope_and_rsquare_totals = self.linearRegressionSerice.calculate_slope_and_rsquare(ticker_data)

        return render_template('iteration3andProbably4.html', tickers = tickers, from_date=from_date, till_date= till_date,
                               bullish_vs_bearish_totals=bullish_vs_bearish_totals,
                               slope_and_rsquare_totals=slope_and_rsquare_totals,
                               price_changes=price_changes)
