import sys, time
import pygame

try:
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    s=pygame.mixer.Sound('1.wav')

    s.set_volume(0.5)

    while True:
        pygame.mixer.music.pause()
        channel=s.play()
        while pygame.mixer.music.get_busy():
            pass

except KeyboardInterrupt:
    print ("Exiting on user abort\n")

except:
    print ("General error occurred\n")

    
finally:
    print ("Terminating\n")
