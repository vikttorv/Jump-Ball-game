import pygame
from pygame import mixer
# Создание звукового сопровождения.
def music():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.mixer.init()
    sound = pygame.mixer.Sound('Angel.ogx')
    sound.play(-1)
