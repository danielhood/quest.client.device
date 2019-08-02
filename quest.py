import sys, time

from handlers.gpio import GpioHandler
from handlers.audio import AudioHandler
from handlers.action import ActionHandler
from handlers.stdin import StdinHandler
from api.client import QuestApiClient


apiClient = QuestApiClient('https://quest.local:8443')
audioHandler = AudioHandler()
gpioHandler = GpioHandler(audioHandler, apiClient)
actionHandler = ActionHandler(apiClient, gpioHandler, audioHandler)
stdinHandler = StdinHandler(actionHandler)

try:
    print ('Ready')

    stdinHandler.process_input()

    #while True:
    #    time.sleep(0.1)

except KeyboardInterrupt:
    print ("Exiting on user abort\n")

except Exception as e:
    print ("General error occurred\n")
    print (e)

    
finally:
    gpioHandler.cleanup()

