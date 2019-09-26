import pandas as pd
class BullishVsBearishAnalysisService:

    def __init__(self):
        self.periods = {
            "recent3month" : [0, 93],
            "recent9month" : [0, 182],
            "recent1year"  : [0, 252],
            "recent4years" : [0, 1114],
            "past3month" : [943, 1006],
            "past9month" : [817, 1006],
            "past1year"  : [608, 1008] # o_O
        }


    def analyze_dataframe(self, df):
        bb_counts = {}
        for label , period in self.periods.items():
            bb_counts[label] = self.count_markers(df,period)

        df = self.pack_to_dataframe(bb_counts)
        return df

    # pandas count bulls and bears
    def count_markers(self,df,period):
        df = df[period[0]:period[1]]
        bearish = len(df[df["bearish"] == 'BEARISH'])
        bullish = len(df[df["bullish"] == 'BULLISH'])
        return {'bearish':bearish,'bullish':bullish}

    def pack_to_dataframe(self,bb_counts):

        df_3month =  pd.DataFrame({'recent_bullish': bb_counts['recent3month']['bullish'],
                                   'recent_bearish': bb_counts['recent3month']['bearish'],
                                   'past_bullish': bb_counts['past3month']['bullish'],
                                   'past_bearish': bb_counts['past3month']['bearish']},index=['3month'])

        df_9month = pd.DataFrame({'recent_bullish': bb_counts['recent9month']['bullish'],
                                'recent_bearish': bb_counts['recent9month']['bearish'],
                                'past_bullish': bb_counts['past9month']['bullish'],
                                'past_bearish': bb_counts['past9month']['bearish']},index=['9month'])

        df_1year = pd.DataFrame({'recent_bullish': bb_counts['recent1year']['bullish'],
                                  'recent_bearish': bb_counts['recent1year']['bearish'],
                                  'past_bullish': bb_counts['past1year']['bullish'],
                                  'past_bearish': bb_counts['past1year']['bearish']}, index=['1year'])

        df_4years = pd.DataFrame({'recent_bullish': bb_counts['recent4years']['bullish'],
                                 'recent_bearish': bb_counts['recent4years']['bearish'],
                                 'past_bullish': 0,
                                 'past_bearish': 0}, index=['4year'])
        df = pd.concat([df_3month,df_9month,df_1year,df_4years])


        df['%recent_bullish'] = 100 * (df['recent_bullish'].divide(df['recent_bullish'] + df['recent_bearish']))
        df['%past_bullish'] = 100 * (df['past_bullish'].divide(df['past_bullish'] + df['past_bearish']))

        df.set_value('4year','past_bullish',None)
        df.set_value('4year', 'past_bearish',None)
        df.set_value('4year', '%past_bullish',None)

        df = df[['recent_bullish','recent_bearish','%recent_bullish','past_bullish','past_bearish','%past_bullish']]
        return df