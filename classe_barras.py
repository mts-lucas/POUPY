import pygame
from pygame.locals import *
from constantes import ler_imagens, SPRITES_BARRAS


pygame.init()


class Barras(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_barra = ler_imagens(0, 15, SPRITES_BARRAS, 60, 20)