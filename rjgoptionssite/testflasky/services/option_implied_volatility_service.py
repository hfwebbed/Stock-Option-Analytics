
class OptionImpliedVolatilityService:

    def __init__(self,optionSuggestionService,dataframeColumnInserterService):
        self.optionSuggestionService = optionSuggestionService
        self.dataframeColumnInserterService = dataframeColumnInserterService

    def appendMarketPriceColumns(self,df_call,df_put):

        df_call = self.appendMarketPriceColumnsToDataframe(df_call,"call")
        df_put = self.appendMarketPriceColumnsToDataframe(df_put, "put")

        return df_call, df_put

    def appendMarketPriceColumnsToDataframe(self, df , side):
        rows = df.shape[0]
        colImpliedVolatilityRequest = []
        colImpliedVolatilityResponse = []

        for row in range(rows):
            input_field = '<input  id="request_' + side + '_' + str(row) + '" value="0.00" type="number" min="0.00" step="0.01">'
            button = '<button data-rowid="' + str(row) + \
                 '" exercisePrice= ' + str(df.iloc[row]["exercisePrice"]) + \
                 ' optionSide=' + side + \
                 ' class="implied_volatility_button">get</button>'
            colImpliedVolatilityRequest.append(input_field + "$ &nbsp&nbsp" + button)
            answerSpan = '<span id="response_' + side + "_" + str(row) + '"></span>'
            colImpliedVolatilityResponse.append(answerSpan)

        df = self.dataframeColumnInserterService.insertColumnAfter(df, side + "Option", side + "MarketPrice",colImpliedVolatilityRequest)
        df = self.dataframeColumnInserterService.insertColumnAfter(df, side + "MarketPrice","implied" + side + "Volatility", colImpliedVolatilityResponse)
        return df


    def impliedCallVolatility(self, underlyingPrice, exercisePrice, days, targetPrice, interest, dividend):
        interest /= 100.0
        dividend /= 100.0
        time =  days/(365 * 1.0)

        return self.optionSuggestionService.impliedCallVolatility(underlyingPrice, exercisePrice, time, targetPrice, interest, dividend)

    def impliedPutVolatility(self, underlyingPrice, exercisePrice, time, targetPrice, interest, dividend):
        return self.optionSuggestionService.impliedPutVolatility(underlyingPrice, exercisePrice, time, targetPrice, interest, dividend)

