from flask import render_template

class PredictionController:

    def __init__(self, parameterService, tickerRateService, ticketAnalysisService, priceChangeSimulationService, template):
        self.parameterService = parameterService
        self.tickerRateService = tickerRateService
        self.ticketAnalysisService = ticketAnalysisService
        self.priceChangeSimulationService = priceChangeSimulationService
        self.template = template
        self.timeframe = 365
        self.weeks_to_simul = 51


    def dispatch(self, request):
        tickers, from_date, till_date = self.parameterService.init_params(self.timeframe)
        weeks_to_simul = self.weeks_to_simul
        test_img1 = None
        test_img2 = None
        final_prices = []
        if request.method == 'POST':
            tickers = self.parameterService.process_params(request)[0]
            tickers = tickers[0]
            weeks_to_simul = int(self.parameterService.get_param(request,"weeks"))

            if not (tickers is None or from_date is None or till_date is None):

                ticker_data = self.tickerRateService.get_rate(tickers, from_date, till_date)
                if ticker_data is not None:
                    ticker_data = self.ticketAnalysisService.analyze_dataframe(ticker_data)
                    test_img1,test_img2,final_prices = self.priceChangeSimulationService.simmulate_price_change(ticker_data,weeks=weeks_to_simul)

        return render_template(self.template, tickers=tickers, from_date=from_date, till_date=till_date,test_img1=test_img1,test_img2=test_img2,final_prices=final_prices,selected_week=weeks_to_simul)