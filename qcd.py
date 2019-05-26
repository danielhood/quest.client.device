import sys, time
import requests, json
import RPi.GPIO as GPIO
import pygame

BTN1 = 3
LED1 = 5
LED2 = 7
LED3 = 11
LED4 = 13


class GpioHandler:
    def __init__(self, audioHandler):
        self.buttonState = False
        self.audioHandler = audioHandler

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BTN1, GPIO.IN) # Hardwired PULL UP, so button triggers LOW state
        GPIO.setup(LED1, GPIO.OUT)
        GPIO.setup(LED2, GPIO.OUT)
        GPIO.setup(LED3, GPIO.OUT)
        GPIO.setup(LED4, GPIO.OUT)

        GPIO.add_event_detect(BTN1, GPIO.FALLING)
        GPIO.add_event_callback(BTN1, self.button_pressed)

    def button_pressed(self, channel):
        print('button_pressed() - enter')
    
        self.buttonState = not self.buttonState

        self.audioHandler.PlaySuccess()

        for i in range(1, 32):
            GPIO.output(LED1, (i % 2 == 0))
            GPIO.output(LED2, (i % 3 == 0))
            GPIO.output(LED3, (i % 2 != 0))
            GPIO.output(LED4, (i % 4 == 0))
            time.sleep(0.1)

        
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

    def PlaySuccess(self):
        if not pygame.mixer.music.get_busy():
            self.SoundSuccess.play()


try:
    
    audioHandler = AudioHandler()
    gpioHandler = GpioHandler(audioHandler)
   
    print ('ready')

    while True:
        time.sleep(0.1)


except KeyboardInterrupt:
    print ("Exiting on user abort\n")

except Exception as e:
    print ("General error occurred\n")
    print (e)

    
finally:
    GPIO.cleanup()

