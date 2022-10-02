import pygame
from pygame.locals import *
from sys import exit
from classe_bixinho import Poupy
from classe_mouse import Hand
from classe_comida import Alimento
from classe_botao_comida import Alimento_Button
from classe_botao_sabao import Soap_Button
from classe_sabao import Soap
from classe_barras import Barras
from random import randint
from constantes import ALTURA_JANELA, LARGURA_JANELA, RELOGIO_JOGO

pygame.init()

# musica de fundo do jogo

pygame.mixer.music.set_volume(0.50)
pygame.mixer.music.load("trilha sonora/BoxCat Games - Young Love.mp3")
pygame.mixer.music.play(-1)

tela_fundo = pygame.image.load('sprites/telafundo.png')
tela_fundo = pygame.transform.scale(tela_fundo, (LARGURA_JANELA, ALTURA_JANELA))

tela_jogo = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption("Poupy")

todas_as_sprites = pygame.sprite.Group()
bixinho = Poupy()
botao_comida = Alimento_Button()
botao_sabao = Soap_Button()


barra_fome = Barras(bixinho.fome, 30, 20)
barra_limpo = Barras(bixinho.limpo, 30, 45)
barra_felicidade = Barras(bixinho.feliz, 30, 70)
todas_as_sprites.add(botao_sabao)
todas_as_sprites.add(bixinho)
todas_as_sprites.add(botao_comida)
todas_as_sprites.add(barra_fome)
todas_as_sprites.add(barra_felicidade)
todas_as_sprites.add(barra_limpo)
travar_comida = False
mouse = Hand(pygame.mouse.get_pos())
todas_as_sprites.add(mouse)
sabao_existe = False
comida_existe = False
grupo_sabao = pygame.sprite.Group()
grupo_comida = pygame.sprite.Group()
continua_andando = True

while True:

    mouse_pos = pygame.mouse.get_pos()
    mouse_button1 = pygame.mouse.get_pressed()[0]

    RELOGIO_JOGO.tick(60)  # 60 fps
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
                comida_existe = True

            if event.button == 1 and botao_sabao.rect.collidepoint(mouse_pos):
                sabao = Soap(mouse_pos)
                todas_as_sprites.add(sabao)
                sabao_existe = True

        if event.type == pygame.USEREVENT + 2:
            pygame.time.set_timer(maca.sumir, 0)
            todas_as_sprites.remove(maca)
            comida_existe = False
            del maca
            travar_comida = False

        if event.type == pygame.USEREVENT + 3:
            pygame.time.set_timer(sabao.sumir, 0)
            todas_as_sprites.remove(sabao)
            del sabao
            sabao_existe = False

        if event.type == bixinho.descer_fome:
            if bixinho.fome <= 0:
                bixinho.fome = 0

            else:
                bixinho.fome -= 5

            barra_fome.descer_barra(bixinho.fome)
            barra_felicidade.descer_barra(bixinho.feliz)


        if event.type == bixinho.descer_limpeza:
            if bixinho.limpo <= 0:
                bixinho.limpo = 0
            else:
                bixinho.limpo -= 5  

            barra_limpo.descer_barra(bixinho.limpo)
            barra_felicidade.descer_barra(bixinho.feliz)

        if sabao_existe == True:
            grupo_sabao.add(sabao)
            colisoes = pygame.sprite.spritecollide(bixinho, grupo_sabao, False, pygame.sprite.collide_mask)

            if colisoes:
                sabao.usando = True
                if bixinho.limpo >= 150:
                    bixinho.limpo = 150
                else:
                    bixinho.limpo += 0.5
                    
                barra_limpo.subir_barra(bixinho.limpo)
            else:
                sabao.usando = False

        if comida_existe == True:
            if maca.comida_no_chao == True:
                continua_andando = False
                bixinho.newx = maca.rect.x - 64
                bixinho.newy = maca.rect.y - 66

                grupo_comida.add(maca)
                colisoes2 = pygame.sprite.spritecollide(bixinho, grupo_comida, False, pygame.sprite.collide_mask)

                if colisoes2:
                    bixinho.newx = bixinho.rect.x
                    bixinho.newy = bixinho.rect.y
                    bixinho.comendo = True
                    maca.sendo_comido()
                if maca.foi_comida == True:
                    if bixinho.fome >= 150:

                        bixinho.fome = 150

                    else:
                        bixinho.fome += 10

                    barra_fome.subir_barra(bixinho.fome)
                    pygame.time.set_timer(maca.sumir, 8000)
                    bixinho.comendo = False
                    continua_andando = True
                    comida_existe = False

    if mouse_button1 == True and bixinho.rect.collidepoint(mouse_pos):
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
