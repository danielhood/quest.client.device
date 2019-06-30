import sys
import pygame

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

