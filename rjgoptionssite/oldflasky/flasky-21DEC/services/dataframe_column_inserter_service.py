import pandas as pd
class DataftrameColumnInserterService:

    def __init__(self):
        pass

    def insertColumnAfter(self,df,afterColumn,newColumnName,newColumnContent):
        before = []
        after = []
        beforeComplete = False

        for column in list(df.columns.values):
            if beforeComplete:
                after.append(column)
            else:
                before.append(column)
                if column == afterColumn:
                    beforeComplete = True


        df_before = df[before]
        df_after = df[after]
        df_new = pd.DataFrame({newColumnName:newColumnContent})
        df = pd.concat([df_before,df_new,df_after],axis=1)
        return df
