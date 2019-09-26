

class StockGameDbService:
    def __init__(self, connectionFactory, utils):
        self.connectionFactory = connectionFactory
        self.utils = utils

        self.SQLgetById       = "SELECT id,name,user_id FROM stock_game_ticker WHERE id=?"
        self.SQLgetByVisitor  = "SELECT id,name,user_id FROM stock_game_ticker WHERE user_id=?"
        self.SQLinsertTicker = "INSERT INTO stock_game_ticker(name,user_id) VALUES(?,?)"
        self.SQLdeleteTicker = "DELETE FROM stock_game_ticker WHERE id=?"

    def getById(self,id,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()
        stock_game_ticker = self.utils.get_as_dictionary_list(connection=connection,sql=self.SQLgetById,params=(id,))
        if len(stock_game_ticker) == 1:
            return stock_game_ticker[0]
        return None

    def getByVisitor(self,visitor,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()

        stock_game_tickers = self.utils.get_as_dictionary_list(connection=connection,sql=self.SQLgetByVisitor,params=(visitor['id'],))
        return stock_game_tickers

    def getNamesByVisitor(self,visitor):
        name_records = self.getByVisitor(visitor)
        names = []
        for item in name_records:
            names.append(item['name'])
        return names

    def create(self,name,visitor,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()
        connection.execute(self.SQLinsertTicker, (name.upper(),visitor['id']))
        connection.commit()

    def delete(self,id,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()
        connection.execute(self.SQLdeleteTicker, (id))
        connection.commit()



