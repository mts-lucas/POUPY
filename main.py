import pygame
from pygame.locals import *
from sys import exit
from classe_bixinho import Poupy
from classe_mouse import Hand
from classe_comida import Alimento
from classe_botao_comida import Alimento_Button
from classe_botao_sabao import Soap_Button
from classe_sabao import Soap
from random import randint
from constantes import ALTURA_JANELA, LARGURA_JANELA

pygame.init()

# musica de fundo do jogo

pygame.mixer.music.set_volume(0.50)
pygame.mixer.music.load("trilha sonora/BoxCat Games - Young Love.mp3")
pygame.mixer.music.play(-1)

tela_fundo = pygame.image.load('sprites/telafundo.png')
tela_fundo = pygame.transform.scale(
    tela_fundo, (LARGURA_JANELA, ALTURA_JANELA))

tela_jogo = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
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
continua_andando = True

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

        if continua_andando == True:
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
        print("entrou")
        continua_andando = False
        bixinho.update_action(5)
        bixinho.newx = bixinho.rect.x
        bixinho.newy = bixinho.rect.y

    if bixinho.action == 0:
        continua_andando = True


    tela_jogo.blit(tela_fundo, (0, 0))
    todas_as_sprites.draw(tela_jogo)
    todas_as_sprites.update()
    pygame.display.flip()

# Fim do trecho da janela
