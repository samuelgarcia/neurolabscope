# -*- coding: utf-8 -*-
import sys
sys.path = ['../']+sys.path



from PyQt4 import QtCore,QtGui
from neurolabscope.annotationstool import AnnotationsWidget,  _default_param_annotations




def test1():
    app = QtGui.QApplication([])
    
    w = QtGui.QWidget()
    h = QtGui.QHBoxLayout()
    w.setLayout(h)
    
    w1 = AnnotationsWidget()
    #~ w1.show()
    
    w1.set_annotations({'new_field' : 'yep1'})
    
    w1.set_annotations({'new_field' : 'yep2'})
    
    def print_all():
        w2.setFocus()
        print w1.get_annotations()
        print w1.get_param_annotations()
    
    w2 = QtGui.QPushButton('get')
    #~ w2.show()
    
    w2.clicked.connect(print_all)
    
    h.addWidget(w1)
    h.addWidget(w2)
    w.show()
    
    app.exec_()
    #~ print w.get_annotations()
    #~ print w.get_param_annotations()

    

    



if __name__ == '__main__':
    test1()
