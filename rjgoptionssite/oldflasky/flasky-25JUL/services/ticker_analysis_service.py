
class TickerAnalysisService:

    def __init__(self):
        self.MARKER_DEFAULT = 'no'
        self.FITS_BITCH_MARKER = 'FITS BITCH'
        self.VOLUME_DECREASE_FITS_BITCH = -8.00
        pass

    def analyze_dataframes(self,dfs):
        new_dataframes = {}
        for ticket,df in dfs.items():
            new_dataframes[ticket] = self.analyze_dataframe(df)
        return new_dataframes

    def analyze_dataframe(self,df):
        if df is None:
            return None
        df = self.add_adjusted_close(df)
        df = self.add_adjusted_close_difference(df)
        df = self.add_volume_difference(df)
        df = self.add_volume_decrease_marker(df)
        df = self.add_high_raises_marker(df)
        df = self.add_low_drops_marker(df)
        df = self.add_close_below_last_high_marker(df)
        df = self.add_close_above_last_low_marker(df)
        df = self.add_bullish_marker(df)
        df = self.add_bearish_marker(df)

        df = self.clean(df)
        return df

    def add_adjusted_close(self,df):
        return df.assign(adjclose=df['Close'])

    def add_adjusted_close_difference(self,df):
        return df.assign(adjclosediff= ((df['Close'] - df['Close'].shift(1)) / df['Close']) * 100)

    def add_volume_difference(self,df):
        return df.assign(volumediff = ((df['Volume'] - df['Volume'].shift(1))/df['Volume']) * 100)

    def add_volume_decrease_marker(self,df):
        df['volume_decrease'] = self.MARKER_DEFAULT
        df.loc[df['volumediff'] < self.VOLUME_DECREASE_FITS_BITCH , 'volume_decrease'] = self.FITS_BITCH_MARKER
        return df

    def add_high_raises_marker(self,df):
        df['high_raises'] = self.MARKER_DEFAULT
        df.loc[df['High'] > df['High'].shift(-1),'high_raises'] = self.FITS_BITCH_MARKER
        return df

    def add_low_drops_marker(self, df):
        df['low_drops'] = self.MARKER_DEFAULT
        df.loc[df['Low'] < df['Low'].shift(-1),'low_drops'] = self.FITS_BITCH_MARKER
        return df

    def add_close_below_last_high_marker(self,df):
        df['close_below_last_high'] = self.MARKER_DEFAULT
        df.loc[df['Close'] < df['High'].shift(-1),'close_below_last_high'] = self.FITS_BITCH_MARKER
        return df

    def add_close_above_last_low_marker(self,df):
        df['close_above_last_low'] = self.MARKER_DEFAULT
        df.loc[df['Close'] > df['Low'].shift(-1),'close_above_last_low'] = self.FITS_BITCH_MARKER
        return df

    def add_bullish_marker(self,df):
        df['bullish'] = ""
        df['FITS_BITCH_MARKER'] = self.FITS_BITCH_MARKER

        df.loc[(df['volume_decrease'] == df['FITS_BITCH_MARKER']) &
               (df['high_raises'] == df['FITS_BITCH_MARKER']) &
               (df['close_below_last_high'] == df['FITS_BITCH_MARKER']),'bullish'] = 'BULLISH'
        return df

    def add_bearish_marker(self, df):
        df['bearish'] = ""

        df['FITS_BITCH_MARKER'] = self.FITS_BITCH_MARKER
        df.loc[(df['volume_decrease'] == df['FITS_BITCH_MARKER']) &
               (df['low_drops'] == df['FITS_BITCH_MARKER']) &
               (df['close_above_last_low'] == df['FITS_BITCH_MARKER']), 'bearish'] = 'BEARISH'
        return df


    def clean(self,df):
        df = df.drop('FITS_BITCH_MARKER', 1)
        return df




