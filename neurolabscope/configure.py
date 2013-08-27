# -*- coding: utf-8 -*-
"""
Neurolabscope configuration nwindow.
"""

from PyQt4 import QtCore,QtGui
import os

from .guiutil import *



class ConfigWindow(QtGui.QWidget):
    def __init__(self, parent  = None):
        QtGui.QWidget.__init__(self, parent = parent)
        
        self.setWindowTitle(u'Configuration')
        self.setWindowIcon(QtGui.QIcon(':/neurolabscope.png'))
        
        
        
        
