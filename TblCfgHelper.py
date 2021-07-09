# -*- coding: utf-8 -*-
from Constraint import ConstraintError, ConstraintTableReference, ConstraintValueRange
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QIntValidator, QRegExpValidator, QStandardItemModel, QStandardItem
import DbMgr
import sys
import Ui_main
import Ui_project
import Ui_checkconfig
import Ui_rule
import os
import shutil
import json
import Rules
import Ui_constraint
import MyRuleDialog
import Ui_database

from PyQt5.QtWidgets import QAction, QApplication, QDialog, QGridLayout, QLabel, QMainWindow, QMessageBox, QStatusBar, QFileDialog, QStyleFactory,  QTextEdit, QTreeView, QWidget, QInputDialog
from ProjectSelector import ProjectSelector

class TableCfgHelper:
    app = QApplication(sys.argv)
    ps = ProjectSelector()
    mw = QMainWindow()
    pw = Ui_project.Ui_Dialog()
    dbm = DbMgr.DbMgr(DbMgr.DB_CONFIG)
    mwui = Ui_main.Ui_MainWindow()
    tableRules = None
    colors = [QColor.fromRgb(0xFFEB3B), QColor.fromRgb(0xF0F4B3), QColor.fromRgb(0xCDDC39)]

    def __init__(self) -> None:
        self.showMainWindow()
        self.showSelectProjectDialog()

    def reset(self):
        self.ps = ProjectSelector()
        self.dbm = DbMgr.DbMgr(DbMgr.DB_CONFIG)
        self.tableRules = []
    

    def showMainWindow(self):
        self.mwui.setupUi(self.mw)

        #菜单栏
        self.mwui.menu.triggered[QAction].connect(self.onMenuBar)
        self.mwui.menu_2.triggered[QAction].connect(self.onMenuBar)
        self.mwui.menu_3.triggered[QAction].connect(self.onMenuBar)

        #创建左侧部件
        self.mwui.lw = QWidget()
        self.mwui.ll = QGridLayout()
        self.mwui.lw.setLayout(self.mwui.ll)

        #创建右侧部件
        self.mwui.rw = QWidget()
        self.mwui.rl = QGridLayout()
        self.mwui.rw.setLayout(self.mwui.rl)
        
        self.mwui.gridLayout.addWidget(self.mwui.lw, 0, 0, 48, 12)
        self.mwui.gridLayout.addWidget(self.mwui.rw, 0, 12, 48, 36)

        self.mwui.dblabel = QLabel("数据库连接", self.mwui.lw)
        self.mwui.dbtree = QTreeView(self.mwui.lw)

        self.ShowDbTree()

        self.mwui.ll.addWidget(self.mwui.dblabel, 0, 0, 1, 12)
        self.mwui.ll.addWidget(self.mwui.dbtree, 1, 0, 47, 12)

        self.mwui.rulelabel = QLabel("规则", self.mwui.rw)
        self.mwui.ruletree = QTreeView(self.mwui.rw)
        self.mwui.rl.addWidget(self.mwui.rulelabel, 0, 0, 1, 36)
        self.mwui.rl.addWidget(self.mwui.ruletree, 1, 0, 35, 36)

        self.showRuleTree()
        
        self.mwui.outputlabel = QLabel("输出", self.mwui.rw)
        self.mwui.outputtext = QTextEdit(self.mwui.rw)
        self.mwui.outputtext.setReadOnly(True)
        self.mwui.rl.addWidget(self.mwui.outputlabel, 36, 0, 1, 36)
        self.mwui.rl.addWidget(self.mwui.outputtext, 37, 0, 11, 36)

        #状态栏
        self.mwui.statusbar = QStatusBar()
        self.mw.setStatusBar(self.mwui.statusbar)
        self.mwui.statuslabel = QLabel()
        self.mwui.statusbar.addWidget(self.mwui.statuslabel)
        self.setStatusLabel()

        #显示主窗口
        self.mw.setWindowTitle("服务端配置检查工具")
        #self.mw.resize(self.app.desktop().width(), self.app.desktop().height())
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.mw.show()

    def showRuleTree(self):
        model = QStandardItemModel(self.mw)
        model.setHorizontalHeaderLabels(["数据表","字段", "规则"])
        emptyitem = QStandardItem()
        emptyitem.setEditable(False)

        if self.tableRules is not None and len(self.tableRules) > 0:
            for table in self.tableRules:
                itemtable = QStandardItem(table.table)
                itemtable.setData("table", QtCore.Qt.UserRole)
                itemtable.setEditable(False)
                itemtable.setBackground(self.colors[0])
                emptyitem.setBackground(self.colors[0])
                model.appendRow([itemtable, QStandardItem(emptyitem), QStandardItem(emptyitem)])

                i = 0
                for r in table.rules:
                    if r is not None:
                        f = QStandardItem(r.getField())
                        f.setEditable(False)
                        f.setData("field", QtCore.Qt.UserRole)
                        desc = QStandardItem(r.getDesc())
                        desc.setEditable(False)
                        desc.setData("desc", QtCore.Qt.UserRole)

                        colorIdx = 1+i % 2;

                        f.setBackground(self.colors[colorIdx])
                        desc.setBackground(self.colors[colorIdx])
                        emptyitem.setBackground(self.colors[colorIdx])
                    
                        itemrule = [QStandardItem(emptyitem), f, desc]
                        itemtable.appendRow(itemrule)
                        i += 1
                        
        else:
            itemrule = QStandardItem("未配置规则，请先创建规则。")
            itemrule.setData("fail", QtCore.Qt.UserRole)
            itemrule.setEditable(False)
            model.appendRow(itemrule)

        treeview = self.mwui.ruletree
        treeview.doubleClicked.connect(self.onRuleTreeItemDoubleClicked)
        treeview.setSelectionBehavior(QTreeView.SelectRows)
        treeview.setIndentation(0)
        treeview.setModel(model)
        treeview.expandAll()

    def setStatusLabel(self):
        pname = self.ps.getSelectedProjectName()
        dbname = self.dbm.getSelectedDb()
        if pname is None:
            pname = "未选择"
        if dbname is None:
            dbname = "未选择"

        txt = "当前项目：{p}\t当前数据库：{db}".format(p=pname, db=dbname)
        self.mwui.statuslabel.setText(txt)

    def onRuleTreeItemDoubleClicked(self, index):
        cat = index.data(QtCore.Qt.UserRole)
        if cat == "fail":
            return
        item = self.mwui.ruletree.model().itemFromIndex(index)
        if item is not None:
            if cat == "table":
                pass
            else:
                pass

    def showDatabaseDialog(self):
        self.dbd = QDialog()
        self.dbui = Ui_database.Ui_Dialog()
        self.dbui.setupUi(self.dbd)
        self.dbui.buttonBox.accepted.connect(self.onDatabaseAccepted)
        self.dbui.buttonBox.rejected.connect(self.onDatabaseRejected)

        regexp = QtCore.QRegExp("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))")
        v = QRegExpValidator(regexp)
        self.dbui.lineEdit.setValidator(v)
        self.dbd.setModal(True)

        self.dbd.show()

    def onDatabaseAccepted(self):
        if len(self.dbui.lineEdit.text()) > 0 and len(self.dbui.lineEdit_2.text()) > 0 and len(self.dbui.lineEdit_3.text()) > 0:
            cfg = {"host": self.dbui.lineEdit.text(), "user": self.dbui.lineEdit_2.text(), "password": self.dbui.lineEdit_3.text()}
            self.dbm.cfgs.append(cfg)
            self.dbm.saveFile()
            self.ShowDbTree()
            self.dbd.close()
        else:
            QMessageBox.information(self.dbd, "错误", "请填写连接IP、用户名和密码！")
            self.showDatabaseDialog()
            return

    def onDatabaseRejected(self):
        self.dbd.close()

    def onMenuBar(self, q):
        if q.text() == "执行检查":
            self.onRunCheck()
        elif q.text() == "关于":
            self.onAbout()
        elif q.text() == "退出":
            exit(0)
        elif q.text() == "选择项目":
            self.onReselectProject()
        elif q.text() == "编辑规则":
            self.showRuleDialog()
        elif q.text() == "新增数据库连接":
            self.showDatabaseDialog()
        else:
            pass

    def onReselectProject(self):
        self.reset()
        self.showSelectProjectDialog()
        self.showMainWindow()

    def onAbout(self):
        msgbox = QMessageBox()
        msgbox.setTextFormat(QtCore.Qt.RichText)
        msgbox.setWindowTitle("关于")
        msgbox.setText("数据库表配置检查工具<br>github地址: <a href='https://github.com/foryoung365/DBTableCheckHelper'>https://github.com/foryoung365/DBTableCheckHelper</a>")

        msgbox.exec()

    def onRunCheck(self):
        if self.dbm.getSelectedDb() is None:
            self.mwui.outputtext.setText("请先选择要检查的数据库！")
            return

        results = "====================开始检查=========================\n"
        for table in self.tableRules:
            if table is not None:
                res = table.checkTable(self.dbm.conn.cursor())
                if res is not None:
                    results += res
                    self.mwui.outputtext.setText(results)

        results += "====================检查完成=========================\n"
        self.mwui.outputtext.setText(results)


    def ShowDbTree(self):
        model = QStandardItemModel(self.mw)
        model.setHorizontalHeaderLabels(["Host"])

        dblist = self.dbm.getConfigList()
        selectedHost = self.dbm.getSelectedConfig()
        if len(dblist) > 0:
            for l in dblist:
                itemhost = QStandardItem(l["host"])
                itemhost.setEditable(False)
                itemhost.setData("host", QtCore.Qt.UserRole)
                model.appendRow(itemhost)
                if selectedHost == l:
                    dblist = self.dbm.getDbList()
                    if dblist is not None:
                        for db in dblist:
                            itemdb = QStandardItem(db)
                            itemdb.setData("db", QtCore.Qt.UserRole)
                            itemhost.appendRow(itemdb)
                            itemdb.setEditable(False)
                    else:
                        itemdb = QStandardItem("无法连接数据库！")
                        itemdb.setData("fail", QtCore.Qt.UserRole)
                
        else:
            itemhost = QStandardItem("未配置连接")
            itemhost.setData("fail", QtCore.Qt.UserRole)
            itemhost.setEditable(False)
            model.appendRow(itemhost)

        treeview = self.mwui.dbtree
        treeview.doubleClicked.connect(self.onDbTreeItemDoubleClicked)
        treeview.setModel(model)
        treeview.expandAll()

    def onDbTreeItemDoubleClicked(self, index):
        cat = index.data(QtCore.Qt.UserRole)
        if cat == "fail":
            return
        item = self.mwui.dbtree.model().itemFromIndex(index)
        if item is not None:
            if cat == "host":
                self.dbm.setSelectedHost(item.text())
                dbc = self.dbm.Connect()
                if dbc == None:
                    QMessageBox.information(self.mw, "错误", "连接数据库【{db}】失败！".format(db = self.dbm.selectedHost))
                self.ShowDbTree()
            else:
                self.dbm.setSelectedDb(item.text())
                self.setStatusLabel()


    def showSelectProjectDialog(self):
        self.d = QDialog()
        #self.d.setParent(self.mw)
        self.pw.setupUi(self.d)
        self.pw.comboBox.addItems(self.ps.getProjectNameList())
        self.pw.buttonBox.accepted.connect(self.onSelectProjectAccepted)
        self.pw.buttonBox.rejected.connect(self.onSelectProjectRejected)
        self.d.setModal(True)
        self.d.show()

    def onSelectProjectAccepted(self):
        self.ps.setSelectedProject(self.pw.comboBox.currentText())
        self.setStatusLabel()
        self.d.close()
        self.checkProjectConfig()

    def onSelectProjectRejected(self):
        if self.ps.getSelectedProject() is None:
            QMessageBox.question(self.d, "提示", "请选择一个项目以开始！", QMessageBox.Yes)
        self.d.show()
        

    def checkProjectConfig(self)->bool:     
        bExists = self.ps.isProjectConfigExists()
        if not bExists:
            filename = self.ps.getConfigFileName()
            self.ccd = QDialog()
            self.ccw = Ui_checkconfig.Ui_Dialog()
            self.ccw.setupUi(self.ccd)
            hint = self.ccw.label.text().format(project=self.ps.getSelectedProjectName(), file=filename)
            self.ccw.label.setText(hint)
            self.ccw.createButton.clicked.connect(self.onCreateButtonClicked)
            self.ccw.importButton.clicked.connect(self.onImportButtonClicked)
            self.ccd.setModal(True)
            self.ccd.show()
        else:
            self.parseProjectConfig()

    def askImportFile(self, title:str, filetype:str):
        fileName,fileExt = QFileDialog.getOpenFileName(self.mw, title, os.getcwd(), filetype)
        return fileName, fileExt

    def getRuleCount(self):
        count = 0
        for t in self.tableRules:
            count += len(t.rules)

        return count

    def parseProjectConfig(self):
        try:
            with open(self.ps.getConfigFileName(), 'r', encoding="utf-8") as cfg:
                self.tableRules = []
                try:
                    res = json.load(cfg)["tables"]
                    for r in res:

                        self.tableRules.append(Rules.DbTable(jsonR=r))

                    QMessageBox.information(self.mw, '提示',
                    "成功加载{num}条规则。".format(num=self.getRuleCount()))
                    self.showRuleTree()
                except:
                    QMessageBox.information(self.mw, '提示',
                            "配置文件【{file}】解析失败，请检查文件是否正确。".format(file=self.ps.getConfigFileName()))
                    return
        except:
            reply = QMessageBox.question(self.mw, '提示',
                    "当前项目还未配置规则，是否现在新增规则?", QMessageBox.Yes | 
                    QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.showRuleDialog()
            else:
                pass

    def onImportButtonClicked(self):
        name,ext = self.askImportFile("选择导入文件", "Json Files(*.json);;All Files(*);")

        if os.path.exists(name):
            shutil.copyfile(name, os.getcwd() +"\\" + self.ps.getConfigFileName())
        
        self.checkProjectConfig()
        

    def onCreateButtonClicked(self):
        with open(self.ps.getConfigFileName(), "w+"):
            self.checkProjectConfig()

    def onRuleTableDelButton(self):
        list = self.rui.listView.model().stringList()
        index = self.rui.listView.currentIndex()
        if index.row() == -1:
            QMessageBox.information(self.rd, "错误", "请先选择要删除的表！")
            return

        table = list[index.row()]
        if table is not None:
            for t in self.tableRules:
                if t.table == table:
                    self.tableRules.remove(t)
                    break
        self.showRuleTables()
        #self.showRuleTree()

    def onRuleDelButton(self):
        index = self.rui.treeView.currentIndex()
        if index.row() == -1:
            QMessageBox.information(self.rd, "错误", "请先选择要删除的规则！")
            return
        
        table = self.getNewRuleCurrentTable()
        del table.rules[index.row()]
        self.showTableRule(table.table)


    def showRuleDialog(self):
        self.rd = MyRuleDialog.RuleDialog(self)
        self.rui = Ui_rule.Ui_Dialog()
        self.rui.setupUi(self.rd)

        self.resetNewRule()
        
        self.showRuleTables()
        self.rui.listView.clicked.connect(self.onSelectRuleList)
        self.rui.pushButton.clicked.connect(self.onRuleAddTableButton)

        self.showNewRuleS()

        self.rui.pushButton_2.clicked.connect(self.onNewRuleSingleAddButton)
        self.rui.pushButton_3.clicked.connect(self.onNewRuleSingleDelButton)

        self.showNewRuleI()

        self.rui.pushButton_5.clicked.connect(self.onNewRuleIFTTTAdd1Button)
        self.rui.pushButton_6.clicked.connect(self.onNewRuleIFTTTDel1Button)
        self.rui.pushButton_7.clicked.connect(self.onNewRuleIFTTTAdd2Button)
        self.rui.pushButton_8.clicked.connect(self.onNewRuleIFTTTDel2Button)

        regexp = QtCore.QRegExp("[\w]+")
        v = QRegExpValidator(regexp)
        self.rui.lineEdit.setValidator(v)
        self.rui.lineEdit_2.setValidator(v)
        self.rui.lineEdit_3.setValidator(v)
        self.rui.lineEdit_4.setValidator(v)
        self.rui.lineEdit_5.setValidator(v)

        regexp2 = QtCore.QRegExp("[\w+\-*/%{}]+")
        v2 = QRegExpValidator(regexp2)
        self.rui.lineEdit_6.setValidator(v2)

        self.rui.pushButton_9.clicked.connect(self.onNewRuleAddButton)
        self.rui.pushButton_4.clicked.connect(self.onNewRuleDoneButton)

        self.rui.lineEdit_6.textChanged.connect(self.onNewRuleCalcExpChanged)


        self.rui.pushButton_10.clicked.connect(self.onRuleTableDelButton)
        self.rui.pushButton_11.clicked.connect(self.onRuleDelButton)

        self.rd.setFixedSize(self.rd.width(), self.rd.height())
        self.rd.setModal(True)
        self.rd.show()

    def onNewRuleAddButton(self):
        valid = False
        table = self.getNewRuleCurrentTable()
        
        if self.ruleS is not None and self.ruleS.isValid():
            table.rules.append(self.ruleS)
            valid = True

        if self.ruleC is not None and self.ruleC.isValid():
            table.rules.append(self.ruleC)
            valid = True

        if self.ruleI is not None and self.ruleI.isValid():
            table.rules.append(self.ruleI)
            valid = True

        if not valid:
            QMessageBox.information(self.rd, "错误", "新规则无效，请检查输入！")
            return

        self.resetNewRule()
        self.onSelectRuleList(self.rui.listView.currentIndex())
        self.showNewRule()
        #self.showRuleTree()

    def onNewRuleDoneButton(self):
        self.rd.close()
        #self.showRuleTree()

    def showNewRule(self):
        idx = self.rui.tabWidget.currentIndex()
        if idx == 0:
            self.showNewRuleS()
        elif idx == 1:
            self.showNewRuleI()
        else:
            self.showNewRuleC()

    def showNewRuleC(self):
        self.rui.lineEdit_4.setText("")
        self.rui.lineEdit_5.setText("")
        self.rui.lineEdit_6.setText("")

    def showNewRuleS(self):
        model = QtCore.QStringListModel()
        list = []
        if self.ruleS is not None and self.ruleS.isValid():
            for c in self.ruleS.constraints:
                list.append(c.getDescString() + c.getContentString())

        model.setStringList(list)
        self.rui.listView_2.setModel(model)

    def showNewRuleI(self):
        model = QtCore.QStringListModel()
        list = []
        if self.ruleI is not None:
            for c1 in self.ruleI.constraints1:
                list.append(c1.getDescString() + c1.getContentString())
        model.setStringList(list)
        self.rui.listView_3.setModel(model)

        model = QtCore.QStringListModel()
        list = []
        if self.ruleI is not None:
            for c2 in self.ruleI.constraints2:
                list.append(c2.getDescString() + c2.getContentString())
        model.setStringList(list)
        self.rui.listView_4.setModel(model)

    def onNewRuleIFTTTAdd1Button(self):
        if not self.checkNewRuleIFTTTField():
            return
        self.iftttIdx = 1
        self.showConstraintDialog(True)

    def onNewRuleIFTTTDel1Button(self):
        index = self.rui.listView_3.currentIndex()
        if index.row() == -1:
            QMessageBox.information(self.rd, "错误", "请先选择要删除的约束！")
        else:
            del self.ruleI.constraints1[index.row()]
            self.showNewRuleI()

    def onNewRuleIFTTTAdd2Button(self):
        if not self.checkNewRuleIFTTTField():
            return

        self.iftttIdx = 2
        self.showConstraintDialog(True)

    def onNewRuleIFTTTDel2Button(self):
        index = self.rui.listView_4.currentIndex()
        if index.row() == -1:
            QMessageBox.information(self.rd, "错误", "请先选择要删除的约束！")
        else:
            del self.ruleI.constraints2[index.row()]
            self.showNewRuleI()

    def onNewRuleCalcExpChanged(self):
        exp = self.rui.lineEdit_6.text()
        if len(exp) <= 0:
            return

        if not self.checkNewRuleCalcField():
            self.rui.lineEdit_6.setText("")
            return
        else:
            if exp.find("{f}") == -1:
                return
            exp = exp.format(f=self.rui.lineEdit_4.text())
            txt = "{f2}={exp}".format(f2=self.rui.lineEdit_5.text(), exp=exp)

            self.rui.textEdit.setText(txt)
            self.ruleC.expr = self.rui.lineEdit_4.text()

    def checkNewRuleIFTTTField(self)->bool:
        if (len(self.rui.lineEdit_2.text()) <= 0 or len(self.rui.lineEdit_3.text()) <= 0):
            QMessageBox.information(self.rd, "错误", "请先输入字段1和字段2！")
            return False
        else:
            if self.ruleI is None:
                self.ruleI = Rules.RuleIFTTT(self.getNewRuleCurrentTable(), self.rui.lineEdit_2.text(), self.rui.lineEdit_3.text())
            return True

    def checkNewRuleCalcField(self)->bool:
        if len(self.rui.lineEdit_4.text()) <= 0 or len(self.rui.lineEdit_5.text()) <= 0:
            QMessageBox.information(self.rd, "错误", "请先输入字段1和字段2！")
            return False
        else:
            if self.ruleC is None:
                self.ruleC = Rules.RuleCalc(self.getNewRuleCurrentTable(), self.rui.lineEdit_4.text(), self.rui.lineEdit_5.text())
            return True

    def onNewRuleSingleAddButton(self):
        if self.ruleS is None:
            field = self.rui.lineEdit.text()
            if len(field) <= 0:
                QMessageBox.information(self.rd, "错误", "请先输入字段名！")
                return
            else:
                self.ruleS = Rules.RuleSingleField(self.getNewRuleCurrentTable(), field)
            
        self.showConstraintDialog(True)

    def getNewRuleCurrentTable(self)->Rules.DbTable:
        index = self.rui.listView.currentIndex()
        return self.tableRules[index.row()]

    def addNewRuleConstraint(self):
        idx = self.rui.tabWidget.currentIndex()
        rule = None
        if idx == 0:
            self.addNewRuleCosntraintS()
        elif idx == 1:
            self.addNewRuleConstraintI()
        else:
           pass

    def addNewRuleCosntraintS(self):
        if self.rangeC.isValid():
            self.ruleS.constraints.append(self.rangeC)
        
        if self.refC.isValid():
            self.ruleS.constraints.append(self.refC)

    def addNewRuleConstraintI(self):
        if self.iftttIdx == 1:
            if self.rangeC.isValid():
                self.ruleI.constraints1.append(self.rangeC)
        
            if self.refC.isValid():
                self.ruleI.constraints1.append(self.refC)
        else:
            if self.rangeC.isValid():
                self.ruleI.constraints2.append(self.rangeC)
        
            if self.refC.isValid():
                self.ruleI.constraints2.append(self.refC)


    def onNewRuleSingleDelButton(self):
        index = self.rui.listView_2.currentIndex()
        if index.row() == -1:
            QMessageBox.information(self.rd, "错误", "请先选择要删除的约束！")
        else:
            del self.ruleS.constraints[index.row()]
            self.showNewRuleS()


    def showRuleTables(self):
        model = QtCore.QStringListModel()
        tablelist = []

        for r in self.tableRules:
            if r is not None:
                tablelist.append(r.table)

        model.setStringList(tablelist)

        self.rui.listView.setModel(model)

        self.onSelectRuleList(self.rui.listView.currentIndex())

    def onSelectRuleList(self, index):
        list = self.rui.listView.model().stringList()
        row = index.row()
        if row == -1 or row >= len(list):
            return

        table = list[row]
        if table is not None:
            self.showTableRule(table)


    def showTableRule(self, t:str):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["字段", "规则"])
        for table in self.tableRules:
            if table is not None and t == table.table:
                if len(table.rules) > 0:
                    i = 0
                    for r in table.rules:
                        coloridx = 1 + i % 2
                        f = QStandardItem(r.getField())
                        f.setEditable(False)
                        f.setBackground(self.colors[coloridx])
                        desc = QStandardItem(r.getDesc())
                        desc.setEditable(False)
                        desc.setBackground(self.colors[coloridx])
                        model.appendRow([f, desc])
                        i += 1
        self.rui.treeView.setIndentation(0)
        self.rui.treeView.setModel(model)
        self.rui.treeView.expandAll()

    def resetNewRule(self):
        self.ruleS = None
        self.ruleI = None
        self.ruleC = None
        self.rui.lineEdit.setText("")
        self.rui.lineEdit_2.setText("")
        self.rui.lineEdit_3.setText("")
        self.rui.lineEdit_4.setText("")
        self.rui.lineEdit_5.setText("")
        self.rui.lineEdit_6.setText("")
        self.rui.textEdit.setText("")
                        
    def onRuleAddTableButton(self):
        name,succ = QInputDialog.getText(self.rd, "新数据表", "请输入数据表名：")
        if not self.IsExistTable(name):
            self.tableRules.append(Rules.DbTable(name))

        idx = 0
        for table in self.tableRules:
            if name == table.table:
                self.showRuleTables()
                index = self.rui.listView.model().index(idx, 0)
                self.rui.listView.setCurrentIndex(index)
                self.onSelectRuleList(index)
                return
            idx += 1

    def IsExistTable(self, table:str)->bool:
        for t in self.tableRules:
            if table == t.table:
                return True
        
        return False

    def showConstraintDialog(self, reset:bool = False):
        if reset:
            self.cd = QDialog()
            self.cui = Ui_constraint.Ui_Form()
            self.cui.setupUi(self.cd)

            self.rangeC = ConstraintValueRange()
            self.refC = ConstraintTableReference()

        self.refreshConstraint()

        self.cui.lineEdit_3.setValidator(QIntValidator())
        self.cui.lineEdit_4.setValidator(QIntValidator())

        self.cui.pushButton.clicked.connect(self.onRangeConstraintClearButton)
        self.cui.pushButton_2.clicked.connect(self.onRangeConstraintAddButtion)
        self.cui.pushButton_3.clicked.connect(self.onRefConstraintClearButton)
        self.cui.pushButton_4.clicked.connect(self.onRefConstraintAddButton)

        self.cui.buttonBox.accepted.connect(self.onConstraintButtonBoxAccepted)
        self.cui.buttonBox.rejected.connect(self.onConstraintButtonBoxRejected)

        self.cd.setModal(True)
        self.cd.show()

    def onConstraintButtonBoxAccepted(self):
        self.cd.close()

        self.addNewRuleConstraint()
        self.showNewRule()

    def onConstraintButtonBoxRejected(self):
        self.rangeC = ConstraintValueRange()
        self.refC = ConstraintTableReference()
        self.cd.close()

    def refreshConstraint(self):
        if len(self.rangeC.ranges) > 0:
            txt = self.rangeC.getDescString()
            txt += self.rangeC.getContentString()
            self.cui.textEdit.setText(txt)
        else:
            self.cui.textEdit.setText("")

        if len(self.refC.refs) > 0:
            txt = self.refC.getDescString()
            txt += self.refC.getContentString()

            self.cui.textEdit_2.setText(txt)
        else:
            self.cui.textEdit_2.setText("")

    def onRangeConstraintClearButton(self):
        self.rangeC = ConstraintValueRange()
        self.refreshConstraint()

    def onRangeConstraintAddButtion(self):
        min = int(self.cui.lineEdit_3.text())
        max = int(self.cui.lineEdit_4.text())
        
        succ = self.rangeC.addRange(min, max)
        if succ != ConstraintError.CONSTRAINT_ERROR_OK:
            QMessageBox.information(self.cd, "错误", self.rangeC.getErrorString(succ))
        else:
            self.refreshConstraint()

    def onRefConstraintClearButton(self):
        self.refC = ConstraintTableReference()
        self.refreshConstraint()

    def onRefConstraintAddButton(self):
        t = self.cui.lineEdit_2.text()
        f = self.cui.lineEdit.text()
        succ = self.refC.addRef(t, f)
        if succ != ConstraintError.CONSTRAINT_ERROR_OK:
            QMessageBox.information(self.cd, "错误", self.refC.getErrorString(succ))
        else:
            self.refreshConstraint()

    def toJson(self)->dict:
        tList = []
        for t in self.tableRules:
            if t.isValid():
                tList.append(t.toJson())

        res = {"tables": tList}

        return res
    
    def saveCfg(self):
        res = self.toJson()
        with open(self.ps.getConfigFileName(), "w+") as cfg:
            json.dump(res, cfg)
 