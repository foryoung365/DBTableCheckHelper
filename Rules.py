# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox
from pymysql import constants
from Debughelp import DEBUG_INFO
from enum import IntEnum
import json
import Constraint
import pymysql
import traceback

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
        pass

    def run(self, row, cursor:pymysql.cursors.Cursor)->list:
        pass

    def getDesc(self)->str:
        pass

    def isValid(self)->bool:
        pass

    def toJson(self)->dict:
        pass

class TableCheckError(IntEnum):
    TABLE_CHECK_OK                  = 0
    TABLE_CHECK_NO_DATA_OR_ERROR    = 1
    TABLE_CHECK_FAILED              = 2

class DbTable:
    def __init__(self, table:str = None, jsonR:str=None) -> None:
        self.table = table
        self.rules = []

        if jsonR is not None:
            self.initFromJson(jsonR)

    def initFromJson(self, res:dict):
        self.table = str(res["table"])
        for r in res["rules"]:
            if r["type"] == RuleType.RULE_TYPE_SINGLE_FIELD:
                self.rules.append(RuleSingleField(self, args=r))
            elif r["type"] == RuleType.RULE_TYPE_IFTTT:
                self.rules.append(RuleIFTTT(self, args=r))
            elif r["type"] == RuleType.RULE_TYPE_CALCULATION:
                self.rules.append(RuleCalc(self, args=r))

    def initFields(self, cursor:pymysql.cursors.Cursor)->bool:
        sql = "DESCRIBE {table}".format(table=self.table)

        cursor.execute(sql)
        self.fields = []
    
        res = cursor.fetchall()
        for r in res:
            self.fields.append(r[0])

        
    def getFieldIndex(self, field:str)->int:
        return self.fields.index(field)

    def isValid(self)->bool:
        return len(self.rules) > 0


    def getErrorStr(self, err:TableCheckError):
        if err == TableCheckError.TABLE_CHECK_OK:
            return "表【{table}】校验通过。\n".format(table=self.table)
        elif err == TableCheckError.TABLE_CHECK_NO_DATA_OR_ERROR:
            return "表【{table}】不存在或者无数据。\n".format(table=self.table)
        elif err == TableCheckError.TABLE_CHECK_FAILED:
            return "表【{table}】校验失败。\n".format(table=self.table)

    def checkTable(self, cursor:pymysql.cursors.Cursor)->str:
        txt = "开始校验表【{t}】：\n".format(t=self.table)
        
        try:
            self.initFields(cursor)
            
        
            sql = "SELECT * FROM {table}".format(table=self.table)
            cursor.execute(sql)
        except:
            txt += self.getErrorStr(TableCheckError.TABLE_CHECK_NO_DATA_OR_ERROR)
            return txt

        res = cursor.fetchall()
        if res is None or len(res) <= 0:
            txt += self.getErrorStr(TableCheckError.TABLE_CHECK_NO_DATA_OR_ERROR)
            return txt
           

        result = []
        for row in res:
            for rule in self.rules:
                result += rule.run(row, cursor)

        for r in result:
            txt += r + "\n"

        if len(result) > 0:
            txt += self.getErrorStr(TableCheckError.TABLE_CHECK_FAILED)
        else:
            txt += self.getErrorStr(TableCheckError.TABLE_CHECK_OK)

        return txt

    def toJson(self)->dict:
        rList = []
        for r in self.rules:
            if r.isValid():
                rList.append(r.toJson())

        res = {"table": self.table, "rules": rList}

        return res
    
'''
"tables":[
    {"table": "cq_xxx", 
        "rules": [
            {"type":1, "field": "id", constraints:[...]
            },
            {"type":2, "field1": "id", constraints1:[...], "field2": "data", constraints2:[...]},
            {"type":3, "field1": "id", "field2": "data", expr:"{f}/100"}
            ...
        ]
    },
    ...
]
'''

class RuleSingleField(Rule):
    def __init__(self, table:DbTable, field:str = None, args:dict = None) -> None:
        self.type = RuleType.RULE_TYPE_SINGLE_FIELD
        self.table = table
        self.field = field
        self.constraints = []


        if args is not None:
            self.initFromJson(args)

    def initFromJson(self, args:dict)->None:
        DEBUG_INFO(args)
        self.type = RuleType(args["type"])
        self.field = str(args["field"])
        
        for c in args["constraints"]:
            self.constraints.append(Constraint.createNewConstrainst(c))


    def getErrorStr(self, err:Constraint.ConstraintError)->str:
        c = Constraint()
        return "字段({f})校验失败：{e})\n".format(f = self.field, e = c.getErrorString(err))

    def run(self, row, cursor:pymysql.cursors.Cursor)->list:
        idx = self.table.getFieldIndex(self.field)

        result = []
        for constraint in self.constraints:
            err = constraint.verify(row[idx], cursor)
            if err != Constraint.ConstraintError.CONSTRAINT_ERROR_OK:
               result.append(self.getErrorStr(err))

        return result

    def getDesc(self)->str:
        desc = ""
        for c in self.constraints:
            desc += c.getDescString() + c.getContentString()

        return desc

    def getField(self)->str:
        return self.field

    def isValid(self) -> bool:
        return len(self.constraints) > 0

    def toJson(self) -> dict:
        cList = []
        for c in self.constraints:
            if c.isValid():
                cList.append(c.toJson()) 
        res = { "type": int(self.type), "field": self.field, "constraints": cList }

        return res

class RuleIFTTT(Rule):
    def __init__(self, table:DbTable, field1:str = None, field2:str = None, args:dict = None) -> None:
        self.type = RuleType.RULE_TYPE_IFTTT
        self.table = table
        self.field1 = field1
        self.field2 = field2
        self.constraints1 = []
        self.constraints2 = []

    def initFromJson(self, args:dict)->None:
        DEBUG_INFO(args)
        self.type = RuleType(args["type"])
        self.field1 = str(args["field1"])
        self.field2 = str(args["field2"])
        
        for c in args["constraints1"]:
            self.constraints1.append(Constraint.createNewConstrainst(c))

        for c in args["constraints2"]:
            self.constraints2.append(Constraint.createNewConstrainst(c))

    def run(self, row, cursor:pymysql.cursors.Cursor) -> list:
        idx1 = self.table.getFieldIndex(self.field1)
        idx2 = self.table.getFieldIndex(self.field2)

        result = []
        for constraint1 in self.constraints1:
            err1 = constraint1.verify(row[idx1], cursor)
            if err1 == Constraint.ConstraintError.CONSTRAINT_ERROR_OK:
               for constraint2 in self.constraints2:
                   err2 = constraint2.verify(row[idx2], cursor)
                   if err2 != Constraint.ConstraintError.CONSTRAINT_ERROR_OK:
                       result.append(self.getErrorStr(err2, constraint1, constraint2))

        return result

    def getField(self)->str:
        return self.field1

    def getErrorStr(self, err: Constraint.ConstraintError, c1:Constraint.Constraint, c2:Constraint.Constraint):
        text = "字段{f1}，{f2}校验失败：当字段{f1}满足以下条件时：{t1}{ctx1}\n字段{f2}不满足以下条件：{t2}{ctx2}\n".format(f1=self.field1, f2=self.field2, t1=c1.getDescString(), ctx1=c1.getContentString(), t2=c2.getDescString(), ctx2=c2.getContentString())

    def getDesc(self) -> str:
        desc = ""
        if len(self.constraints1) > 0 and len(self.constraints2) > 0:
            c1 = self.constraints1[0]
            c2 = self.constraints2[0]
            text = "当字段{f1}满足以下条件时：{t1}{ctx1}\n字段{f2}需满足以下条件：{t2}{ctx2}\n".format(f1=self.field1, f2=self.field2, t1=c1.getDescString(), ctx1=c1.getContentString(), t2=c2.getDescString(), ctx2=c2.getContentString())
        desc += text

        return desc

    def isValid(self) -> bool:
        return len(self.constraints1) > 0 and len(self.constraints2) > 0

    def toJson(self) -> dict:
        c_list1 = []
        c_list2 = []
        for c1 in self.constraints1:
            if c1.isValid():
                c_list1.append(c1.toJson())

        for c2 in self.constraints2:
            if c2.isValid():
                c_list2.append(c2.toJson())

        res = {"type":int(self.type), "field1": self.field1, "constraints1": c_list1, "field2":self.field2, "constraints2": c_list2 }

        return res

class RuleCalc(Rule):
    def __init__(self, table:DbTable, field1:str = None, field2:str = None, args:dict = None) -> None:
        self.type = RuleType.RULE_TYPE_CALCULATION
        self.table = table
        self.field1 = field1
        self.field2 = field2
        self.expr = ""

    def getErrorStr(self)->str:
        expr1 = self.expr.format(f=self.field1)
        return "字段({f1},{f2})校验失败：{expr}!={f2}\n".format(f1 = self.field1, expr = expr1, f2 = self.field2)

    def initFromJson(self, args:dict):
        DEBUG_INFO(args)
        self.type = RuleType(args["type"])
        self.field1 = str(args["field1"])
        self.field2 = str(args["field2"])
        
        self.expr = str(args["expr"])

    def run(self, row, cursor:pymysql.cursors.Cursor)->list:
        idx1 = self.table.getFieldIndex(self.field1)
        idx2 = self.table.getFieldIndex(self.field2)

        result = []
        v1 = eval(self.expr.format(f=row[idx1]))
        v2 = row[idx2]

        if v1 != v2:
            result.append(self.getErrorStr())

        return result

    def getField(self)->str:
        return self.field1

    def getDesc(self) -> str:
        expr1 = self.expr.format(f=self.field1)
        return "字段({f1},{f2})需满足条件：{expr}=={f2}\n".format(f1 = self.field1, expr = expr1, f2 = self.field2)

    def isValid(self) -> bool:
        return len(self.expr) > 0

    def toJson(self) -> dict:
        res = {"type":int(self.type), "field1": self.field1, "field2": self.field2, "expr": self.expr}

        return res