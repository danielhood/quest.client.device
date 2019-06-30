import sys, time

from handlers.gpio import GpioHandler
from handlers.audio import AudioHandler
from api.client import QuestApiClient


apiClient = QuestApiClient('https://quest.local:8443')
audioHandler = AudioHandler()
gpioHandler = GpioHandler(audioHandler, apiClient)

try:
    print ('Ready')

    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print ("Exiting on user abort\n")

except Exception as e:
    print ("General error occurred\n")
    print (e)

    
finally:
    gpioHandler.cleanup()

