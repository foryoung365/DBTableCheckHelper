# -*- coding: utf-8 -*-
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import DbMgr
import sys
import Ui_main
import Ui_project
import Ui_checkconfig
import os
import shutil
import json
import Rules

from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QMainWindow, QMessageBox, QStatusBar, QFileDialog, QStyleFactory, QTextBrowser, QTextEdit, QTreeView, QWidget
from ProjectSelector import ProjectSelector

class TableCfgHelper:
    app = QApplication(sys.argv)
    ps = ProjectSelector()
    mw = QMainWindow()
    pw = Ui_project.Ui_Dialog()
    dbm = DbMgr.DbMgr(DbMgr.DB_CONFIG)
    mwui = Ui_main.Ui_MainWindow()

    def __init__(self) -> None:
        self.showMainWindow()
        self.showSelectProjectDialog()
    

    def showMainWindow(self):
        self.mwui.setupUi(self.mw)

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
        self.mwui.ll.addWidget(self.mwui.dblabel, 0, 0, 1, 12)
        self.mwui.ll.addWidget(self.mwui.dbtree, 1, 0, 47, 12)

        self.mwui.rulelabel = QLabel("规则", self.mwui.rw)
        self.mwui.ruletree = QTreeView(self.mwui.rw)
        self.mwui.rl.addWidget(self.mwui.rulelabel, 0, 0, 1, 36)
        self.mwui.rl.addWidget(self.mwui.ruletree, 1, 0, 35, 36)
        
        self.mwui.outputlabel = QLabel("输出", self.mwui.rw)
        self.mwui.outputtext = QTextEdit(self.mwui.rw)
        self.mwui.outputtext.setReadOnly(True)
        self.mwui.rl.addWidget(self.mwui.outputlabel, 36, 0, 1, 36)
        self.mwui.rl.addWidget(self.mwui.outputtext, 37, 0, 11, 36)

        self.mwui.statusbar = QStatusBar()
        self.mw.setStatusBar(self.mwui.statusbar)
        self.mwui.statuslabel = QLabel("当前项目：未选择")
        self.mwui.statusbar.addWidget(self.mwui.statuslabel)
        self.mw.setWindowTitle("服务端配置检查工具")
        #self.mw.resize(self.app.desktop().width(), self.app.desktop().height())
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.mw.show()

    def ShowDbTree(self):
        model = QStandardItemModel(self.mw)
        model.setHorizontalHeaderLabels(["Host"])

        dblist = self.dbm.getConfigList()
        if len(dblist) > 0:
            for l in dblist:
                itemhost = QStandardItem(l)
                model.appendRow(itemhost)
        else:
            itemhost = QStandardItem("未配置连接")
            model.appendRow(itemhost)

        treeview = self.mwui.treeView
        treeview.setModel(model)
        treeview.expandAll()

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
            ccd = QDialog()
            ccw = Ui_checkconfig.Ui_Dialog()
            ccw.setupUi(ccd)
            hint = ccw.label.text().format(project=self.ps.getSelectedProjectName(), file=filename)
            ccw.label.setText(hint)
            ccw.createButton.clicked.connect(self.onCreateButtonClicked)
            ccw.importButton.clicked.connect(self.onImportButtonClicked)
            ccd.setParent(self.mw)
            ccd.setModal(True)
            ccd.show()
        else:
            self.parseProjectConfig()

    def askImportFile(self, title:str, filetype:str):
        fileName,fileExt = QFileDialog.getOpenFileName(self.mw, title, os.getcwd(), filetype)
        return fileName, fileExt

    def parseProjectConfig(self):
        with open(self.ps.getConfigFileName(), 'r', encoding="utf-8") as cfg:
            self.tableRules = []
            #try:
            res = json.load(cfg)["tables"]
            for r in res:
                try:
                    self.tableRules.append(Rules.DbTable(jsonR=r))
                except:
                    QMessageBox.information(self.mw, '提示',
                    "配置文件{file}解析失败，请检查文件是否正确。".format(self.ps.getConfigFileName()))
                    return
            QMessageBox.information(self.mw, '提示',
            "成功加载{num}条规则。".format(num=len(self.tableRules)))
                
            #except:
            #    reply = QMessageBox.question(self.mw, '提示',
            #    "当前项目还未配置规则，是否现在新增规则?", QMessageBox.Yes | 
            #    QMessageBox.No, QMessageBox.No)
            #    if reply == QMessageBox.Yes:
            #        pass
            #    else:
            #        pass

    def onImportButtonClicked(self):
        name,ext = self.askImportFile("选择导入文件", "Json Files(*.json);;All Files(*);")

        if os.path.exists(name):
            shutil.copyfile(name, os.getcwd() +"\\" + self.ps.getConfigFileName())
        
        self.checkProjectConfig()
        

    def onCreateButtonClicked(self):
        pass
