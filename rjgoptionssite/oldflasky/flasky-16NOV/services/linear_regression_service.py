from scipy import stats
import numpy as np
import pandas as pd

from pandas.formats.style import Styler


class LinearRegressionSerice:

    def __init__(self):

        self.periods = {
            "recent9month": [0, 189],
            "recent1year": [0, 251],
            "recent4years": [0, 1009]
        }
        pass


    def calculate_slope_and_rsquare(self,df,styling=True):
        period_data = {}
        for tag,period in self.periods.items():
            period_data[tag] = self.calculate_slope_and_rsquare_for_period(df,period)
        df = self.pack_to_dataframe(period_data,styling=styling)
        return df


    def calculate_slope_and_rsquare_for_period(self,df,period=None):
        if period is not None:
            df = df[period[0]:period[1]]
        df = df.reindex(index=df.index[::-1])
        df['Days'] = (df.index - df.index[0]).days
        return self.calculate_slope_and_rsquare_for_dataframe(df,"Days","Close")


    def calculate_slope_and_rsquare_for_dataframe(self,df,x,y):
        return self.calculate_slope_and_rsquare_kernel(df[x], df[y])


    def calculate_slope_and_rsquare_kernel(self,x,y):
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        return {"slope": slope, "r_squared": r_value ** 2}

    def pack_to_dataframe(self,period_data,styling=True):
        df_9month = pd.DataFrame({'slope': period_data['recent9month']['slope'],
                                 'r_squared': period_data['recent9month']['r_squared']}, index=['9month'])

        df_1year = pd.DataFrame({'slope': period_data['recent1year']['slope'],
                                  'r_squared': period_data['recent1year']['r_squared']}, index=['1year'])

        df_4years = pd.DataFrame({'slope': period_data['recent4years']['slope'],
                          'r_squared': period_data['recent4years']['r_squared']}, index=['4years'])
        df = pd.concat([df_9month, df_1year, df_4years])

        if styling:
            return self.apply_styling(df)
        else:
            return df


    def apply_styling(self,df):
        styler = Styler(df)
        styler = styler.apply(highlight_rsquare,subset=["r_squared"])
        return styler

    def rsquare_group(self,v):
        if v < 0.33:
            return 0
        elif v > 0.66:
            return 2
        else:
            return 1


def highlight_rsquare(x):
    style = []
    for v in x:
        if v < 0.33:
            style.append('background-color: red')
        elif v > 0.66:
            style.append('background-color: green')
        else:
            style.append('background-color: yellow')
    return

