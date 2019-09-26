

from services.db.connection_factory import ConnectionFactory
from services.db.utils import Utils
factory = ConnectionFactory("../db/flaskysqlite.db")
utils = Utils()
connection = factory.get_connection()

print(connection)

sqls = [
    "select * from stock_game_ticker",
    "update stock_game_ticker set user_id = -6 where user_id = 6"
]

for sql in sqls:
    print("running",sql)
    result = utils.get_as_dictionary_list(connection, sql)
    for entry in result:
        print(entry)
connection.commit()
