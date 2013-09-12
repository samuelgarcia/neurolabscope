# -*- coding: utf-8 -*-
"""
Neurolabscope configuration nwindow.
"""

from PyQt4 import QtCore,QtGui
import pyqtgraph as pg
import os
import copy
import json

from .guiutil import icons, get_dict_from_group_param, set_dict_to_param_group
from .default_setup import default_setup
from pyacq import device_classes


subdevice_to_view = {
    'AnalogInput': ['Oscilloscope', 'TimeFreq'],
    'DigitalInput':  ['OscilloscopeDigital'],
}


class ConfigWindow(QtGui.QDialog):
    def __init__(self, parent  = None, setup = None):
        QtGui.QDialog.__init__(self, parent = parent)
        
        if setup is None: 
            setup = default_setup
        
        self.setWindowTitle(u'Setup configuration')
        self.setWindowIcon(QtGui.QIcon(':/neurolabscope.png'))
        self.resize(640, 640)
        
        mainlayout = QtGui.QVBoxLayout()
        self.setLayout(mainlayout)
        
        # actions
        self.toolbar = QtGui.QToolBar()
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)        
        mainlayout.addWidget(self.toolbar)
        self.toolbar.setIconSize(QtCore.QSize(60, 40))

        self.actLoadSetup = QtGui.QAction(u'&Load setup', self,icon =QtGui.QIcon(':/document-open-folder.png'))
        self.toolbar.addAction(self.actLoadSetup)
        self.actLoadSetup.triggered.connect(self.load_setup)

        self.actSaveSetup = QtGui.QAction(u'&Save setup', self,icon =QtGui.QIcon(':/document-save.png'))
        self.toolbar.addAction(self.actSaveSetup)
        self.actSaveSetup.triggered.connect(self.save_setup)

        self.actAddDev = QtGui.QAction(u'&Add device', self,icon =QtGui.QIcon(':/list-add.png'))
        self.toolbar.addAction(self.actAddDev)
        self.actAddDev.triggered.connect(self.add_device)
        
        

        self.actRemoveDev = QtGui.QAction(u'&Remove device', self,icon =QtGui.QIcon(':/list-remove.png'))
        self.actRemoveDev.triggered.connect(self.remove_device)

        self.actConfigDev = QtGui.QAction(u'&Configure device', self,icon =QtGui.QIcon(':/configure.png'))
        self.actConfigDev.triggered.connect(self.config_device)

        self.actAddView = QtGui.QAction(u'&Add view', self,icon =QtGui.QIcon(':/list-add.png'))
        self.actAddView.triggered.connect(self.add_view)

        self.actRemoveView = QtGui.QAction(u'&Remove view', self,icon =QtGui.QIcon(':/list-remove.png'))
        self.actRemoveView.triggered.connect(self.remove_view)

        
        # treeview
        #~ self.tree = pg.TreeWidget()
        self.tree = QtGui.QTreeWidget()
        mainlayout.addWidget(self.tree)
        self.tree.setIconSize(QtCore.QSize(64, 40))
        self.set_setup(setup)
        self.tree.expandAll()
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.context_menu)
        mainlayout.addWidget(QtGui.QLabel('Right click on item to remove add views'))

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok| QtGui.QDialogButtonBox.Cancel)
        mainlayout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
    
    
    def set_setup(self, setup):
        self.tree.clear()
        self.setup = setup
        
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
            subitem = self.tree.topLevelItem(view['device_num']).child(view['subdevice_num'])
            viewitem = QtGui.QTreeWidgetItem(['{name}'.format(**view )])
            viewitem.setIcon(0, QtGui.QIcon(':/{}.png'.format(view['class'])))
            viewitem.type = 'view'
            viewitem.params = view
            subitem.addChild(viewitem)
        

    def get_setup(self):
        setup ={'devices':[ ], 'views' : [ ] }
        for d in range(self.tree.topLevelItemCount()):
            devitem = self.tree.topLevelItem(d)
            setup['devices'].append(devitem.params)
            for s,subdev in enumerate(devitem.params['subdevices']):
                subitem = devitem.child(s)
                for v in range(subitem.childCount()):
                    viewitem  = subitem.child(v)
                    p = viewitem.params
                    p['device_num'] = d
                    p['subdevice_num'] = s
                    setup['views'].append(p)
        return setup
    
    def load_setup(self):
        fd = QtGui.QFileDialog(fileMode= QtGui.QFileDialog.ExistingFile, acceptMode = QtGui.QFileDialog.AcceptOpen)
        fd.setNameFilter('Neurolabscope setup (*.json)')
        if fd.exec_():
            filename = unicode(fd.selectedFiles()[0])
            self.set_setup(json.load(open(filename, 'rb')))

        
    def save_setup(self):
        fd = QtGui.QFileDialog(fileMode= QtGui.QFileDialog.AnyFile, acceptMode = QtGui.QFileDialog.AcceptSave)
        fd.setNameFilter('Neurolabscope setup (*.json)')
        if fd.exec_():
            filename = unicode(fd.selectedFiles()[0])
            json.dump(self.get_setup(),open(filename, 'wb'), indent=4, separators=(',', ': '))

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
                view_class = subdevice_to_view[sub['type']][0]
                name = '{}'.format(view_class)
                viewitem = QtGui.QTreeWidgetItem([name])
                viewitem.setIcon(0, QtGui.QIcon(':/{}.png'.format(view_class)))
                viewitem.type = 'view'
                viewitem.params = {'class':view_class, 'name': name, 'kargs': {}, }
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
            #~ print d.get()
            item.params = d.get()
            
        
    
    def add_view(self):
        l = self.tree.selectedItems()
        if len(l) == 0: return
        subitem = l[0]
        devitem = subitem.parent()
        num_subdevice = self.tree.selectedIndexes()[0].row()
        subdev = devitem.params['subdevices'][num_subdevice]
        
        menu = QtGui.QMenu()
        actions = [ ]
        view_classes = subdevice_to_view[subdev['type']]
        for view_class in view_classes:
            act = QtGui.QAction(view_class, self, icon =  QtGui.QIcon(':{}.png'.format(view_class)) )
            actions.append(act)
            menu.addAction(act)
        act = menu.exec_(self.cursor().pos())
        if act is None: return
        view_class = view_classes[actions.index(act)]
        
        name = '{} {}'.format(view_class, subitem.childCount())
        viewitem = QtGui.QTreeWidgetItem([name])
        viewitem.setIcon(0, QtGui.QIcon(':/{}.png'.format(view_class)))
        viewitem.type = 'view'
        viewitem.params = {'class':view_class, 'name': name, 'kargs': {}, }
        subitem.addChild(viewitem)
        
    def remove_view(self):
        l = self.tree.selectedItems()
        if len(l) == 0: return
        item = l[0]
        item.parent().takeChild(self.tree.selectedIndexes()[0].row())

    
    def context_menu(self):
        menu = QtGui.QMenu()
        if len(self.tree.selectedItems())==0:
            menu.addActions([self.actAddDev])
        else:
            t = self.tree.selectedItems()[0].type
            if t == 'device':
                menu.addActions([self.actConfigDev, self.actRemoveDev])
            elif t == 'subdevice':
                menu.addActions([self.actAddView])
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
        
        self.resize(600, 800)
        
        self.fix_parms = copy.deepcopy(params)
        
        self.setWindowTitle(u'Configure device')
        self.setWindowIcon(QtGui.QIcon(':/neurolabscope.png'))

        mainlayout = QtGui.QVBoxLayout()
        self.setLayout(mainlayout)

        self.treeParam = pg.parametertree.ParameterTree()
        self.treeParam.header().hide()
        mainlayout.addWidget(self.treeParam)
        
        conv = {str : 'str', float : 'float',  int : 'int' }

        all = [ ]
        for k, v in params['global_params'].items():
            #~ if k in ['subdevices' , 'class', ] : continue
            if type(v) in conv :
                d = { 'name' : k, 'type' : conv[type(v)], 'value' : v }
                all.append(d)
        
        self.subdev_names= [ ]
        for s, sub in enumerate(params['subdevices' ]):
            subparams = [ ]
            print sub
            n = sub['nb_channel']
            for i in range(n):
                bychannel = [ ]
                
                channel_index = sub['by_channel_params']['channel_indexes'][i]
                
                
                for k, v in sub['by_channel_params'].items():
                    if k=='channel_indexes' :
                        continue
                    elif k=='channel_selection' :
                        bychannel.append({ 'name' : 'selected', 'type' :'bool', 'value' : v[i] })
                    elif k== 'channel_names':
                        bychannel.append({ 'name' : 'name', 'type' :'str', 'value' : v[i] })
                    #~ elif k=='channel_ranges':
                        #~ bychannel.append({ 'name' : 'AD_range', 'type' :'range', 'value' : v[i] })
                    else:
                        pass
                        #~ if type(v[i]) in conv :
                            #~ bychannel.append({ 'name' : k, 'type' : conv[type(v[i])], 'value' : v[i] })
                    #~ bychannel.append({ 'name' : k, 'type' :'float', 'value' : 1. })
                    
                d = { 'name' : 'Channel {}'.format(channel_index), 'type' : 'group', 'children' : bychannel }
                subparams.append(d)
                
            #~ sub['by_channel_params']
            name = '{} {type} {nb_channel} channels'.format(s, **sub) if 'nb_channel' in sub else sub['type']
            d = { 'name' : name, 'type' : 'group', 'children' : subparams }
            self.subdev_names.append(name)
            all.append(d)
        
        self.params = pg.parametertree.Parameter.create(name='Parameters for {}'.format(params['board_name']), type='group', children=all)
        
        self.treeParam.setParameters(self.params, showTop=True)
        
        
         
        
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok| QtGui.QDialogButtonBox.Cancel)
        mainlayout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        


    def get(self):
        
        params = self.fix_parms
        d = get_dict_from_group_param(self.params, cascade = False)
        params['global_params'].update(d)
        
        for s,sub in enumerate(params['subdevices' ]):
            subparams = self.params.param(self.subdev_names[s])
            for i, channel_params in enumerate(subparams.children()):
                for p in channel_params:
                    if p.name() == 'name':
                        sub['by_channel_params']['channel_names'][i] = p.value()
                    elif p.name() == 'selected':
                        sub['by_channel_params']['channel_selection'][i] = p.value()
                    #~ elif p.name() == 'AD_range':
        
        return params








