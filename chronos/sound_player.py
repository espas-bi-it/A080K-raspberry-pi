import os
import pygame
class SoundPlayer: 

    def __init__(self):
        pygame.init()
        pass
    
    def play(self, soundPath):
        pygame.mixer.music.load(soundPath)
        pygame.mixer.music.play()
        pass
