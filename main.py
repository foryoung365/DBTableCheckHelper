# -*- coding: utf-8 -*-

import sys
from TblCfgHelper import TableCfgHelper

if __name__ == '__main__':
    cfg = TableCfgHelper()

    sys.exit(cfg.app.exec_())