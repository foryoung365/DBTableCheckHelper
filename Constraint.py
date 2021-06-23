# -*- coding: utf-8 -*-

from enum import Enum
import json

import Global

import pymysql

class ConstraintType(Enum):
    CONSTRAINT_VALUE_RANGE = 1

class ConstraintError(Enum):
    CONSTRAINT_ERROR_OK                         = 0 #成功
    CONSTRAINT_ERROR_ALREADY_EXISTS             = 1 #已存在
    CONSTRAINT_ERROR_OUT_OF_RANGE               = 2 #超出范围

class Constraint:
    def verify(self, field)->ConstraintError:
        pass
    
    def getErrorString(self, err: ConstraintError)->str:
        pass

    def getDescString(self)->str:
        pass

    def getContentString(self)->str:
        pass

'''
"constraint":[
    {"type": 1, "content": [{"min":minV, "max": maxV}, {"min":minV, "max": maxV}, ..., {"min":minV, "max": maxV}]},

]
'''
class ConstraintValueRange(Constraint):
    def __init__(self, ranges : str = None ) -> None:
        super().__init__()
        if ranges is None:
            self.ranges = []
        else:
            self.addRangeFromJson(ranges)

    def addRange(self, minV, maxV)->ConstraintError:
        for range in self.ranges:
            if range["min"] <= minV and range["max"] >= maxV:
                return ConstraintError.CONSTRAINT_ERROR_ALREADY_EXISTS
        pair = {"min" : minV, "max": maxV}
        self.ranges.append(pair)
        return ConstraintError.CONSTRAINT_ERROR_OK
    
    def addRangeFromJson(self, jsonR:str)->ConstraintError:
        self.ranges += json.loads(jsonR)

        return ConstraintError.CONSTRAINT_ERROR_OK

    def verify(self, field) -> ConstraintError:
        for range in self.ranges:
            bValid = False
            if field >= range["min"] and field <= range["max"]:
                bValid = True
            if not bValid:
                return ConstraintError.CONSTRAINT_ERROR_OUT_OF_RANGE
        
        return ConstraintError.CONSTRAINT_ERROR_OK

    def getRanges(self)->list:
        return self.ranges

    def getDescString(self) -> str:
        return "取值必须在以下范围（左右均为闭区间）：\n"
    
    def getContentString(self)->str:
        template = "[{min}, {max}]\n"
        text = ""
        for range in self.ranges:
            text += template.format(min=range["min"], max=range["max"])
        return text

class ConstraintTableReference(Constraint):
    def __init__(self, refs : str = None) -> None:
        if refs is None:
            self.refs = []
        else:
            self.addRefFromJson(refs)

    def addRef(self, tbl : str, field : str)->ConstraintError:
        for ref in self.refs:
            if ref["table"] == tbl and ref["field"] == field:
                return ConstraintError.CONSTRAINT_ERROR_ALREADY_EXISTS
        pair = {"table":tbl, "field":field}
        self.refs.append(pair)

        return ConstraintError.CONSTRAINT_ERROR_OK

    def addRefFromJson(self, jsonR:str)->ConstraintError:
        self.refs += json.loads(jsonR)
        return ConstraintError.CONSTRAINT_ERROR_OK

    def verify(self, field) -> ConstraintError:
        global g_db
        

conn = pymysql.connect(host="172.24.140.83",user="wjq", passwd="wjq", port=3306, client_flag = 1)
conn.select_db("xsjmygf_0616")
cur = conn.cursor()
sql = "SELECT * FROM cq_user LIMIT 1"
cur.execute(sql)
print(cur.fetchall())

