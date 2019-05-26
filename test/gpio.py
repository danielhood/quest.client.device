import sys, time
import RPi.GPIO as GPIO

try:
    GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(2, GPIO.IN)
    GPIO.setup(5, GPIO.OUT)
    #GPIO.setup(4, GPIO.OUT)

    GPIO.output(5, True)
    time.sleep(0.5)
    GPIO.output(5, False)
    time.sleep(0.5)
    GPIO.output(5, True)
    time.sleep(0.5)
    GPIO.output(5, False)
    time.sleep(0.5)


except KeyboardInterrupt:
    print ("Exiting on user abort\n")

except:
    print ("General error occurred\n")

    
finally:
    GPIO.cleanup()

