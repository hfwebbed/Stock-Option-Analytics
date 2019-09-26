from flask import Flask
from flask import request

from context_builder import application_context_builder

app = Flask(__name__)
rawRequestController , fourYearAnalysisController = application_context_builder()

@app.route("/", methods=['GET', 'POST'])
@app.route("/iteration1and2", methods=['GET', 'POST'])
def raw_requests():
    return rawRequestController.dispatch(request)


@app.route("/iteration3andProbably4", methods=['GET', 'POST'])
def four_year_analysis():
    return fourYearAnalysisController.dispatch(request)


if __name__ == "__main__":
    app.run(debug=True, port=80)


