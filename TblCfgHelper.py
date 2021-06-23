# -*- coding: utf-8 -*-
import sys
import Ui_main
import Ui_project
import Ui_checkconfig

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QWidget
from ProjectSelector import ProjectSelector

class TableCfgHelper:
    app = QApplication(sys.argv)
    ps = ProjectSelector()
    mw = QMainWindow()
    pw = Ui_project.Ui_Dialog()
    d = QDialog()

    def __init__(self) -> None:
        self.showMainWindow()
        self.showSelectProjectDialog()
    

    def showMainWindow(self):

        ui = Ui_main.Ui_MainWindow()
        ui.setupUi(self.mw)
        
        self.mw.setWindowTitle("服务端配置检查工具")
        self.mw.resize(self.app.desktop().width(), self.app.desktop().height())
        self.mw.showMaximized()


    def showSelectProjectDialog(self):
        self.d.setParent(self.mw)
        self.pw.setupUi(self.d)
        self.pw.comboBox.addItems(self.ps.getProjectNameList())
        self.pw.buttonBox.accepted.connect(self.onSelectProjectAccepted)
        self.pw.buttonBox.rejected.connect(self.onSelectProjectRejected)
        self.d.setModal(True)
        self.d.show()

    def onSelectProjectAccepted(self):
        self.ps.setSelectedProject(self.pw.comboBox.currentText())
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

    def onImportButtonClicked(self):
        pass

    def onCreateButtonClicked(self):
        pass
