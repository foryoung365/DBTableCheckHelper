from PyQt5.QtWidgets import QDialog
import Ui_rule

class RuleDialog(QDialog):
    def __init__(self, helper) -> None:
        super().__init__()
        self.helper = helper

    def closeEvent(self, event):
        self.helper.showRuleTree()
        self.helper.saveCfg()
        event.accept()
