# -*- coding: utf-8 -*-
import sys
sys.path = ['../']+sys.path



from PyQt4 import QtCore,QtGui
from neurolabscope.annotationstool import AnnotationsWidget,  _default_param_annotations



def test1():
    app = QtGui.QApplication([])
    w = AnnotationsWidget()
    w.show()
    
    w.set_annotations({'new_field' : 'yep1'})
    
    w.set_annotations({'new_field' : 'yep2'})
    
    app.exec_()
    print w.get_annotations()
    print w.get_param_annotations()

    

    



if __name__ == '__main__':
    test1()
