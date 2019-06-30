import sys
import pygame

class AudioHandler:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.mixer.init()

        self.SoundActivate = pygame.mixer.Sound('activate.wav')
        self.SoundActivate.set_volume(0.5)

        self.SoundNoQuest = pygame.mixer.Sound('noquest.wav')
        self.SoundNoQuest.set_volume(0.5)

        # TODO: define other sound and light animiation responses

    def play_activate(self):
        if not pygame.mixer.music.get_busy():
            self.SoundActivate.play()

    def play_no_quest(self):
        if not pygame.mixer.music.get_busy():
            self.SoundNoQuest.play()

