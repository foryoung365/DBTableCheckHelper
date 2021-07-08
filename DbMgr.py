import json
import pymysql
from enum import IntEnum

from pymysql import cursors

from Debughelp import DEBUG_INFO

DB_CONFIG = "db.json"

class DbError(IntEnum):
    DB_ERROR_OK                     = 0
    DB_ERROR_ALREADY_EXISTS         = 1
    DB_ERROR_CONN_FAILED            = 2
    DB_ERROR_NOT_EXIST              = 3

"""
{
    "databases": [
        {"host":xxx, "user":xxx, "password":xxx},
        ...
    ]
}
"""

class DbMgr:
    def __init__(self, cfgfile:str = None) -> None:
        self.conn = None
        self.cfgs = []
        self.selectedHost = None
        self.selectedDb = None

        if cfgfile is not None:
            self.addConfigFromJson(cfgfile)

    def __del__(self)->None:
        self.reset()

    def addConfigFromJson(self, jsonDb:str)->DbError:
        DEBUG_INFO(jsonDb)
        try:
            with open(jsonDb, 'r', encoding="utf-8") as cfg:
                self.cfgs = json.load(cfg)["databases"]
        except:
            self.cfgs = []
        DEBUG_INFO(self.cfgs)

    def reset(self)->None:
        if self.conn is not None:
            self.conn.close()
            self.selectedDb = None

    def addConfig(self, host:str, user:str, passwd:str)->DbError:
        for cfg in self.cfgs:
            if host == cfg["host"]:
                return DbError.DB_ERROR_ALREADY_EXISTS
        
        newCfg = {"host":host, "user":user, "password":passwd}
        DEBUG_INFO(newCfg)
        self.cfgs.append(newCfg)

        return DbError.DB_ERROR_OK

    def getConfigList(self)->list:
        return self.cfgs

    def setSelectedHost(self, host:str)->bool:
        found = False
        for cfg in self.cfgs:
            if host == cfg["host"]:
                self.selectedHost = host
                found = True
        
        return found

    def getSelectedConfig(self)->dict:
        for cfg in self.cfgs:
            if self.selectedHost == cfg["host"]:
                return cfg

        return None

    def Connect(self)->pymysql.Connection:
        self.reset()

        if self.selectedHost is None:
            return None
        
        cfg = self.getSelectedConfig()

        DEBUG_INFO(cfg)
        try:
            self.conn = pymysql.connect(cfg["host"], cfg["user"], cfg["password"])
        except:
            return None

        return self.conn

    def getDbList(self)->list:
        if self.conn is None:
            return None
        sql = "show databases"
        
        cursor = self.conn.cursor()
        cursor.execute(sql)

        res = cursor.fetchall();

        dblist = []
        for r in res:
            dblist.append(r[0])

        return dblist

    def setSelectedDb(self, db:str):
        self.selectedDb = db
        if self.conn is not None:
            self.conn.select_db(db)
        
    def getSelectedDb(self)->str:
        return self.selectedDb

    def toJson(self)->dict:
        dblist = []
        for c in self.cfgs:
            dblist.append({"host": c["host"], "user": c["user"], "password": c["password"]})

        return { "databases": dblist }

    def saveFile(self):
        with open(DB_CONFIG, "w+") as f:
            json.dump(self.toJson(), f)

if __name__ == '__main__':
    db = DbMgr()

    db.addConfig("172.24.140.83", "wjq", "wjq")
    print(db.getConfigList())
    print(db.setSelectedHost("172.24.140.83"))
    print(db.Connect())
    print(db.getDbList())
    db.setSelectedDb("xsjmygf_0621wb")
    print(db.selectedDb)
    print(0 == DbError.DB_ERROR_OK)