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
        weeks = request.form.get("weeks")
        if weeks is not None:
            weeks = int(weeks)
        else:
            weeks = self.stockGameService.weeks_to_simul

        visitor = self.get_visitor(request)
        visitor_tickers = self.stockGameDbService.getByVisitor(visitor)

        img_for = request.form.get("show_img")
        for ticker in visitor_tickers:
            if ticker['name'] == img_for:
                break
        else:
            img_for = None

        ticker_data,images = self.stockGameService.get_for_tickers(visitor_tickers,weeks_to_simul=weeks,img_for=img_for)
        return render_template(self.template,ticker_data=ticker_data,images=images,selected_week=weeks,img_for=img_for)

    def create_visitor(self,request):
        ip = request.remote_addr
        visitor = self.visitorDbService.create(ip)
        return visitor

    def get_visitor(self,request):
        ip = request.remote_addr
        return self.visitorDbService.getByIp(ip)
