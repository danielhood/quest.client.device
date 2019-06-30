import urllib3
import sys, time
import requests, json
import RPi.GPIO as GPIO
import pygame
import platform

BTN1 = 3
LED1 = 5
LED2 = 7
LED3 = 11
LED4 = 13

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GpioHandler:
    def __init__(self, audioHandler, apiClient):
        self.buttonState = False
        self.audioHandler = audioHandler
        self.apiClient = apiClient

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BTN1, GPIO.IN) # Hardwired PULL UP, so button triggers LOW state
        GPIO.setup(LED1, GPIO.OUT)
        GPIO.setup(LED2, GPIO.OUT)
        GPIO.setup(LED3, GPIO.OUT)
        GPIO.setup(LED4, GPIO.OUT)

        GPIO.add_event_detect(BTN1, GPIO.FALLING)
        GPIO.add_event_callback(BTN1, self.button_pressed)

    def decode_player_id(self):
        # TODO: decode player id from IR stream
        return "1234abcd"

    def button_pressed(self, channel):
        print('button_pressed() - enter')
    
        action = self.apiClient.trigger_player_action(self.decode_player_id())

        if action == 'SUCCESS':
            self.audioHandler.play_success()

            for i in range(1, 32):
                GPIO.output(LED1, (i % 2 == 0))
                GPIO.output(LED2, (i % 3 == 0))
                GPIO.output(LED3, (i % 2 != 0))
                GPIO.output(LED4, (i % 4 == 0))
                time.sleep(0.1)

        elif action == 'NOQUEST':
            # TODO:
            time.sleep(1)
        else:
            # TODO:
            time.sleep(1)

        GPIO.output(LED1, False)
        GPIO.output(LED2, False)
        GPIO.output(LED3, False)
        GPIO.output(LED4, False)

        print ('button_pressed() - exit')


class AudioHandler:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.mixer.init()

        self.SoundSuccess = pygame.mixer.Sound('1.wav')
        self.SoundSuccess.set_volume(0.5)

        # TODO: define other sound and light animiation responses

    def play_success(self):
        if not pygame.mixer.music.get_busy():
            self.SoundSuccess.play()


class QuestApiClient:
    def __init__(self, baseUri):
        self.baseUri = baseUri
        self.deviceKey = 'somesecretkeythattheapponlyknows'
        self.authToken = ''
        self.deviceType = 'STAR:BLUE'


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


try:
    apiClient = QuestApiClient('https://quest.local:8443')
    audioHandler = AudioHandler()
    gpioHandler = GpioHandler(audioHandler, apiClient)
   
    while (not apiClient.register()):
        print ('Device not registered. Retrying in 5s...')
        time.sleep(5)

    print ('Ready')

    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print ("Exiting on user abort\n")

except Exception as e:
    print ("General error occurred\n")
    print (e)

    
finally:
    GPIO.cleanup()

