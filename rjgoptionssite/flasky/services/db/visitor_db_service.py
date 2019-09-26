
class VisitorDbService:
    def __init__(self, connectionFactory, utils):
        self.connectionFactory = connectionFactory
        self.utils = utils

        self.SQLgetById = "SELECT id,ip FROM Visitors WHERE id=?"
        self.SQLgetByIp = "SELECT id,ip FROM Visitors WHERE ip=?"
        self.SQLinsertVisitor = "INSERT INTO Visitors(ip) VALUES(?)"

    def getById(self,id,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()
        visitor = self.utils.get_as_dictionary_list(connection=connection,sql=self.SQLgetById,params=(id,))
        if len(visitor) == 1:
            return visitor[0]
        return None

    def getByIp(self,ip,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()
        visitor = self.utils.get_as_dictionary_list(connection=connection,sql=self.SQLgetByIp,params=(ip,))

        if len(visitor) == 1:
            return visitor[0]
        return None

    def create(self,ip,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()
        connection.execute(self.SQLinsertVisitor, (ip,))
        connection.commit()
        visitor = self.getByIp(ip)
        return visitor

    def findOrCreate(self,ip,connection=None):
        visitor = self.getByIp(ip)
        if visitor is not None:
            return visitor
        return self.create(ip)

