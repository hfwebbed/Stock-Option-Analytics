from flask import render_template

class StockGameController:

    def __init__(self, stockGameService , stockGameDbService, visitorDbService, template):
        self.stockGameService = stockGameService
        self.stockGameDbService = stockGameDbService
        self.visitorDbService = visitorDbService
        self.template = template

    def add(self,request):
        name = request.form.get('new_ticker').upper()
        if name is not None and name != '':
            visitor = self.get_visitor(request)
            if visitor is None:
                visitor = self.create_visitor(request)

            names = self.stockGameDbService.getNamesByVisitor(visitor)
            if name not in names:
                self.stockGameDbService.create(name,visitor)
        return self.dispatch(request)

    def delete(self,request):
        id = request.args.get('id')
        visitor = self.get_visitor(request)
        record = self.stockGameDbService.getById(id)
        if record is not None:
            if visitor is not None:
                if record['user_id'] == visitor['id']:
                    self.stockGameDbService.delete(id)
        return self.dispatch(request)

    def dispatch(self, request):
        visitor_id = self.get_visitor(request)
        visitor_tickers = self.stockGameDbService.getByVisitor(visitor_id)

        ticker_data = self.stockGameService.get_for_tickers(visitor_tickers)
        return render_template(self.template,ticker_data=ticker_data)

    def create_visitor(self,request):
        ip = request.remote_addr
        visitor = self.visitorDbService.create(ip)
        return visitor

    def get_visitor(self,request):
        ip = request.remote_addr
        return self.visitorDbService.getByIp(ip)

    def get_visitor_tickers(self,visitor):
        print(self.dummy_db)
        return self.dummy_db