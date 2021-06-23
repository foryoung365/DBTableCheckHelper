import pymysql

DB_CONFIG = "db.json"

class DbMgr:
    def __init__(self) -> None:
        self.conn = None
        self.cfgs = []


    def __del__(self)->None:
        if self.conn is not None:
            self.conn.close()

    def addConfig(self, host:str, user:str, passwd:str, database:str):
        for cfg in self.cfgs:
            if host == cfg["host"]:
                return 