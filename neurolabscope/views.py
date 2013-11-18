# -*- coding: utf-8 -*-
from collections import OrderedDict

from pyacq.gui import Oscilloscope, OscilloscopeDigital, TimeFreq

views_list = [Oscilloscope, OscilloscopeDigital, TimeFreq ]
views_dict = OrderedDict()
for v in views_list:
    views_dict[v.__name__] = v

subdevice_to_view = {
    'AnalogInput': ['Oscilloscope', 'TimeFreq'],
    'DigitalInput':  ['OscilloscopeDigital'],
    'Event' : [ ],
}
