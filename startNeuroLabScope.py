#!python
# -*- coding: utf-8 -*-

import sys
import os.path
from PyQt4.QtGui import QApplication
from neurolabscope.mainwindow import MainWindow



app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())

