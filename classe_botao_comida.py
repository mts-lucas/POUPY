import pygame
from pygame.locals import *
from constantes import SPRITE_BUT_COMIDA


pygame.init()

class Alimento_Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_button = SPRITE_BUT_COMIDA.subsurface((0, 0), (64, 64))
        self.botao_clicado = False
        self.image = self.img_button
        self.image = pygame.transform.scale(self.image, (64 + 32, 64 + 32))
        self.x = 112
        self.y = 374
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def update(self):

        self.image = pygame.transform.scale(self.image, (64 + 32, 64 + 32))