# -*- coding: utf-8 -*-
import sys
sys.path = ['../']+sys.path



from PyQt4 import QtCore,QtGui
import datetime
from neurolabscope.recordinglist import RecordingList



def test1():
    app = QtGui.QApplication([])
    w = RecordingList()
    w.add_rec('yep', 'yep', datetime.datetime.now(), state = 'finished')
    w.add_rec('yep', 'yep', datetime.datetime.now())
    w.show()
    
    app.exec_()


if __name__ == '__main__':
    test1()


