# -*- coding: utf-8 -*-
import sys
sys.path = ['../']+sys.path



from PyQt4 import QtCore,QtGui
import datetime
from neurolabscope.recordingtools import ConfigRecOnTrig



def test1():
    app = QtGui.QApplication([])
    w = ConfigRecOnTrig()
    w.show()
    
    app.exec_()


if __name__ == '__main__':
    test1()


