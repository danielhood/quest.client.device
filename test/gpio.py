import sys, time
import RPi.GPIO as GPIO

BTN1 = 3
LED1 = 5
LED2 = 7
LED3 = 11
LED4 = 13


class ButtonHandler:
    def __init__(self):
        self.buttonState = False

    def button_pressed(self, channel):
        print('button pressed')
    
        self.buttonState = not self.buttonState

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

        print ('button pressed - exit')



try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BTN1, GPIO.IN) # Hardwired PULL UP, so button triggers LOW state
    GPIO.setup(LED1, GPIO.OUT)
    GPIO.setup(LED2, GPIO.OUT)
    GPIO.setup(LED3, GPIO.OUT)
    GPIO.setup(LED4, GPIO.OUT)
    
    bh = ButtonHandler()

    GPIO.add_event_detect(BTN1, GPIO.FALLING)
    GPIO.add_event_callback(BTN1, bh.button_pressed)

    print ('ready')

    while True:
        
        #GPIO.output(LED1, GPIO.input(BTN1))
        #time.sleep(0.5)
        #GPIO.output(LED1, False)
        #time.sleep(0.5)
        #if GPIO.event_detected(BTN1):
        #    print ("detected button")

        time.sleep(0.1)




except KeyboardInterrupt:
    print ("Exiting on user abort\n")

except Exception as e:
    print ("General error occurred\n")
    print (e)

    
finally:
    GPIO.cleanup()

