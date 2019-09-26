
class Utils:

    def __init__(self):
        pass

    def get_as_dictionary_list(self,connection,sql,params=()):
        query_result = connection.execute(sql,params)
        rows = []
        for row in query_result:
            rows.append(self.row_to_dictionary(query_result, row))
        return rows

    def row_to_dictionary(self,query_result,row):
        return {k[0]: v for k, v in list(zip(query_result.description, row))}
