# -*- coding: utf-8 -*-
"""
annotations widget
"""


from PyQt4 import QtCore,QtGui
import pyqtgraph as pg
import copy

from .guiutil import icons, get_dict_from_group_param, set_dict_to_param_group
import  pyacq.gui.guiutil.mypyqtgraph as mypg

_default_param_annotations = [
                                                            { 'name' : 'animal', 'type' :'str', 'values' : '', 'renamable': True, 'removable': True },
                                                            { 'name' : 'trial', 'type' :'str', 'values' : '', 'renamable': True, 'removable': True },
                                                            ]

class CustumGroup(pg.parametertree.parameterTypes.GroupParameter):
    def __init__(self, **opts):
        pg.parametertree.parameterTypes.GroupParameter.__init__(self, **opts)
        self.n = len(opts['children'])
    
    def addNew(self):
        self.addChild({ 'name' : 'new_field_{}'.format(self.n), 'type' :'str', 'values' : '', 'renamable': True, 'removable': True  })
        self.n += 1



class AnnotationsWidget(QtGui.QWidget):
    def __init__(self, parent  = None, param_annotations = None):
        QtGui.QWidget.__init__(self, parent = parent)
        
        mainlayout = QtGui.QVBoxLayout()
        self.setLayout(mainlayout)
        
        self.tree = pg.parametertree.ParameterTree(showHeader = False)
        mainlayout.addWidget(self.tree)
        
        if param_annotations is None:
            param_annotations = _default_param_annotations
        self.param_annotations = param_annotations
        

        self.params = CustumGroup(name='annotations', type='group', children = self.param_annotations, addText = u'Add')
        self.tree.setParameters(self.params)

    def get_annotations(self, cascade = True,  dict_type = 'OrderedDict'):
        return mypg.get_dict_from_group_param(self.params, cascade = cascade, dict_type = dict_type)
        
    def get_param_annotations(self):
        p = [ ]
        for child in self.params.children():
            p.append(child.opts)
        return p

