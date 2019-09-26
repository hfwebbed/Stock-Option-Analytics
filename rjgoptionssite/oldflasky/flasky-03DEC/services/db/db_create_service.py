import sqlite3
from sqlite3 import Error




class CreateDbService:

    def __init__(self):
        self.db_available = False
        try:
            self.db = sqlite3.connect("../db/flaskysqlite.db")
            self.db_available = True

            self.sqls = [

                "CREATE TABLE visitors(id integer PRIMARY KEY AUTOINCREMENT,ip text not null)",
                "CREATE INDEX visitors_id_index ON visitors(id)",
                "CREATE INDEX visitors_ip_index ON visitors(ip)",

                "create table users( id integer PRIMARY KEY,name text NOT NULL)",
                "CREATE INDEX users_id_index ON users(id)",
                "CREATE INDEX users_name_index ON users(name)",


                "create table industries( id integer PRIMARY KEY AUTOINCREMENT,name text NOT NULL,desc text ,user_id integer)",
                "CREATE INDEX industries_user_id ON industries(user_id)",

                "create table industry_relations( id integer PRIMARY KEY,industry1_id integer,industry2_id integer,score integer,user_id integer)",
                "CREATE INDEX industry_relations__user_id ON industry_relations(user_id)",

                "Insert into users(name) values('rgj')",
                "Insert into users(name) values('algis')",

                "Insert into industries(name,desc,user_id) values('foo','footabll management',1)",
                "Insert into industries(name,desc,user_id) values('bar','chocolate bars',1)",
                "Insert into industries(name,desc,user_id) values('baz','bazaar style markets',1)",

                "Insert into industry_relations(industry1_id,industry2_id,score,user_id) values(1,2,1,1)",
                "Insert into industry_relations(industry1_id,industry2_id,score,user_id) values(3,2,2,1)",

                "Select * from users",
                "Select * from industries",
                "Select * from industry_relations",

            ]

            for sql in self.sqls:
                result = self.db.execute(sql)
                print(sql,result)
                for data in result:
                    print("    ",data)
            self.db.commit()
        except Error as e:
            print("DB NOT AVAILABLE",e)
            pass

    def execute_query(self,sql):
        self.db.execute(sql)


dbs = CreateDbService()







