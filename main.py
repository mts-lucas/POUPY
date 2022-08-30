import pygame
from pygame.locals import *
from sys import exit

pygame.init()

#musica de fundo do jogo

pygame.mixer.music.set_volume(0.50)
pygame.mixer.music.load("trilha sonora/BoxCat Games - Young Love.mp3")
pygame.mixer.music.play(-1)

# trecho dedicado a janela do jogo

largura_janela = 640
altura_janela = 480


tela_fundo = pygame.image.load('telafundo.png1').convert()
tela_fundo = pygame.transform.scale(tela_fundo, (largura_janela, altura_janela))
tela_jogo = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("Poupy")
relogio_jogo = pygame.time.Clock()

while True:

    relogio_jogo.tick(60)  # 30 fps
    tela_jogo.fill((0, 0, 0))  # cor da tela preta

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            exit()

    tela_jogo.blit(tela_fundo, (0, 0))
    pygame.display.flip()

#Fim do trecho da janela