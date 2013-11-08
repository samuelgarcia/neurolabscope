#!python
# -*- coding: utf-8 -*-

import sys
import os.path
from PyQt4.QtGui import QApplication
from neurolabscope.mainwindow import MainWindow

#~ from neurolabscope.default_setup import default_setup
import json

if __name__== '__main__':
    if len(sys.argv)==1:
        setup = None
    else:
        filename = sys.argv[1]
        setup = json.load(open(filename))

    app = QApplication(sys.argv)
    w = MainWindow(setup = setup)
    w.show()
    sys.exit(app.exec_())

