import pygame
from pygame.locals import *
import os

pygame.init()


def ler_imagens(primeiro_numero, segundo_numero, sprite, xsprite, ysprite):
    lista_imagens = []
    for i in range(primeiro_numero, segundo_numero):
        img = sprite.subsurface((i * xsprite, 0), (xsprite, ysprite))
        lista_imagens.append(img)

    return lista_imagens


DIRETORIO_PRINCIPAL = os.path.dirname(__file__)
DIRETORIO_IMAGENS = os.path.join(diretorio_principal, 'sprites')
DIRETORIO_SONS = os.path.join(diretorio_principal, 'trilha sonora')
SPRITE_SHEET = pygame.image.load(os.path.join(diretorio_imagens, 'link_sprites.png'))
SPRITE_COMIDA = pygame.image.load(os.path.join(diretorio_imagens, 'apple.png'))
SPRITE_BUT_COMIDA = pygame.image.load(os.path.join(diretorio_imagens, 'apple_button.png'))
SPRITE_BUT_SABAO = pygame.image.load(os.path.join(diretorio_imagens, 'botao_sabao.png'))
SPRITE_SABAO = pygame.image.load(os.path.join(diretorio_imagens, 'sabao_sprites.png'))
SPRITE_MOUSE = pygame.image.load(os.path.join(diretorio_imagens, 'mouse_sprites.png'))
SPRITE_AFAGADO = pygame.image.load(os.path.join(diretorio_imagens, 'link_sprites_afago.png'))
