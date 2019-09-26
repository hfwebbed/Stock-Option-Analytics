import matplotlib
matplotlib.use('Agg')

import pandas as pd
pd.set_option('display.max_colwidth', -1)

from services.rsquare_highlighter import RSquareHighlighter
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
from services.option_suggestion_service import OptionSuggestionService
from services.dataframe_column_inserter_service import DataftrameColumnInserterService
from services.option_implied_volatility_service import OptionImpliedVolatilityService
from services.option_suggestion_column_labeling_service import OptionSuggestionColumnLabelingService

from services.db.connection_factory import ConnectionFactory
from services.db.utils import Utils
from services.db.stock_game_db_service import StockGameDbService
from services.db.industry_crosstable_db_service import IndustryDbService,IndustryRelationsDbService
from services.db.visitor_db_service import VisitorDbService
from services.industry_crosstable_service import IndustryCrosstableService
from services.industry_crosstable_default_template_service import IndustryCrosstableDefaultTemplateService
from services.stock_game_service import StockGameService

from controllers.raw_data_controller import RawDataController
from controllers.summary_analysis_controller import  SummaryAnalysisController
from controllers.summary_analysis_recommendation_controller import SummaryAnalysisRecommendationController
from controllers.prediction_controller import PredictionController
from controllers.download_controller import DownloadController
from controllers.options_controller import OptionsController
from controllers.profit_controller import ProfitController
from controllers.industry_controller import IndustryController
from controllers.stock_game_controller import StockGameController


def application_context_builder():

    #tickerRateService = TickerRateService('google')
    rsquareHighlighter = RSquareHighlighter()
    tickerRateService = TickerRateService('yahoo')
    tickerNameService = TickerInfoService('resources/secwiki_tickers.csv')
    parameterService = ParameterService(10)
    tickerAnalysisService = TickerAnalysisService()
    bullishVsBearishAnalysisService = BullishVsBearishAnalysisService()
    linearRegressionSerice = LinearRegressionSerice(rsquareHighlighter)
    volatilityAnalysisService = VolatilityAnalysisService()
    plottingUtilService = PlottingUtilServce()
    optionSuggestionService = OptionSuggestionService()

    connectionFactory = ConnectionFactory("../db/flasky/flaskysqlite.db")
    db_utils = Utils()

    stockGameDbService = StockGameDbService(connectionFactory,db_utils)
    visitorDbService = VisitorDbService(connectionFactory,db_utils)
    industryDbService = IndustryDbService(connectionFactory,db_utils)
    industryRelationsDbService = IndustryRelationsDbService(connectionFactory,db_utils)
    industryCrosstableDefaultTemplateService = IndustryCrosstableDefaultTemplateService()
    industryCrosstableService = IndustryCrosstableService(industryDbService,industryRelationsDbService)

    dataftameColumnInserterService = DataftrameColumnInserterService()
    optionImpliedVolatilityService = OptionImpliedVolatilityService(optionSuggestionService,dataftameColumnInserterService)
    optionSuggestionColumnLabelingService = OptionSuggestionColumnLabelingService()

    priceChangeAnalysisService = PriceChangeAnalysisService(volatilityAnalysisService)
    priceChangeSimulationService = PriceChangeSimulationService(volatilityAnalysisService,plottingUtilService)

    rawDataController = RawDataController(parameterService,tickerRateService,tickerAnalysisService, tickerNameService, "raw_data.html")
    summaryAnalysisController = SummaryAnalysisController(parameterService,tickerRateService,tickerAnalysisService,
                                            bullishVsBearishAnalysisService, linearRegressionSerice,
                                            priceChangeAnalysisService, "summary_analysis.html")

    summaryAnalysisRecommendationController = SummaryAnalysisRecommendationController(parameterService, tickerRateService, tickerAnalysisService,
                                            bullishVsBearishAnalysisService, linearRegressionSerice,
                                            priceChangeAnalysisService, "recommendation.html")

    predictionController = PredictionController(parameterService,tickerRateService,tickerAnalysisService,priceChangeSimulationService, "prediction.html")
    downloadController = DownloadController(parameterService,tickerRateService)
    optionsController = OptionsController(parameterService,optionSuggestionService,optionImpliedVolatilityService,
                                          optionSuggestionColumnLabelingService,"options.html")
    profitController = ProfitController("profit.html")

    industryController = IndustryController(industryCrosstableService,visitorDbService,industryCrosstableDefaultTemplateService,"industry.html")

    stockGameService = StockGameService(parameterService,tickerRateService,tickerAnalysisService,priceChangeSimulationService,linearRegressionSerice,rsquareHighlighter)
    stockGameController = StockGameController(stockGameService,stockGameDbService,visitorDbService,"stock_game.html")

    return rawDataController , summaryAnalysisController , summaryAnalysisRecommendationController,\
           predictionController , downloadController,optionsController, profitController , industryController, stockGameController