from flask import render_template
from flask import jsonify

class OptionsController:
    def __init__(self,parameterService, optionSuggestionService, optionImpliedVolatilityService, optionSuggestionColumnLabelingService, template):
        self.parameterService = parameterService
        self.optionSuggestionService = optionSuggestionService
        self.optionImpliedVolatilityService = optionImpliedVolatilityService
        self.optionSuggestionColumnLabelingService = optionSuggestionColumnLabelingService
        self.template = template

    def dispatch(self, request):
        df_call = None
        df_put = None
        underlyingPrice, days, volatility,interest, dividend = self.parameterService.init_option_controller_params()

        if request.method == 'POST':
            underlyingPrice, days, volatility,interest, dividend = self.parameterService.process_options_params(request)
            df_call, df_put = self.optionSuggestionService.calculate_options(underlyingPrice,days,volatility,interest, dividend)
            df_call, df_put = self.optionImpliedVolatilityService.appendMarketPriceColumns(df_call,df_put)

            self.optionSuggestionColumnLabelingService.rename_call(df_call)
            self.optionSuggestionColumnLabelingService.rename_put(df_put)

        return render_template(self.template,underlyingPrice=underlyingPrice,
                               days=days,volatility=volatility,interest=interest,dividend=dividend,
                               df_call=df_call,df_put=df_put)


    def serveImpliedVolatility(self,request):
        optionSide , underlyingPrice, exercisePrice, days, targetPrice, interest, dividend = self.parameterService.process_options_params_ajax(request)

        if optionSide == "call":
            result = self.optionImpliedVolatilityService.impliedCallVolatility(underlyingPrice, exercisePrice, days , targetPrice, interest, dividend)
        else:
            result = self.optionImpliedVolatilityService.impliedPutVolatility(underlyingPrice, exercisePrice, days,targetPrice, interest, dividend)

        return jsonify(result=result)

