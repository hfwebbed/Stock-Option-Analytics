

from services.db.connection_factory import ConnectionFactory
from services.db.utils import Utils
factory = ConnectionFactory("../db/flasky/flaskysqlite.db")
utils = Utils()
connection = factory.get_connection()

print(connection)

sqls = [
    "select * from visitors",
    "select * from industries",
    "update visitors set ip = 'xxxxxxxxx-xxxxxxxxx--xxx' where id = -4"
]


for sql in sqls:
    print("running",sql)
    result = utils.get_as_dictionary_list(connection, sql)
    for entry in result:
        print(entry)
connection.commit()
