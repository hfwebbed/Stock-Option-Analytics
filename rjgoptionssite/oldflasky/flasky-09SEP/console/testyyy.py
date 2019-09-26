from services.option_implied_volatility_service import OptionImpliedVolatilityService
from services.option_suggestion_service import OptionSuggestionService
from services.dataframe_column_inserter_service import DataftrameColumnInserterService
import math
import pandas as pd


pd.set_option('display.width', 150)


serv = OptionImpliedVolatilityService(OptionSuggestionService(),DataftrameColumnInserterService())
print(serv)


underlyingPrice = 14.00
exercisePrice = 12.00

targetPrice = 2.20

time = 21
interest = 1.5 * 0.01
volatility = 76.5 * 0.01
dividend = 0 * 0.01

res = serv.impliedCallVolatility(underlyingPrice,exercisePrice,time,targetPrice,interest,dividend)

print(res)




