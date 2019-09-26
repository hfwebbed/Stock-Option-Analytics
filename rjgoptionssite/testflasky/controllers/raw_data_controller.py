from flask import render_template


class RawDataController:

    def __init__(self, parameterService, tickerRateService, ticketAnalysisService, tickerNameService, template):
        self.parameterService = parameterService
        self.tickerRateService = tickerRateService
        self.ticketAnalysisService = ticketAnalysisService
        self.tickerNameService = tickerNameService
        self.template = template

    def dispatch(self,request):
        ticker_data = None
        ticker_headers = None

        tickers, from_date, till_date = self.parameterService.init_params()
        if request.method == 'POST':
            tickers, from_date, till_date = self.parameterService.process_params(request)
            if not ( tickers is None or from_date is None or till_date is None):
                ticker_data = self.tickerRateService.get_rates(tickers, from_date, till_date)
                #ticker_data = self.ticketAnalysisService.analyze_dataframes(ticker_data)
                ticker_headers = self.tickerNameService.get_tickers_data(tickers)
                tickers = ",".join(tickers)

        return render_template(self.template, ticker_data=ticker_data, ticker_headers=ticker_headers,from_date=from_date,
                           till_date=till_date, tickers=tickers)