# -*- coding: utf-8 -*-
"""
Neurolabscope configuration nwindow.
"""

from PyQt4 import QtCore,QtGui
import pyqtgraph as pg
import os
import copy

from .guiutil import icons, get_dict_from_group_param, set_dict_to_param_group
from .default_setup import default_setup
from pyacq import device_classes


default_view = {
    'AnalogInput': 'Oscilloscope',
    'DigitalInput': 'OscilloscopeDigital',
}


class ConfigWindow(QtGui.QWidget):
    def __init__(self, parent  = None, setup = None):
        QtGui.QWidget.__init__(self, parent = parent)
        
        self.setup = setup
        if self.setup is None: 
            self.setup = default_setup
        
        self.setWindowTitle(u'Setup configuration')
        self.setWindowIcon(QtGui.QIcon(':/neurolabscope.png'))
        
        mainlayout = QtGui.QVBoxLayout()
        self.setLayout(mainlayout)
        
        # actions
        self.toolbar = QtGui.QToolBar()
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)        
        mainlayout.addWidget(self.toolbar)
        self.toolbar.setIconSize(QtCore.QSize(60, 40))

        self.actAddDev = QtGui.QAction(u'&Add device', self,icon =QtGui.QIcon(':/list-add.png'))
        self.toolbar.addAction(self.actAddDev)
        self.actAddDev.triggered.connect(self.add_device)

        self.actRemoveDev = QtGui.QAction(u'&Remove device', self,icon =QtGui.QIcon(':/list-remove.png'))
        self.actRemoveDev.triggered.connect(self.remove_device)

        self.actConfigDev = QtGui.QAction(u'&Configure device', self,icon =QtGui.QIcon(':/configure.png'))
        self.actConfigDev.triggered.connect(self.config_device)

        self.actConfigSubDev = QtGui.QAction(u'&Configure subdevice', self,icon =QtGui.QIcon(':/configure.png'))
        self.actConfigSubDev.triggered.connect(self.config_subdevice)
        
        self.actAddView = QtGui.QAction(u'&Add view', self,icon =QtGui.QIcon(':/list-add.png'))
        self.actAddView.triggered.connect(self.add_view)

        self.actRemoveView = QtGui.QAction(u'&Remove view', self,icon =QtGui.QIcon(':/list-remove.png'))
        self.actRemoveView.triggered.connect(self.remove_view)

        
        # treeview
        
        self.tree = pg.TreeWidget()
        mainlayout.addWidget(self.tree)
        self.tree.setIconSize(QtCore.QSize(64, 40))
        
        for dev in self.setup['devices']:
            item  = QtGui.QTreeWidgetItem(['{class} : {board_name}'.format(**dev )])
            item.setIcon(0, QtGui.QIcon(':/device.png'))
            item.type = 'device'
            item.params = dev
            self.tree.addTopLevelItem(item)
            for sub in dev['subdevices']:
                name = '{type} {nb_channel} channels'.format(**sub) if 'nb_channel' in sub else sub['type']
                subitem  = QtGui.QTreeWidgetItem([name])
                subitem.setIcon(0, QtGui.QIcon(':/{}.png'.format(sub['type'])))
                subitem.type = 'subdevice'
                item.addChild(subitem)
            
        for view in self.setup['views']:
            subitem = self.tree.topLevelItem (view['device_num']).child(view['subdevice_num'])
            viewitem = QtGui.QTreeWidgetItem(['{name}'.format(**view )])
            viewitem.setIcon(0, QtGui.QIcon(':/{}.png'.format(view['class'])))
            viewitem.type = 'view'
            subitem.addChild(viewitem)
        
        self.tree.expandAll()
        
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.context_menu)
        
        mainlayout.addWidget(QtGui.QLabel('Right click on item to remove add views'))
        
        
    def add_device(self):
        
        d = NewDeviceDialog()
        if d.exec_():
            if d.get() is None: return
            name, info_device =  d.get()
            
            item  = QtGui.QTreeWidgetItem(['{} : {}'.format(info_device['class'], name )])
            item.setIcon(0, QtGui.QIcon(':/device.png'))
            item.type = 'device'
            item.params = info_device
            self.tree.addTopLevelItem(item)
            for sub in info_device['subdevices']:
                name = '{type} {nb_channel} channels'.format(**sub) if 'nb_channel' in sub else sub['type']
                subitem  = QtGui.QTreeWidgetItem([name])
                subitem.setIcon(0, QtGui.QIcon(':/{}.png'.format(sub['type'])))
                subitem.type = 'subdevice'
                item.addChild(subitem)
                
                # Add one default view
                view_class = default_view[sub['type']]
                viewitem = QtGui.QTreeWidgetItem(['{}'.format(view_class)])
                viewitem.setIcon(0, QtGui.QIcon(':/{}.png'.format(view_class)))
                viewitem.type = 'view'
                subitem.addChild(viewitem)
    
    
    def remove_device(self):
        l = self.tree.selectedIndexes()
        if len(l) == 0: return
        index = l[0]
        self.tree.takeTopLevelItem(index.row())
    
    def config_device(self):
        item = self.tree.selectedItems()[0]
        d = ConfigDeviceWidget( params = item.params)
        if d.exec_():
            print d.get()
        
    
    def config_subdevice(self):
        pass
    
    def add_view(self):
        pass
        
    def remove_view(self):
        pass

    
    def context_menu(self):
        menu = QtGui.QMenu()
        if len(self.tree.selectedItems())==0:
            menu.addActions([self.actAddDev])
        else:
            t = self.tree.selectedItems()[0].type
            if t == 'device':
                menu.addActions([self.actConfigDev, self.actRemoveDev])
            elif t == 'subdevice':
                menu.addActions([self.actConfigSubDev, self.actAddView])
            elif t == 'view':
                menu.addAction(self.actRemoveView)
        act = menu.exec_(self.cursor().pos())

    
class NewDeviceDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        
        self.setWindowTitle(u'Choose new device')
        self.setWindowIcon(QtGui.QIcon(':/neurolabscope.png'))
        
        mainlayout = QtGui.QVBoxLayout()
        self.setLayout(mainlayout)
        
        but = QtGui.QPushButton(QtGui.QIcon(':/reload.png'), 'Rescan devices', )
        mainlayout.addWidget(but)
        but.clicked.connect(self.refresh_list)
        
        self.show_fake = QtGui.QCheckBox('Show fake device', checked = False)
        mainlayout.addWidget(self.show_fake)
        self.show_fake.stateChanged.connect(self.refresh_list)
        
        self.list = QtGui.QListWidget()
        mainlayout.addWidget(self.list)
        self.list.itemDoubleClicked.connect(self.accept)
        
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok| QtGui.QDialogButtonBox.Cancel)
        mainlayout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        self.refresh_list()
    
    
    def refresh_list(self, state = None):
        self.scans = [ ]
        self.list.clear()
        for dev_class in device_classes:
            for name, info_device in dev_class.get_available_devices().items():
                if not self.show_fake.isChecked() and name.startswith('fake'):
                    continue
                item = QtGui.QListWidgetItem('{}'.format(name))
                self.list.addItem(item)
                item.setIcon(QtGui.QIcon(':/device.png'))
                self.scans.append((name, info_device))
                
    
    def get(self):
        l = self.list.selectedIndexes()
        if len(l)>0:
            return self.scans[l[0].row()]
            



class ConfigDeviceWidget(QtGui.QDialog):
    def __init__(self, parent = None, params = None):
        QtGui.QDialog.__init__(self, parent)
        
        self.params = copy.deepcopy(params)
        

        self.setWindowTitle(u'Configure device')
        self.setWindowIcon(QtGui.QIcon(':/neurolabscope.png'))

        mainlayout = QtGui.QVBoxLayout()
        self.setLayout(mainlayout)

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok| QtGui.QDialogButtonBox.Cancel)
        mainlayout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


    def get(self):
        return








