# -*- coding: utf-8 -*-
import sys
sys.path = ['../']+sys.path



from PyQt4 import QtCore,QtGui
from neurolabscope.configure import ConfigWindow

def test1():
    app = QtGui.QApplication([])
    w = ConfigWindow()
    w.show()
    
    app.exec_()












if __name__ == '__main__':
    test1()