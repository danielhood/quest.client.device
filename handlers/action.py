import sys
import time
from handlers import gpio
from handlers import audio
from api import client

class ActionHandler:
    def __init__(self, apiClient, gpioHandler, audioHandler):
        self.apiClient = apiClient
        self.gpioHandler = gpioHandler
        self.audioHandler = audioHandler

    def handle_action(self, key):
        
        if key == 2153839348:
            print ("Hello AARON!!!!")
        elif key == 2178501388:
            print ("Hello ANTHONY!!!")
        else:
            print ("Hello ", key, "???!?")
        
        action = self.apiClient.trigger_player_action(key)

        if action == 'ACTIVATE':
            self.audioHandler.play_activate()
            self.gpioHandler.show_activate()
        elif action == 'NO_QUEST':
            self.audioHandler.play_no_quest()
            self.gpioHandler.show_no_quest()
        else:
            # TODO:
            time.sleep(1)
        
