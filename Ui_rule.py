# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\Projects\PythonProjects\TblCfgHelper\rule.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(1041, 770)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setModal(True)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 241, 721))
        self.groupBox.setObjectName("groupBox")
        self.listView = QtWidgets.QListView(self.groupBox)
        self.listView.setGeometry(QtCore.QRect(10, 50, 221, 661))
        self.listView.setObjectName("listView")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(140, 20, 41, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_10 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_10.setGeometry(QtCore.QRect(190, 20, 41, 23))
        self.pushButton_10.setObjectName("pushButton_10")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(280, 20, 751, 291))
        self.groupBox_2.setObjectName("groupBox_2")
        self.treeView = QtWidgets.QTreeView(self.groupBox_2)
        self.treeView.setGeometry(QtCore.QRect(10, 20, 731, 231))
        self.treeView.setObjectName("treeView")
        self.pushButton_11 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_11.setGeometry(QtCore.QRect(670, 260, 71, 23))
        self.pushButton_11.setObjectName("pushButton_11")
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(280, 310, 751, 421))
        self.groupBox_3.setObjectName("groupBox_3")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_3)
        self.tabWidget.setGeometry(QtCore.QRect(10, 20, 731, 391))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(80, 19, 601, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 80, 321, 281))
        self.groupBox_4.setObjectName("groupBox_4")
        self.listView_2 = QtWidgets.QListView(self.groupBox_4)
        self.listView_2.setGeometry(QtCore.QRect(10, 20, 301, 251))
        self.listView_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView_2.setObjectName("listView_2")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_5.setGeometry(QtCore.QRect(350, 80, 361, 281))
        self.groupBox_5.setObjectName("groupBox_5")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 20, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 70, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.listView_4 = QtWidgets.QListView(self.tab_2)
        self.listView_4.setGeometry(QtCore.QRect(20, 260, 561, 101))
        self.listView_4.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView_4.setObjectName("listView_4")
        self.listView_3 = QtWidgets.QListView(self.tab_2)
        self.listView_3.setGeometry(QtCore.QRect(20, 120, 561, 101))
        self.listView_3.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView_3.setObjectName("listView_3")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_7.setGeometry(QtCore.QRect(620, 270, 75, 23))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_8.setGeometry(QtCore.QRect(620, 330, 75, 23))
        self.pushButton_8.setObjectName("pushButton_8")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(20, 240, 131, 16))
        self.label_5.setObjectName("label_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_6.setGeometry(QtCore.QRect(620, 190, 75, 23))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_5.setGeometry(QtCore.QRect(620, 130, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(20, 90, 141, 31))
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 71, 21))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(20, 60, 54, 12))
        self.label_4.setObjectName("label_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 20, 621, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(70, 60, 621, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_6 = QtWidgets.QLabel(self.tab_3)
        self.label_6.setGeometry(QtCore.QRect(10, 20, 71, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_4.setGeometry(QtCore.QRect(80, 20, 621, 31))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_7 = QtWidgets.QLabel(self.tab_3)
        self.label_7.setGeometry(QtCore.QRect(10, 70, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_5.setGeometry(QtCore.QRect(80, 70, 621, 31))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_8 = QtWidgets.QLabel(self.tab_3)
        self.label_8.setGeometry(QtCore.QRect(10, 110, 81, 41))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_6.setGeometry(QtCore.QRect(80, 120, 621, 31))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setGeometry(QtCore.QRect(10, 160, 691, 16))
        self.label_9.setObjectName("label_9")
        self.textEdit = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit.setGeometry(QtCore.QRect(10, 220, 691, 111))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(14)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.label_10 = QtWidgets.QLabel(self.tab_3)
        self.label_10.setGeometry(QtCore.QRect(10, 190, 71, 21))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.tabWidget.addTab(self.tab_3, "")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(950, 740, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_9 = QtWidgets.QPushButton(Dialog)
        self.pushButton_9.setGeometry(QtCore.QRect(870, 740, 75, 23))
        self.pushButton_9.setObjectName("pushButton_9")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "新增规则"))
        self.groupBox.setTitle(_translate("Dialog", "选择数据表"))
        self.pushButton.setText(_translate("Dialog", "新增"))
        self.pushButton_10.setText(_translate("Dialog", "删除"))
        self.groupBox_2.setTitle(_translate("Dialog", "已有规则"))
        self.pushButton_11.setText(_translate("Dialog", "删除"))
        self.groupBox_3.setTitle(_translate("Dialog", "新增规则"))
        self.label.setText(_translate("Dialog", "字段："))
        self.groupBox_4.setTitle(_translate("Dialog", "当前约束"))
        self.groupBox_5.setTitle(_translate("Dialog", "新增约束"))
        self.pushButton_2.setText(_translate("Dialog", "新增"))
        self.pushButton_3.setText(_translate("Dialog", "删除"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Single"))
        self.pushButton_7.setText(_translate("Dialog", "新增"))
        self.pushButton_8.setText(_translate("Dialog", "删除"))
        self.label_5.setText(_translate("Dialog", "字段2需满足以下条件："))
        self.pushButton_6.setText(_translate("Dialog", "删除"))
        self.pushButton_5.setText(_translate("Dialog", "新增"))
        self.label_3.setText(_translate("Dialog", "当字段1满足以下条件时："))
        self.label_2.setText(_translate("Dialog", "字段1："))
        self.label_4.setText(_translate("Dialog", "字段2："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "IFTTT"))
        self.label_6.setText(_translate("Dialog", "字段1："))
        self.label_7.setText(_translate("Dialog", "字段2："))
        self.label_8.setText(_translate("Dialog", "表达式："))
        self.label_9.setText(_translate("Dialog", "说明：输入从字段1计算出字段2的表达式（支持基础数学运算），字段1使用{f}代替。如字段2=字段1/100，则只需填入：{f}/100"))
        self.label_10.setText(_translate("Dialog", "预览："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Calc"))
        self.pushButton_4.setText(_translate("Dialog", "完成"))
        self.pushButton_9.setText(_translate("Dialog", "添加"))
