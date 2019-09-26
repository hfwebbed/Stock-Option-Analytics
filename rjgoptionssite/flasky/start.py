from flask import Flask
from flask import request

from context_builder import application_context_builder

app = Flask(__name__)

rawDataController , summaryAnalysisController , summaryAnalysisRecommendationController, predictionController , \
downloadController, optionsController, profitController , industryController, stockGameController = application_context_builder()

"""""
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
"""



@app.route("/", methods=['GET', 'POST'])
@app.route("/summary_analysis", methods=['GET', 'POST'])
def four_year_analysis():
    return summaryAnalysisController.dispatch(request)

@app.route("/recommendation", methods=['GET','POST'])
def summaryAnalysisRecommendation():
    return summaryAnalysisRecommendationController.dispatch(request)


@app.route("/prediction", methods=['GET', 'POST'])
def future_year_analysis():
    return predictionController.dispatch(request)


@app.route("/download", methods=['GET', 'POST'])
def download_excel():
    return downloadController.dispatch(request)


@app.route("/options", methods=['GET', 'POST'])
def options_summary():
    return optionsController.dispatch(request)

@app.route("/profit", methods=['GET'])
def profit():
    return profitController.dispatch(request)


@app.route('/options/marketPrice')
def impliedVolatilityAjaxCall():
    return optionsController.serveImpliedVolatility(request)

@app.route('/industry')
def industry():
    return industryController.dispatch(request)

@app.route('/industry/add', methods=['POST'])
def industry_add():
    return industryController.add(request)

@app.route('/industry/template', methods=['GET'])
def industry_template():
    return industryController.get_template(request)

@app.route('/industry/delete', methods=['POST'])
def industry_delete():
    return industryController.delete(request)

@app.route('/industry/update', methods=['POST'])
def industry_update():
    return industryController.update_all(request)

@app.route('/industry/subscribe')
def industry_subscribe():
    return industryController.subscribe(request)

@app.route('/industry/unsubscribe')
def industry_unsubscribe():
    return industryController.unsubscribe(request)

@app.route("/raw_data", methods=['GET', 'POST'])
def raw_requests():
    return rawDataController.dispatch(request)

@app.route("/stock_game", methods=['GET', 'POST'])
def stock_game():
    return stockGameController.dispatch(request)

@app.route('/stock_game/add', methods=['POST'])
def stock_game_add():
    return stockGameController.add(request)

@app.route('/stock_game/delete', methods=['GET'])
def stock_game_delete():
    return stockGameController.delete(request)


if __name__ == "__main__":
    app.run(debug=True, port=4999)


