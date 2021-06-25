# -*- coding: utf-8 -*-

from Debughelp import DEBUG_INFO
from enum import IntEnum
import json
import Constraint
import pymysql

class RuleType(IntEnum):
    RULE_TYPE_NONE              = 0
    RULE_TYPE_SINGLE_FIELD      = 1
    RULE_TYPE_IFTTT             = 2 #two fields rule, IFTTT:if this then that
    RULE_TYPE_CALCULATION       = 3 #

class Rule:
    def __init__(self) -> None:
        self.type = RuleType.RULE_TYPE_NONE

    def initFromJson(args:list):
        pass

    def getType(self)->RuleType:
        return self.type

    def getField(self)->str:
        return self.field

    def run(self, row)->list:
        pass

class TableCheckError(IntEnum):
    TABLE_CHECK_OK                  = 0
    TABLE_CHECK_NO_DATA_OR_ERROR    = 1
    TABLE_CHECK_FAILED              = 2

class DbTable:
    def __init__(self, cursor:pymysql.cursors.Cursor, table:str = None, jsonR:str=None) -> None:
        self.table = table
        self.cursor = cursor
        self.rules = []

        if jsonR is not None:
            self.initFromJson(jsonR)

        self.initFields()

    def initFromJson(self, jsonR:str):
        res = json.loads(jsonR)
        self.table = str(res["table"])
        for r in res["rules"]:
            if r["type"] == RuleType.RULE_TYPE_SINGLE_FIELD:
                self.rules.append(RuleSingleField(self, self.cursor, args=r))
            elif r["type"] == RuleType.RULE_TYPE_IFTTT:
                self.rules.append(RuleIFTTT(self, self.cursor, args=r))
            elif r["type"] == RuleType.RULE_TYPE_CALCULATION:
                self.rules.append(RuleCalc(self, self.cursor, args=r))

    def initFields(self):
        sql = "DESCRIBE {table}".format(self.table)
        self.cursor.execute(sql)
        self.fields = []

        res = self.cursor.fetchall()
        for r in res:
            self.fields.append(r[0])
        
    def getFieldIndex(self, field:str)->int:
        return self.fields.index(field)


    def getErrorStr(self, err:TableCheckError):
        if err == TableCheckError.TABLE_CHECK_OK:
            return "表【{table}】校验通过。".format(self.table)
        elif err == TableCheckError.TABLE_CHECK_NO_DATA_OR_ERROR:
            return "表【{table}】不存在或者无数据。".format(self.table)
        elif err == TableCheckError.TABLE_CHECK_FAILED:
            return "表【{table}】校验失败。".format(self.table)

    def checkTable(self)->str:
        sql = "SELECT * FROM {table}".format(self.table)
        self.cursor.execute(sql)

        txt = "开始校验表【{t}】：\n".format(t=self.table)

        res = self.cursor.fetchall()
        if res is None or len(res) <= 0:
            txt += self.getErrorStr(TableCheckError.TABLE_CHECK_NO_DATA_OR_ERROR)
            return txt

        result = []
        for row in res:
            for rule in self.rules:
                result += rule.run(row)

        for r in result:
            txt += r + "\n"

        if len(result) > 0:
            txt += self.getErrorStr(TableCheckError.TABLE_CHECK_FAILED)
            return txt
        else:
            txt += self.getErrorStr(TableCheckError.TABLE_CHECK_OK)
            return txt
    
'''
"tables":[
    {"table": "cq_xxx", 
        "rules": [
            {"type":1, "field": "id", constraints:[...]
            },
            {"type":2, }
            ...
        ]
    },
    ...
]
'''

class RuleSingleField(Rule):
    def __init__(self, table:DbTable, cursor:pymysql.cursors.Cursor, field:str = None, args:dict = None) -> None:
        self.type = RuleType.RULE_TYPE_SINGLE_FIELD
        self.table = table
        self.field = field
        self.cursor = cursor
        self.constraints = []


        if args is not None:
            self.initFromJson(args)

    def initFromJson(self, args:dict)->None:
        DEBUG_INFO(args)
        self.type = RuleType(args["type"])
        self.field = str(args["field"])
        
        for c in args["constraints"]:
            if c["type"] == Constraint.ConstraintType.CONSTRAINT_VALUE_RANGE:
                self.constraints.append(Constraint.ConstraintValueRange(c))
            elif c["type"] == Constraint.ConstraintType.CONSTRAINT_TABLE_REFERENCE:
                self.constraints.append(Constraint.ConstraintTableReference(self.cursor, c))

    def getErrorStr(self, err:Constraint.ConstraintError)->str:
        c = Constraint()
        return "字段({f})校验失败：{e})".format(f = self.field, e = c.getErrorString(err))

    def run(self, row)->list:
        idx = self.table.getFieldIndex(self.field)

        result = []
        for constraint in self.constraints:
            err = constraint.verify(row[idx])
            if err != Constraint.ConstraintError.CONSTRAINT_ERROR_OK:
               result.append(self.getErrorString(err, self.field))

        return result

class RuleIFTTT:
    def __init__(self, table:DbTable, cursor:pymysql.cursors.Cursor, field1:str = None, field2:str = None, args:dict = None) -> None:
        self.type = RuleType.RULE_TYPE_IFTTT
        self.table = table
        self.field1 = field1
        self.field2 = field2
        self.cursor = cursor
        self.constraints = []


class RuleCalc(Rule):
    def __init__(self, table:DbTable, cursor:pymysql.cursors.Cursor, field1:str = None, field2:str = None, args:dict = None) -> None:
        self.type = RuleType.RULE_TYPE_CALCULATION
        self.table = table
        self.field1 = field1
        self.field2 = field2
        self.cursor = cursor
        self.expr = ""

    def getErrorStr(self)->str:
        return "字段({f1})校验失败：{f1}{expr}!={f2})".format(f1 = self.field1, expr = self.expr, f2 = self.field2)

    def initFromJson(self, args:dict):
        DEBUG_INFO(args)
        self.type = RuleType(args["type"])
        self.field1 = str(args["field1"])
        self.field2 = str(args["field2"])
        
        self.expr = str(args["expr"])

    def run(self, row)->list:
        idx1 = self.table.getFieldIndex(self.field1)
        idx2 = self.table.getFieldIndex(self.field2)

        result = []
        v1 = eval(self.expr.format(f=row[idx1]))
        v2 = row[idx2]

        if v1 != v2:
            result.append(self.getErrorStr())

        return result