# -*- coding: utf-8 -*-
"""

"""


from PyQt4 import QtCore,QtGui
import pyqtgraph as pg
import datetime


from .guiutil import icons
#~ import  pyacq.gui.guiutil.mypyqtgraph as mypg

import subprocess
import sys, os

class RecordingList(QtGui.QWidget):
    def __init__(self, parent  = None, ):
        QtGui.QWidget.__init__(self, parent = parent)
        
        self.setMinimumSize(10,10)
        
        mainlayout = QtGui.QVBoxLayout()
        self.setLayout(mainlayout)
        
        self.rec_list = QtGui.QTreeWidget(columnCount = 3)
        mainlayout.addWidget(self.rec_list)
        self.rec_list.itemDoubleClicked.connect( self.open_fileexplorer)
        
        self.time_flash = QtCore.QTimer(interval = 500)
        self.time_flash.timeout.connect(self.refresh_color)
        self.flash_state = True
        self.time_flash.start()
        
        self.list = [ ]
        
    
    def refresh_color(self):
        self.flash_state = not(self.flash_state)
        for rec in self.list:
            if rec['state'] == 'finished':
                color = 'green'
            elif rec['state'] == 'recording' and self.flash_state:
                color = 'orange'
            else:
                color = 'white'
            brush = QtGui.QBrush(QtGui.QColor(color), QtCore.Qt.SolidPattern)
            brush.setColor(QtGui.QColor(color))
            rec['item'].setBackground(0, brush)
    
    def refresh_list(self):
        pass
    
    def add_rec(self, name, dirname, rec_datetime, state = 'recording'):
        item = QtGui.QTreeWidgetItem([ name  ,'' , '' ] )
        item.setToolTip(0,name)
        
        self.list.append( {'name' : name, 'dirname': dirname, 'rec_datetime' : rec_datetime, 'item' : item , 'state' : state})
        self.rec_list.addTopLevelItem(item)
    
    def open_fileexplorer(self, item, column):
        #~ print item.index.row()
        i = self.rec_list.	indexOfTopLevelItem(item)
        dirname = self.list[i]['dirname']


        if sys.platform.startswith('win'):
            os.startfile(dirname)
        elif sys.platform.startswith('linux'):
            os.system('xdg-open "{}"'.format(dirname))
        elif sys.platform== 'darwin' :
            os.system('open "{}"'.format(dirname))




