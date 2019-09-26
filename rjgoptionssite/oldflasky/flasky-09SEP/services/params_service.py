from datetime import date, timedelta

class ParameterService:

    def __init__(self,default_date_gap=10):
        self.default_date_gap = default_date_gap
        self.default_ticker = ""

    def init_params(self,date_gap=None):
        if date_gap is None:
                date_gap = self.default_date_gap
        return self.default_ticker , date.today() - timedelta(days=date_gap), date.today()

    def process_params(self,request):
        from_date = request.form.get('from_date')
        till_date = request.form.get('till_date')
        tickers = request.form.get('tickers')
        if tickers is not None:
            for separator in ":,+":
                if tickers.find(separator) >= 0:
                    tickers = tickers.split(separator)
                    break
            else:
                tickers = [tickers]

        return tickers, from_date, till_date

    def get_param(self,request,param):
        return request.form.get(param)

    def init_option_controller_params(self):
        underlyingPrice = 14.00
        days = 21
        volatility = 76.5
        interest = 1.5
        dividend = 0.0
        return underlyingPrice,days,volatility,interest,dividend

    def process_options_params(self,request):
        underlyingPrice = float(request.form.get('underlyingPrice'))
        days = int(request.form.get('days'))
        volatility = float(request.form.get('volatility'))
        interest = float(request.form.get('interest'))
        dividend = float(request.form.get('dividend'))
        return underlyingPrice,  days, volatility, interest, dividend

    def process_options_params_ajax(self,request):
        print(request.args)
        optionSide = request.args.get('optionSide')
        underlyingPrice = float(request.args.get('underlyingPrice'))
        exercisePrice = float(request.args.get('exercisePrice'))
        days = int(request.args.get('days'))
        targetPrice = float(request.args.get('targetPrice'))
        interest = float(request.args.get('interest'))
        dividend = float(request.args.get('dividend'))
        return optionSide,underlyingPrice, exercisePrice, days, targetPrice, interest, dividend