import pygame
from pygame.locals import *
from constantes import ler_imagens, SPRITES_BARRAS

pygame.init()


class Barras(pygame.sprite.Sprite):

    def __init__(self, parametro, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.img_barra = ler_imagens(0, 15, SPRITES_BARRAS, 60, 20)
        self.estado_atual = parametro
        self.index_frame = 0
        self.image = self.img_barra[self.index_frame]
        self.image = pygame.transform.scale(self.image, (60, 20))
        self.x = posx
        self.y = posy
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def update(self):

        self.image = self.img_barra[int(self.index_frame)]
        self.image = pygame.transform.scale(self.image, (60, 20))

    def descer_barra(self, estado):
        if estado == (self.estado_atual - 10) and self.index_frame < 15:
            self.index_frame += 1
            self.estado_atual = estado

    def subir_barra(self, estado):
        if estado == (self.estado_atual + 10) and self.index_frame > 0:
            self.index_frame -= 1
            self.estado_atual = estado

            

