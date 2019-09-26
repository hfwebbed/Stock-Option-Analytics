
class OptionSuggestionColumnLabelingService:

    def __init__(self):
        pass



    #zorg	callXTM	callOption	callMarketPrice	impliedcallVolatility	callDelta	gamma	vega	callTheta	callRho

    def rename_call(self,df_call):

        df_call.columns.values[0] = 'Strike Prices'
        df_call.columns.values[1] = ' '
        df_call.columns.values[2] = 'Theoretical Market Price'
        df_call.columns.values[3] = 'Market Price'
        df_call.columns.values[4] = 'Implied Volatility'

        df_call.columns.values[5] = 'Delta'
        df_call.columns.values[6] = 'Gamma'
        df_call.columns.values[7] = 'Vega'
        df_call.columns.values[8] = 'Theta'
        df_call.columns.values[9] = 'Rho'

    def rename_put(self,df_put):
        df_put.columns.values[0] = 'Strike Prices'
        df_put.columns.values[1] = ' '
        df_put.columns.values[2] = 'Theoretical Market Price'
        df_put.columns.values[3] = 'Market Price'
        df_put.columns.values[4] = 'Implied Volatility'

        df_put.columns.values[5] = 'Delta'
        df_put.columns.values[6] = 'Gamma'
        df_put.columns.values[7] = 'Vega'
        df_put.columns.values[8] = 'Theta'
        df_put.columns.values[9] = 'Rho'
