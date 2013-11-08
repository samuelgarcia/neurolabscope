# -*- coding: utf-8 -*-
"""
metadata widget
"""


from PyQt4 import QtCore,QtGui
import pyqtgraph as pg
import copy

from .guiutil import icons, get_dict_from_group_param, set_dict_to_param_group
import  pyacq.gui.guiutil.mypyqtgraph as mypg

#~ _params_options = [
                                        #~ { 'name' : 'recording_mode', 'type' :'list', 'values' : ['continuous', ] },

_default_param_metadata = [
                                                            { 'name' : 'animal', 'type' :'str', 'values' : '', 'renamable': True, 'removable': True },
                                                            { 'name' : 'trial', 'type' :'str', 'values' : '', 'renamable': True, 'removable': True },
                                                            ]
#'readonly': True

class CustumGroup(pg.parametertree.parameterTypes.GroupParameter):
    def __init__(self, **opts):
        pg.parametertree.parameterTypes.GroupParameter.__init__(self, **opts)
        self.n = len(opts['children'])
    
    def addNew(self):
        self.addChild({ 'name' : 'new_field_{}'.format(self.n), 'type' :'str', 'values' : '', 'renamable': True, 'removable': True  })
        self.n += 1



class MetadataWidget(QtGui.QWidget):
    def __init__(self, parent  = None, param_metadata = None):
        QtGui.QWidget.__init__(self, parent = parent)
        
        mainlayout = QtGui.QVBoxLayout()
        self.setLayout(mainlayout)
        
        #~ h = QtGui.QHBoxLayout()
        #~ mainlayout.addLayout(h)
        #~ h.addWidget(QtGui.QLabel('Metadata'),10)
        
        #~ but = QtGui.QPushButton(icon = QtGui.QIcon(':/configure.png'))
        #~ h.addWidget(but)
        #~ but.clicked.connect(self.open_set_dialog)
        
        self.tree = pg.parametertree.ParameterTree(showHeader = False)
        mainlayout.addWidget(self.tree)
        
        if param_metadata is None:
            param_metadata = _default_param_metadata
        self.param_metadata = param_metadata
        

        self.params = CustumGroup(name='metadata', type='group', children = self.param_metadata, addText = u'Add')
        self.tree.setParameters(self.params)

    def get_metadata(self, cascade = True,  dict_type = 'OrderedDict'):
        return mypg.get_dict_from_group_param(self.params, cascade = cascade, dict_type = dict_type)
        
    def get_param_metadata(self):
        
        #~ print self.params.opts.get('children')
        p = [ ]
        for child in self.params.children():
            #~ print child.name(), child.type(), child.opts
            p.append(child.opts)
            
        return p
        #~ return self.param_metadata
    
    
    #~ def open_set_dialog(self):
        #~ d = ConfigureMetadataWidget(param_metadata = self.param_metadata)
        #~ if d.exec_():
            #~ print d
        
            


#~ class ConfigureMetadataWidget(QtGui.QDialog):
    #~ def __init__(self, parent = None, param_metadata = None):
        #~ QtGui.QDialog.__init__(self, parent)
        
        #~ self.param_metadata = copy.deepcopy(param_metadata)
        
        #~ self.setWindowTitle(u'Configure metadata tree')
        #~ self.setWindowIcon(QtGui.QIcon(':/neurolabscope.png'))
        
        
        #~ mainlayout = QtGui.QVBoxLayout()
        #~ self.setLayout(mainlayout)

        
        
        #~ buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok| QtGui.QDialogButtonBox.Cancel)
        #~ mainlayout.addWidget(buttonBox)
        #~ buttonBox.accepted.connect(self.accept)
        #~ buttonBox.rejected.connect(self.reject)
    
    #~ def get(self):
        #~ return self.param_metadata
        
        


