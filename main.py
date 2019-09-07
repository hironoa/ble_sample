from pybleno import *
import sys
import signal
from EchoCharacteristic import *

echoCharacteristic = EchoCharacteristic('ec0F')

def onStateChange(state):
   print('on -> stateChange: ' + state)

   if (state == 'poweredOn'):
     bleno.startAdvertising('test', ['ec00'])
   else:
     bleno.stopAdvertising()

    
def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': 'ec00',
                'characteristics': [ 
                    #EchoCharacteristic('ec0F')
                    echoCharacteristic
                    ]
            })
        ])

import time

if __name__ == '__main__':
    print('bleno - echo')

    bleno = Bleno()
            
    bleno.on('stateChange', onStateChange)
    bleno.on('advertisingStart', onAdvertisingStart)

    bleno.start()

    print ('Hit <ENTER> to disconnect')

    count = 0
    while True:
        if echoCharacteristic._updateValueCallback:
            echoCharacteristic._updateValueCallback(str(count).encode())
            count += 1
        time.sleep(1)

    if (sys.version_info > (3, 0)):
        input()
    else:
        raw_input()

    bleno.stopAdvertising()
    bleno.disconnect()

    print ('terminated.')
    sys.exit(1)
