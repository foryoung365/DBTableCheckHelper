# -*- coding: utf-8 -*-

import sys

import TblCfgHelper

if __name__ == '__main__':
    cfg = TblCfgHelper.TableCfgHelper()

    sys.exit(cfg.app.exec_())
