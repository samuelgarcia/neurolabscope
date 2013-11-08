# -*- coding: utf-8 -*-
import sys
sys.path = ['../']+sys.path



from PyQt4 import QtCore,QtGui
from neurolabscope.configure import ConfigWindow, ConfigDeviceWidget

from neurolabscope.default_setup import default_setup

def test1():
    app = QtGui.QApplication([])
    w = ConfigWindow()
    w.show()
    
    app.exec_()
    print w.get_setup()


def test2():
    app = QtGui.QApplication([])
    d = ConfigDeviceWidget( params = default_setup['devices'][0])
    if d.exec_():
        print d.get()
    



if __name__ == '__main__':
    test1()
    #~ test2()
