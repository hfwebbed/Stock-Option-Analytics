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