# -*- coding: utf-8 -*-

from enum import Enum
import json

import pymysql
from Debughelp import DEBUG_INFO

class ConstraintType(Enum):
    CONSTRAINT_VALUE_RANGE          = 1
    CONSTRAINT_TABLE_REFERENCE      = 2

class ConstraintError(Enum):
    CONSTRAINT_ERROR_OK                         = 0 #成功
    CONSTRAINT_ERROR_ALREADY_EXISTS             = 1 #已存在
    CONSTRAINT_ERROR_OUT_OF_RANGE               = 2 #超出范围
    CONSTRAINT_ERROR_BAD_SQL                    = 3 #执行SQL失败
    CONSTRAINT_ERROR_REF_NOT_EXISTS             = 4 #关联对象不存在

class Constraint:
    def verify(self, field)->ConstraintError:
        pass
    
    def getErrorString(self, err: ConstraintError)->str:
        if err == ConstraintError.CONSTRAINT_ERROR_OK:
            return "成功"
        elif err == ConstraintError.CONSTRAINT_ERROR_ALREADY_EXISTS:
            return "该配置已存在"
        elif err == ConstraintError.CONSTRAINT_ERROR_OUT_OF_RANGE:
            return "超出范围"
        elif err == ConstraintError.CONSTRAINT_ERROR_BAD_SQL:
            return "SQL执行失败"
        elif err == ConstraintError.CONSTRAINT_ERROR_REF_NOT_EXISTS:
            return "关联表或字段不存在指定值"

    def getDescString(self)->str:
        pass

    def getContentString(self)->str:
        pass

'''
"constraints":[
    {"type": 1, "content": [{"min":minV, "max": maxV}, {"min":minV, "max": maxV}, ..., {"min":minV, "max": maxV}]},
    ...
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
        DEBUG_INFO(jsonR)
        self.ranges += json.loads(jsonR)

        return ConstraintError.CONSTRAINT_ERROR_OK

    def verify(self, field) -> ConstraintError:
        DEBUG_INFO((self.ranges, field))

        bValid = False
        for range in self.ranges:           
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
    def __init__(self, dbCursor: pymysql.cursors.Cursor, refs : str = None) -> None:
        self.cursor = dbCursor
        DEBUG_INFO(refs)
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
        DEBUG_INFO(jsonR)
        self.refs += json.loads(jsonR)
        return ConstraintError.CONSTRAINT_ERROR_OK

    def makeSQL(self, fieldV)->list:
        sqls = []
        for ref in self.refs:
            sql = "SELECT {field} FROM {table} WHERE {field} = {value}".format(field=ref["field"], table=ref["table"], value=fieldV)
            sqls.append(sql)

        return sqls

    def getDescString(self)->str:
        return "字段值必须在以下表的字段中存在对应值：\n"

    def getContentString(self)->str:
        template = "{table}.{field}\n"

        text = ""
        for ref in self.refs:
            text += template.format(table=ref["table"], field=ref["field"])

        return text

    def verify(self, field) -> ConstraintError:
        sqls = self.makeSQL(field)
        for sql in sqls:
            DEBUG_INFO(sql)
            try:
                if not self.cursor.execute(sql) > 0:
                    return ConstraintError.CONSTRAINT_ERROR_REF_NOT_EXISTS
            except:
                return ConstraintError.CONSTRAINT_ERROR_BAD_SQL

        return ConstraintError.CONSTRAINT_ERROR_OK


if __name__ == '__main__':
    conn = pymysql.connect("172.24.140.83", "wjq", "wjq")
    conn.select_db("xsjmygf_0621wb")
    cursor = conn.cursor()

    ctr = ConstraintTableReference(cursor)
    ctr.addRef("cq_magictype", "id")
    print(ctr.verify(12345))

    cvr = ConstraintValueRange()
    cvr.addRange(1, 5)
    cvr.addRange(2, 4)
    cvr.addRange(10, 20)
    print(cvr.verify(6))
    print(cvr.verify(0))
    print(cvr.verify(3))
    print(cvr.verify(10))
    print(cvr.addRange(50,50))

    print(ctr.getDescString(), ctr.getContentString())
    print(cvr.getDescString(), cvr.getContentString())
    


