# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\Projects\PythonProjects\TblCfgHelper\checkconfig.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 240)
        self.importButton = QtWidgets.QPushButton(Dialog)
        self.importButton.setGeometry(QtCore.QRect(40, 180, 75, 23))
        self.importButton.setObjectName("importButton")
        self.createButton = QtWidgets.QPushButton(Dialog)
        self.createButton.setGeometry(QtCore.QRect(200, 180, 75, 23))
        self.createButton.setObjectName("createButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 10, 311, 141))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "配置"))
        self.importButton.setText(_translate("Dialog", "导入"))
        self.createButton.setText(_translate("Dialog", "新建"))
        self.label.setText(_translate("Dialog", "未找到项目【{project}】的配置文件【{file}】，如已有配置，请导入配置文件，或者新建配置文件。"))
