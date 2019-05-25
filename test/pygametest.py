import sys, pygame

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.mixer.init()

s=pygame.mixer.Sound('1.wav')

s.set_volume(0.5)

while True:
    pygame.mixer.music.pause()
    channel=s.play()
    while pygame.mixer.music.get_busy():
        pass

