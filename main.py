# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QMessageBox
from TblCfgHelper import TableCfgHelper

if __name__ == '__main__':
    cfg = TableCfgHelper()

    sys.exit(cfg.app.exec_())
