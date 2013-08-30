# -*- coding: utf-8 -*-


n = 4
default_setup = {
    'devices' : [
        {
            'class' : 'FakeMultiSignals',
            'board_name' : 'fake  analog input'.format(n),
            'global_param' : {
                                            'sampling_rate' : 1000.,
                                            'buffer_length' : 60.,
                                            'nb_channel' : n,
                                            'packet_size' : 10, 
            },
            'subdevices' : [
                {
                    'type' : 'AnalogInput',
                    'nb_channel' : n,
                    'global_param' : {},
                    'by_channel_param' : {
                        'ai_channel_indexes' : range(n),
                        'ai_channel_names' : [ 'AI Channel {}'.format(i) for i in range(n)],
                    },
                },
            ]
        },
    ],

    
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



#~ import json
#~ json.dump(default_setup,open('setup_test.json', 'wb'), indent=4, separators=(',', ': '))