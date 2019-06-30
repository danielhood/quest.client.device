import urllib3
import platform
import requests
import platform
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class QuestApiClient:
    def __init__(self, baseUri):
        self.baseUri = baseUri
        self.deviceKey = 'somesecretkeythattheapponlyknows'
        self.authToken = ''
        self.deviceType = ''


    def register(self):
        print ('Registering device: '+ platform.node() + ':' + self.deviceKey)
        deviceRequest = {}
        deviceRequest['hostname'] = platform.node()
        deviceRequest['devicekey'] = self.deviceKey

        try:

            response = requests.get(self.baseUri + '/token', data=json.dumps(deviceRequest), verify=False, timeout=2)
            if (response.ok):
                self.authToken = response.text
                print ('Registered: {0}'.format(self.authToken))
                self.refresh_device_info()
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
        print ('Refreshing device info')
        deviceRequest = {}
        deviceRequest['hostname'] = platform.node()
        deviceRequest['devicekey'] = self.deviceKey

        try:
            response = requests.get(self.baseUri + '/device', data=json.dumps(deviceRequest), verify=False, timeout=2, headers={'Authorization':'Bearer {0}'.format(self.authToken)})
            if (response.ok):
                print ('JSON: {0}'.format(response.text))
                device = response.json()
                self.deviceType = device['devicetype']
                print ('deviceType: {0}'.format(self.deviceType))
            elif (response.status_code == 401):
                print ('Unauthorized')
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
            elif (response.status_code == 401):
                print ('Unauthorized')
            else:
                print ('Trigger ERROR. Response: {0}'.format(response.status_code))
        except Exception as e:
            print ('Unable to trigger action with Quest server')
            print (e)
            return 'ERROR'
        return 'SUCCESS'

