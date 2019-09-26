from flask import Flask
from flask import request

from context_builder import application_context_builder



app = Flask(__name__)

rawDataController , summaryAnalysisController , predictionController , downloadController,optionsController = application_context_builder()

"""
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
"""


@app.route("/raw_data", methods=['GET', 'POST'])
def raw_requests():
    return rawDataController.dispatch(request)

@app.route("/", methods=['GET', 'POST'])
@app.route("/summary_analysis", methods=['GET', 'POST'])
def four_year_analysis():
    return summaryAnalysisController.dispatch(request)


@app.route("/prediction", methods=['GET', 'POST'])
def future_year_analysis():
    return predictionController.dispatch(request)


@app.route("/download", methods=['GET', 'POST'])
def download_excel():
    return downloadController.dispatch(request)


@app.route("/options", methods=['GET', 'POST'])
def options_summary():
    return optionsController.dispatch(request)


@app.route('/options/marketPrice')
def impliedVolatilityAjaxCall():
    return optionsController.serveImpliedVolatility(request)


if __name__ == "__main__":
    app.run(debug=True, port=4999)


