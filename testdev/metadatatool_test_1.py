# -*- coding: utf-8 -*-
import sys
sys.path = ['../']+sys.path



from PyQt4 import QtCore,QtGui
from neurolabscope.metadatatool import MetadataWidget,  _default_param_metadata



def test1():
    app = QtGui.QApplication([])
    w = MetadataWidget()
    w.show()
    
    app.exec_()
    print w.get_metadata()
    print w.get_param_metadata()

    
#~ def test2():
    #~ app = QtGui.QApplication([])
    #~ d = ConfigureMetadataWidget( param_metadata = _default_param_metadata)
    #~ if d.exec_():
        #~ print d.get()
    



if __name__ == '__main__':
    test1()
    #~ test2()
