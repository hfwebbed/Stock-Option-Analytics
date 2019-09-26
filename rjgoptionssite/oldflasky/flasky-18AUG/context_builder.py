import matplotlib
matplotlib.use('Agg')

from services.ticker_analysis_service import TickerAnalysisService
from services.params_service import ParameterService
from services.ticker_info_service import TickerInfoService
from services.stock_rate_service import TickerRateService
from services.bullish_vs_bearish_analysis_service import BullishVsBearishAnalysisService
from services.linear_regression_service import LinearRegressionSerice
from services.volatility_analysis_service import VolatilityAnalysisService
from services.price_change_analysis_service import PriceChangeAnalysisService
from services.plotting_util_service import PlottingUtilServce
from services.price_change_simulation_service import PriceChangeSimulationService

from controllers.raw_data_controller import RawDataController
from controllers.summary_analysis_controller import  SummaryAnalysisController
from controllers.prediction_controller import PredictionController


def application_context_builder():
    tickerRateService = TickerRateService('google')
    tickerNameService = TickerInfoService('resources/secwiki_tickers.csv')
    parameterService = ParameterService(10)
    tickerAnalysisService = TickerAnalysisService()
    bullishVsBearishAnalysisService = BullishVsBearishAnalysisService()
    linearRegressionSerice = LinearRegressionSerice()
    volatilityAnalysisService = VolatilityAnalysisService()
    plottingUtilService = PlottingUtilServce()

    priceChangeAnalysisService = PriceChangeAnalysisService(volatilityAnalysisService)
    priceChangeSimulationService = PriceChangeSimulationService(volatilityAnalysisService,plottingUtilService)

    rawDataController = RawDataController(parameterService,tickerRateService,tickerAnalysisService, tickerNameService, "raw_data.html")
    summaryAnalysisController = SummaryAnalysisController(parameterService,tickerRateService,tickerAnalysisService,
                                                            bullishVsBearishAnalysisService, linearRegressionSerice,
                                                            priceChangeAnalysisService, "summary_analysis.html")

    predictionController = PredictionController(parameterService,tickerRateService,tickerAnalysisService,priceChangeSimulationService, "prediction.html")

    return rawDataController , summaryAnalysisController , predictionController