import math
import pandas as pd
from scipy.stats import norm


class OptionSuggestionService:

    def __init__(self):
        pass

    def calculate_options(self,underlyingPrice,days,volatility,interest,dividend):

        volatility /= 100
        interest /= 100
        dividend /= 100
        optime = days / (365 * 1.0)

        exercisePrices = []
        for dif in range(-5,6):
            exercisePrices.append(underlyingPrice + 0.5 * dif)

        df = pd.DataFrame({"exercisePrice":exercisePrices})
        df = df.assign(putDelta=df.exercisePrice.apply(lambda e_price: self.putDelta(underlyingPrice, e_price, optime, volatility, interest, dividend)))
        df = df.assign(callDelta=df.exercisePrice.apply(
            lambda e_price: self.callDelta(underlyingPrice, e_price, optime, volatility, interest, dividend)))
        df = df.assign(putTheta=df.exercisePrice.apply(
            lambda e_price: self.putTheta(underlyingPrice, e_price, optime, volatility, interest, dividend)))
        df = df.assign(callTheta=df.exercisePrice.apply(
            lambda e_price: self.callTheta(underlyingPrice, e_price, optime, volatility, interest, dividend)))
        df = df.assign(putRho=df.exercisePrice.apply(
            lambda e_price: self.putRho(underlyingPrice, e_price, optime, volatility, interest, dividend)))
        df = df.assign(callRho=df.exercisePrice.apply(
            lambda e_price: self.callRho(underlyingPrice, e_price, optime, volatility, interest, dividend)))
        df = df.assign(gamma=df.exercisePrice.apply(
            lambda e_price: self.gamma(underlyingPrice, e_price, optime, volatility, interest, dividend)))
        df = df.assign(vega=df.exercisePrice.apply(
            lambda e_price: self.vega(underlyingPrice, e_price, optime, volatility, interest, dividend)))

        df = df.assign(callOption=df.apply(
            lambda row: self.callOption(underlyingPrice, row["exercisePrice"], optime, volatility, interest, dividend),axis=1))
        df = df.assign(putOption=df.apply(
            lambda row: self.putOption(underlyingPrice, row["exercisePrice"], optime, volatility, interest, dividend),axis=1))

        df['callXTM'] = "ATM"
        df.loc[df['exercisePrice'] < underlyingPrice , 'callXTM'] = 'ITM'
        df.loc[df['exercisePrice'] > underlyingPrice, 'callXTM'] = 'OTM'

        df['putXTM'] = "ATM"
        df.loc[df['exercisePrice'] < underlyingPrice, 'putXTM'] = 'OTM'
        df.loc[df['exercisePrice'] > underlyingPrice, 'putXTM'] = 'ITM'

        """
        df = df.assign(impliedCallVolatilityX=df.apply(
            lambda row: self.impliedCallVolatility(underlyingPrice, row["exercisePrice"], days / 365,  2.2 ,interest,dividend), axis=1))
        df = df.assign(impliedPutVolatility=df.apply(
            lambda row: self.impliedPutVolatility(underlyingPrice, row["exercisePrice"], days / 365, 2.2 ,interest,dividend), axis=1))
        """

        df_call = df[["exercisePrice","callXTM","callOption","callDelta","gamma","vega","callTheta","callRho"]]
        df_put = df[["exercisePrice","putXTM","putOption","putDelta", "gamma", "vega", "putTheta", "putRho"]]

        return df_call , df_put


    def volatility_factor(self,volatility,time):
        return volatility * math.sqrt(time)


    def dOne(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):

        return (math.log(underlyingPrice / exercisePrice) + (interest - dividend + 0.5 * volatility**2) * time) / self.volatility_factor(volatility,time)

    def ndOne(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        dOne = self.dOne(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        return math.exp(-0.5 * (dOne**2)) / (math.sqrt(2 * math.pi))

    def dTwo(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        return self.dOne(underlyingPrice, exercisePrice, time, volatility, interest, dividend) - self.volatility_factor(volatility ,time)

    def ndTwo(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        dTwo = self.dTwo(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        return norm.cdf(dTwo)

    def callOption(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        dOne = self.dOne(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        dTwo = self.dTwo(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        return math.exp(- dividend * time) * underlyingPrice * norm.cdf(dOne) - exercisePrice * math.exp(-interest * time) * norm.cdf(dTwo)

    def putOption(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        dOne = self.dOne(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        dTwo = self.dTwo(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        return exercisePrice * math.exp(-interest * time) * norm.cdf(-1 * dTwo) - math.exp(-dividend * time) * underlyingPrice * norm.cdf(-dOne)


    def callDelta(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        dOne = self.dOne(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        return norm.cdf(dOne)

    def putDelta(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        return self.callDelta(underlyingPrice, exercisePrice, time, volatility, interest, dividend) - 1


    def callTheta(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        ndOne = self.ndOne(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        ndTwo = self.ndTwo(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        ct = -(underlyingPrice * volatility * ndOne) / (2 * math.sqrt(time)) - interest * exercisePrice * math.exp(-interest * time) * ndTwo
        return ct / 365

    def putTheta(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        ndOne = self.ndOne(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        ndTwo = self.ndTwo(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        pt = - (underlyingPrice * volatility * ndOne) / (2 * math.sqrt(time)) + interest * exercisePrice * math.exp(- interest * time) * (1 - ndTwo)
        return pt / 365


    def gamma(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        ndOne = self.ndOne(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        return ndOne / ( underlyingPrice * volatility * math.sqrt(time))

    def vega(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        ndOne = self.ndOne(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        return 0.01 * underlyingPrice * math.sqrt(time) * ndOne


    def callRho(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        dTwo = self.dTwo(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        return 0.01 * exercisePrice * time * math.exp(-interest * time) * norm.cdf(dTwo)

    def putRho(self,underlyingPrice, exercisePrice, time, volatility, interest, dividend):
        dTwo = self.dTwo(underlyingPrice, exercisePrice, time, volatility, interest, dividend)
        return - 0.01 * exercisePrice * time * math.exp(-interest * time) * (1 - norm.cdf(dTwo))

    def avg(self,high,low):
        return (high + low) / 2.0

    def impliedCallVolatility(self, underlyingPrice, exercisePrice, time, targetPrice, interest, dividend):
        high = 5
        low = 0

        while (high - low) > 0.0001:
            median = self.avg(high,low)
            if self.callOption(underlyingPrice, exercisePrice, time, median, interest,dividend) > targetPrice:
                high = median
            else:
                low = median
        return median


    def impliedPutVolatility(self, underlyingPrice, exercisePrice, time, targetPrice, interest, dividend):
        high = 5
        low = 0

        while(high - low ) > 0.0001:
            median = self.avg(high, low)
            if self.putOption(underlyingPrice, exercisePrice, time, median, interest,  dividend) > targetPrice:
                high = median
            else:
                low = median
        return median

