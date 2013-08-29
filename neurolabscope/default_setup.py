# -*- coding: utf-8 -*-



default_setup = {
    'devices' : [
        {
            'class' : 'FakeMultiSignals',
            
            'kargs' : {
                    'name' : 'Test dev',
                    'nb_channel' : 3,
                    'sampling_rate' :10000.,
                    'buffer_length' : 64,
                    'packet_size' : 10,
            
            }
        
        
        }
    
    
    ],
    
    'views' : [
        {
            'class' : 'Oscilloscope',
            'name' : 'Oscilloscope',
            'device_num' : 0,
            'stream_num' : 0,
            'kargs' : {
            
            }
        },

    ],
}



#~ import json
#~ json.dump(default_setup,open('setup_test.json', 'wb'), indent=4, separators=(',', ': '))