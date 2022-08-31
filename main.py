import pygame
from pygame.locals import *
from sys import exit
# import os
from classes import Poupy

pygame.init()

# musica de fundo do jogo

pygame.mixer.music.set_volume(0.50)
pygame.mixer.music.load("trilha sonora/BoxCat Games - Young Love.mp3")
pygame.mixer.music.play(-1)

# adcionando diretorios

# diretorio_principal = os.path.dirname(__file__)
# diretorio_imagens = os.path.join(diretorio_principal, 'sprites')
# diretorio_sons = os.path.join(diretorio_principal, 'trilha sonora')
# sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'link_sprites.png'))

# trecho dedicado a janela do jogo

largura_janela = 640
altura_janela = 480

#criando a classe do bixinho:





tela_fundo = pygame.image.load('sprites/telafundo.png')
tela_fundo = pygame.transform.scale(tela_fundo, (largura_janela, altura_janela))

tela_jogo = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("Poupy")
relogio_jogo = pygame.time.Clock()

todas_as_sprites = pygame.sprite.Group()
bixinho = Poupy()
todas_as_sprites.add(bixinho)

while True:

    relogio_jogo.tick(60)  # 30 fps
    tela_jogo.fill((0, 0, 0))  # cor da tela preta

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            exit()


    tela_jogo.blit(tela_fundo, (0, 0))
    todas_as_sprites.draw(tela_jogo)
    todas_as_sprites.update()
    pygame.display.flip()

# Fim do trecho da janela
