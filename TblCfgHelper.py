# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QStandardItemModel, QStandardItem
import DbMgr
import sys
import Ui_main
import Ui_project
import Ui_checkconfig
import os
import shutil
import json
import Rules

from PyQt5.QtWidgets import QAction, QApplication, QDialog, QGridLayout, QLabel, QMainWindow, QMessageBox, QStatusBar, QFileDialog, QStyleFactory,  QTextEdit, QTreeView, QWidget
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
        self.mwui.statuslabel = QLabel("当前项目：未选择")
        self.mwui.statusbar.addWidget(self.mwui.statuslabel)

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

    def onMenuBar(self, q):
        if q.text() == "执行检查":
            self.onRunCheck()
        elif q.text() == "关于":
            self.onAbout()
        elif q.text() == "退出":
            exit(0)
        elif q.text() == "选择项目":
            self.onReselectProject()
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
                self.dbm.Connect()
                self.ShowDbTree()
            else:
                self.dbm.setSelectedDb(item.text())
                self.mwui.statuslabel.setText("当前项目：" + self.ps.getSelectedProjectName() + "\t当前数据库：" + self.dbm.getSelectedDb())


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
        self.mwui.statuslabel.setText("当前项目："+self.ps.getSelectedProjectName())
        self.d.hide()
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

    def parseProjectConfig(self):
        try:
            with open(self.ps.getConfigFileName(), 'r', encoding="utf-8") as cfg:
                self.tableRules = []
                try:
                    res = json.load(cfg)["tables"]
                    for r in res:

                        self.tableRules.append(Rules.DbTable(jsonR=r))

                    QMessageBox.information(self.mw, '提示',
                    "成功加载{num}条规则。".format(num=len(self.tableRules)))
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
                pass
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
