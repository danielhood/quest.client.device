import RPi.GPIO as GPIO
import time

PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, GPIO.PUD_UP)

def getByte():
    byte = 0
    timeRisingEdge = 0
    timeFallingEdge = 0
    timeSpan = 0
    for i in range(0, 8):
        GPIO.wait_for_edge(PIN, GPIO.RISING)
        timeRisingEdge = time.time()
        GPIO.wait_for_edge(PIN, GPIO.FALLING)
        timeFallingEdge = time.time()
        timeSpan  = timeFallingEdge - timeRisingEdge

#        print("%d", timeSpan)
        if (timeSpan > 0.0008):
            byte |= 1 << i

    return byte


try:
    print ("ir input test")
    bytes = [0,0,0,0,0,0,0]
    while True:
        for i in range (0,7):
            bytes[i] = getByte()
        print (bytes)
    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()

