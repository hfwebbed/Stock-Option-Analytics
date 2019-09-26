from flask import Flask
from flask import request

from context_builder import application_context_builder

app = Flask(__name__)

rawDataController , summaryAnalysisController , predictionController , downloadController = application_context_builder()

@app.route("/", methods=['GET', 'POST'])
@app.route("/raw_data", methods=['GET', 'POST'])
def raw_requests():
    return rawDataController.dispatch(request)


@app.route("/summary_analysis", methods=['GET', 'POST'])
def four_year_analysis():
    return summaryAnalysisController.dispatch(request)


@app.route("/prediction", methods=['GET', 'POST'])
def future_year_analysis():
    return predictionController.dispatch(request)

@app.route("/download", methods=['GET', 'POST'])
def download_excel():
    return downloadController.dispatch(request)

if __name__ == "__main__":
    app.run(debug=True, port=4999)


