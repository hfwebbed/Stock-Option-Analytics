
class IndustryDbService():

    def __init__(self,connectionFactory,utils):
        self.connectionFactory = connectionFactory
        self.utils = utils

        self.SQLgetById = "SELECT id,name,desc,user_id FROM Industries WHERE id=?"
        self.SQLgetByUser = "SELECT id,name,desc,user_id FROM Industries WHERE user_id=?"
        self.SQLinsertIndustry =  "INSERT INTO Industries(name,desc,user_id) VALUES(?,?,?)"
        self.SQLdeleteIndustry = "DELETE FROM Industries WHERE id=?"
        self.SQLupdateIndustry = "UPDATE Industries SET name = ? , desc = ? WHERE id = ? and user_id = ?"

    def getByUser(self,user_id,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()
        industries = self.utils.get_as_dictionary_list(connection=connection,sql=self.SQLgetByUser,params=(user_id,))
        return industries


    def getById(self,id):
        connection = self.connectionFactory.get_connection()
        industries = self.utils.get_as_dictionary_list(connection=connection, sql=self.SQLgetById, params=(id,))
        if len(industries) == 1:
            return industries[0]
        return None

    def insert(self,user_id,name,connection=None):
        self.insert_full(user_id,name,None,connection)

    def insert_full(self,user_id,name,desc,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()
            result = connection.execute(self.SQLinsertIndustry,(name,desc,user_id,))
            connection.commit()
        else:
            result = connection.execute(self.SQLinsertIndustry, (name,desc,user_id,))

    def update(self,id,user_id,name,desc,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()
            connection.execute(self.SQLupdateIndustry, (name,desc,id,user_id))
            connection.commit()
        else:
            connection.execute(self.SQLupdateIndustry, (name, desc, id, user_id))


    def delete(self,id):
        connection = self.connectionFactory.get_connection()
        connection.execute(self.SQLdeleteIndustry,(id,))
        connection.commit()


class IndustryRelationsDbService:

    def __init__(self,connectionFactory,utils):
        self.connectionFactory = connectionFactory
        self.utils = utils

        self.SQLgetByUser = "SELECT * FROM Industry_Relations ir WHERE ir.user_id = ?"
        self.SQLinsertRelation = "INSERT INTO Industry_Relations(industry1_id,industry2_id,score,user_id) VALUES(?,?,?,?)"
        self.SQLupdateRelation = "UPDATE Industry_Relations ir SET ir.score=? WHERE ir.industry1_id=? and ir.industry2_id=?"

        self.SQLdeleteByUser     = "DELETE FROM Industry_Relations WHERE user_id = ?"
        self.SQLdeleteByRelation = "DELETE FROM Industry_Relations WHERE (industry1_id = ? or industry2_id = ?)"

    def getByUser(self,user_id):
        connection = self.connectionFactory.get_connection()
        industryRelations = self.utils.get_as_dictionary_list(connection=connection, sql=self.SQLgetByUser, params=(user_id,))
        return industryRelations

    def insert(self,id1,id2,score,user_id,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()
            connection.execute(self.SQLinsertRelation,(id1,id2,score,user_id,))
            #connection.execute(self.SQLinsertRelation, (id2, id1, score, user_id,))
            connection.commit()
        else:
            connection.execute(self.SQLinsertRelation, (id1, id2, score, user_id,))
            #connection.execute(self.SQLinsertRelation, (id2, id1, score, user_id,))

    def update(self,name1,name2,score,user_id):
        connection = self.connectionFactory.get_connection()
        connection.execute(self.SQLupdateRelation,(name1,name2,score,))
        connection.commit()

    def deleteByUser(self,user_id,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()
            connection.execute(self.SQLdeleteByUser, (user_id,))
            connection.commit()
        else:
            connection.execute(self.SQLdeleteByUser, (user_id,))

    def deleteByRelation(self,relation_id,connection=None):
        if connection is None:
            connection = self.connectionFactory.get_connection()
            connection.execute(self.SQLdeleteByRelation, (relation_id,relation_id))
            connection.commit()
        else:
            connection.execute(self.SQLdeleteByRelation, (relation_id,relation_id))
