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
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_PRINCIPAL, 'sprites')
DIRETORIO_SONS = os.path.join(DIRETORIO_PRINCIPAL, 'trilha sonora')
SPRITE_SHEET = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'link_sprites.png'))
SPRITE_COMIDA = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'apple.png'))
SPRITE_BUT_COMIDA = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'apple_button.png'))
SPRITE_BUT_SABAO = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'botao_sabao.png'))
SPRITE_SABAO = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'sabao_sprites.png'))
SPRITE_MOUSE = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'mouse_sprites.png'))
SPRITE_AFAGADO = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'link_sprites_afago.png'))
SPRITE_COMENDO = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'link_sprites_comendo.png'))
SPRITES_BARRAS = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'barra_vida.png'))


LARGURA_JANELA = 640
ALTURA_JANELA = 480
RELOGIO_JOGO = pygame.time.Clock()

#core

PRETO = (0, 0, 0)