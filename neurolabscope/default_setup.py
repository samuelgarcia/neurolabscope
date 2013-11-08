# -*- coding: utf-8 -*-

from pyacq import FakeMultiSignals
print FakeMultiSignals.get_available_devices().values()[0]

from .configure import _params_options
import  pyacq.gui.guiutil.mypyqtgraph as mypg
import pyqtgraph as pg
p = pg.parametertree.Parameter.create(name='options', type='group', children=_params_options)
options = mypg.get_dict_from_group_param(p)
print options

default_setup = {
    'devices' : [ FakeMultiSignals.get_available_devices().values()[0] ],
    'views' : [
        {
            'class' : 'Oscilloscope',
            'name' : 'Oscilloscope',
            'device_num' : 0,
            'subdevice_num' : 0,
            'params' : {
            
            }
        },
    ],
    'options' : options,
    
    
    
}


