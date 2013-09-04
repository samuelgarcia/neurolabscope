# -*- coding: utf-8 -*-

from pyacq import FakeMultiSignals
print FakeMultiSignals.get_available_devices().values()[0]
default_setup = {
    'devices' : [ FakeMultiSignals.get_available_devices().values()[0] ],
    'views' : [
        {
            'class' : 'Oscilloscope',
            'name' : 'Oscilloscope',
            'device_num' : 0,
            'subdevice_num' : 0,
            'kargs' : {
            
            }
        },
    ],
}


