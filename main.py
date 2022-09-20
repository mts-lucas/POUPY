import pygame
from pygame.locals import *
from sys import exit
# import os
from classes import Hand, Poupy, Alimento, Alimento_Button, Soap, Soap_Button
from random import randint

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


tela_fundo = pygame.image.load('sprites/telafundo.png')
tela_fundo = pygame.transform.scale(
    tela_fundo, (largura_janela, altura_janela))

tela_jogo = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("Poupy")
relogio_jogo = pygame.time.Clock()

todas_as_sprites = pygame.sprite.Group()
bixinho = Poupy()
botao_comida = Alimento_Button()
botao_sabao = Soap_Button()
todas_as_sprites.add(botao_sabao)
todas_as_sprites.add(bixinho)
todas_as_sprites.add(botao_comida)
travar_comida = False
mouse = Hand(pygame.mouse.get_pos())
todas_as_sprites.add(mouse)
sabao_existe = False
grupo_sabao = pygame.sprite.Group()

while True:

    mouse_pos = pygame.mouse.get_pos()
    mouse_button1 = pygame.mouse.get_pressed()[0]

    relogio_jogo.tick(60)  # 30 fps
    tela_jogo.fill((0, 0, 0))  # cor da tela preta
    pygame.mouse.set_visible(False)

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == bixinho.timer_andar:
            bixinho.newx = randint(0, 520)
            bixinho.newy = randint(200, 350)

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and botao_comida.rect.collidepoint(mouse_pos) and travar_comida == False:
                maca = Alimento(mouse_pos)
                todas_as_sprites.add(maca)
                travar_comida = True

            if event.button == 1 and botao_sabao.rect.collidepoint(mouse_pos):
                sabao = Soap(mouse_pos)
                todas_as_sprites.add(sabao)
                sabao_existe = True

            # if event.button == 1 and bixinho.rect.collidepoint(mouse_pos):
            #     bixinho.update_action(5)
                

        if event.type == pygame.USEREVENT + 2:
            pygame.time.set_timer(maca.sumir, 0)
            todas_as_sprites.remove(maca)
            del maca
            travar_comida = False

        if event.type == pygame.USEREVENT + 3:
            pygame.time.set_timer(sabao.sumir, 0)
            todas_as_sprites.remove(sabao)
            del sabao
            sabao_existe = False

        if sabao_existe == True:
            grupo_sabao.add(sabao)
            colisoes = pygame.sprite.spritecollide(
            bixinho, grupo_sabao, False, pygame.sprite.collide_mask)

            if colisoes:
                sabao.usando = True
            else:
                sabao.usando = False

    if mouse_button1 == True and bixinho.rect.collidepoint(mouse_pos):
        bixinho.update_action(5)

    if bixinho.rect.x > largura_janela - 120:
        bixinho.rect.x = largura_janela - 120
    if bixinho.rect.x < 0:
        bixinho.rect.x = 0
    if bixinho.rect.y < 200:
        bixinho.rect.y = 200
    if bixinho.rect.y > altura_janela - 130:
        bixinho.rect.y = altura_janela - 130

    tela_jogo.blit(tela_fundo, (0, 0))
    todas_as_sprites.draw(tela_jogo)
    todas_as_sprites.update()
    pygame.display.flip()

# Fim do trecho da janela
