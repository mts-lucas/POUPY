import pygame
from pygame.locals import *
import os
import pickle
# from poupy.entidades.bixinho import Poupy

pygame.init()



def salvar_progresso(fome, limpeza):  # func guardar prog em arquivo
    bixinho = (fome, limpeza)
    arquivo = open('save_bixinho.dat', 'wb')
    pickle.dump(bixinho, arquivo)
    arquivo.close()


def recuperar_progresso(fome, limpeza): # func ler prog em arquivo
    try:
        arquivo = open("save_bixinho.dat", "rb")
        bixinho = pickle.load(arquivo)
        arquivo.close() 
    except:

        arquivo = open("save_bixinho.dat", "wb")
        arquivo.close()
        bixinho = (fome, limpeza)
    
    return bixinho

def ler_imagens(primeiro_numero, segundo_numero, sprite, xsprite, ysprite, linha=0):
    lista_imagens = []
    for i in range(primeiro_numero, segundo_numero):
        img = sprite.subsurface((i * xsprite, linha * ysprite), (xsprite, ysprite))
        lista_imagens.append(img)

    return lista_imagens

def add_sprites_grupo(*sprites):
    spritegroup = pygame.sprite.Group() 
    for sprite in sprites:
        spritegroup.add(sprite)

    return spritegroup



DIRETORIO_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_PRINCIPAL, 'assets', 'sprites')
DIRETORIO_SONS = os.path.join(DIRETORIO_PRINCIPAL, 'assets', 'musica')
LADO_SPRITE_COBRA = 32
ESCALA_SPRITE_COBRA = 4
SPRITE_COBRA_IDLE = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_idle_32x32.png'))
SPRITE_COBRA_WALK = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_walk_32x32.png'))
SPRITE_COBRA_EAT = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_eat_32x32.png'))
SPRITE_COBRA_PET = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_pet_32x32.png'))
SPRITE_COBRA_SCRUB = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_scrub_32x32.png'))
SPRITE_COMIDA = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'carne_mastigada_24x24.png'))
SPRITE_CARNE_PUFT = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'carne_puft_168x24.png'))
SPRITE_OSSO_PUFT = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'osso_puft_168x24.png'))
SPRITE_BUT_COMIDA = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'botao_carne_32x32.png'))
SPRITE_BUT_SABAO = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'botao_sabao_32x32.png'))
SPRITE_SABAO = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'espuma_sabao_24x24.png'))
SPRITE_MOUSE = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'mouse_sprites.png'))
SPRITES_BARRAS = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'barra_vida.png'))
TELA_FUNDO = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'telafundo.png'))


LARGURA_JANELA = 640
ALTURA_JANELA = 480
POSICAO_RELOGIO = (500, 10)
RELOGIO_JOGO = pygame.time.Clock()

#core

PRETO = (0, 0, 0)

#Fontes

FONTE_CS = pygame.font.SysFont("comicsansms", 40, True, True)