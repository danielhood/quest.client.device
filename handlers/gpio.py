import time
import RPi.GPIO as GPIO
from handlers import audio
from api import client

BTN1 = 3
LED1 = 5
LED2 = 7
LED3 = 11
LED4 = 13

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

    def cleanup(self):
        GPIO.cleanup()

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

