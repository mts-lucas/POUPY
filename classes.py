import pygame
from pygame.locals import *

pygame.init()

#criando a classe do bichinho virtual

class Poupy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite(self)