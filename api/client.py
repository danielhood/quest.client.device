import urllib3
import platform
import requests
import platform
import json
import threading
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class QuestApiClient:
    def __init__(self, baseUri):
        self.baseUri = baseUri
        self.deviceKey = 'somesecretkeythattheapponlyknows'
        self.authToken = ''
        self.deviceType = ''
        self.refreshThread = threading.Thread(target = self.device_monitor, daemon=True)
        self.refreshThread.start()

    def device_monitor(self):
        while True:
            self.refresh_device_info()
            time.sleep(5)
    

    def register(self):
        print ('Registering device: '+ platform.node() + ':' + self.deviceKey)
        deviceRequest = {}
        deviceRequest['hostname'] = platform.node()
        deviceRequest['devicekey'] = self.deviceKey

        try:
            response = requests.get(self.baseUri + '/token', data=json.dumps(deviceRequest), verify=False, timeout=2)
            if (response.ok):
                self.authToken = response.json()['token']
                print ('Registered: {0}'.format(self.authToken))
                return True
            elif (response.status_code == 401):
                print ('Unauthorized')
                return False
            else:
                print ('response.NotOK:' + str(response.status_code))
                return False
        except Exception as e:
            print ('Unable to register with Quest server')
            print (e)
            return False

    def refresh_device_info(self):
        deviceRequest = {}
        deviceRequest['hostname'] = platform.node()
        deviceRequest['devicekey'] = self.deviceKey

        try:
            response = requests.get(self.baseUri + '/device', data=json.dumps(deviceRequest), verify=False, timeout=2, headers={'Authorization':'Bearer {0}'.format(self.authToken)})
            if (response.ok):
                device = response.json()
                if (self.deviceType != device['devicetype']):
                    print ('DeviceType changed to: {0}'.format(device['devicetype']))
                    self.deviceType = device['devicetype']
            elif (response.status_code == 401):
                print ('Respone 401 from device request')
                self.register()
            else:
                print ('response.NotOK:{0}'.format(response.status_code))
        except Exception as e:
            print ('Unable to retrieve device info')
            print (e)

    def trigger_player_action(self, playerCode):
        print ('Triggering action with server...')
        triggerRequest = {}
        triggerRequest['playercode'] = playerCode
        triggerRequest['devicetype'] = self.deviceType

        try:
            response = requests.post(self.baseUri + '/trigger', data=json.dumps(triggerRequest), verify=False, timeout=2, headers={'Authorization':'Bearer {0}'.format(self.authToken)})
            if (response.ok):
                print ('Trigger respone: {0}'.format(response.text))
                return response.text
            elif (response.status_code == 401):
                print ('Unauthorized')
            else:
                print ('Trigger ERROR. Response: {0}'.format(response.status_code))
        except Exception as e:
            print ('Unable to trigger action with Quest server')
            print (e)

        return 'ERROR'

