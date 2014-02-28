# -*- coding: utf-8 -*-



from PyQt4 import QtCore,QtGui
import pyqtgraph as pg
from collections import OrderedDict
import datetime
import time


import numpy as np


class ThreadWaitStop(QtCore.QThread):
    rec_terminated = QtCore.pyqtSignal()
    def __init__(self, parent=None, rec_engine = None):
        QtCore.QThread.__init__(self, parent)
        self.running = False
        self.rec_engine = rec_engine
    
    def run(self):
        self.running = True
        while self.running:
            time.sleep(0.01)
            if not self.rec_engine.is_recording():
                self.rec_terminated.emit()
                break






class ConfigRecOnTrig(QtGui.QDialog):
    def __init__(self, parent  = None, setup = None):
        QtGui.QDialog.__init__(self, parent = parent)
        
        mainlayout = QtGui.QVBoxLayout()
        self.setLayout(mainlayout)
        
        #TODO limits for channel
        # TODO stream
        _params_triggers = [
                                                #~ { 'name' : 'stream', 'type' :'list', 'value' : 0,  'limits':[0,1] },
                                                #~ { 'name' : 'channel', 'type' :'int', 'value' : 0,  'limits':[0,1] },
                                                
                                                { 'name' : 'threshold', 'type' :'float', 'value' : 0.25 },
                                                { 'name' : 'front', 'type' :'list', 'values' : ['+', '-', ] },
                                                
                                                
                                                { 'name' : 'debounce_time', 'type' :'float', 'value' : 0.05, 'limits' : [0, np.inf], 'step' : 0.001 , 'suffix': 's', 'siPrefix': True },
                                                { 'name' : 'debounce_mode', 'type' :'list', 'values' : [ 'no-debounce', 'after-stable' , 'before-stable' ] },
                                            ]
        
        self.tree_trigger = pg.parametertree.ParameterTree()
        mainlayout.addWidget(self.tree_trigger)
        self.tree_trigger.header().hide()
        self.param_triggers = pg.parametertree.Parameter.create(name='options', type='group', children=_params_triggers)
        self.tree_trigger.setParameters(self.param_triggers)


        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok| QtGui.QDialogButtonBox.Cancel)
        mainlayout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        
        
        
