from services.dataframe_column_inserter_service import DataftrameColumnInserter
import pandas as pd

inserter = DataftrameColumnInserter()


df = pd.DataFrame({"foo":[1,2,3],"bar":[2,3,4],"baz":[4,4,4]})
df = df[["foo","bar","baz"]]

res = inserter.insertColumnAfter(df,"foo",'c','<input name="marketPrice1" id="marketPrice1" value="{{marketPrice or 0.00}}" type="number" min="0.00" step="0.01">')
print(res)


