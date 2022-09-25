import pygame
from pygame.locals import *
from constantes import ler_imagens, SPRITE_COMIDA

pygame.init()

class Alimento(pygame.sprite.Sprite):

    def __init__(self, mouse_pos):
        pygame.sprite.Sprite.__init__(self)
        self.comida_parada = SPRITE_COMIDA.subsurface((0, 0), (32, 32))
        self.sendo_comida = ler_imagens(0, 5, SPRITE_COMIDA, 32, 32)
        self.index_frame_maca = 0
        self.image = self.comida_parada
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.start_comer = False
        self.caindo = False
        self.comida_no_chao = False
        self.foi_comida = False
        self.solto = False
        self.y_solto = None
        self.y_chao = None
        self.sumir = pygame.USEREVENT + 2
        pygame.time.set_timer(self.sumir, 0)
        self.x, self.y = mouse_pos
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def sendo_comido(self):
        self.start_comer = True

    def cair(self):
        self.caindo = True

    def update(self):

        # if self.foi_comida == True:
        #     pygame.time.set_timer(self.sumir, 5000)

        if self.start_comer == True and self.foi_comida == False:
            self.image = self.sendo_comida[int(self.index_frame_maca)]
            self.index_frame_maca += 0.005
            if self.index_frame_maca >= len(self.sendo_comida):
                self.index_frame_maca = 5
                self.foi_comida = True

        if self.caindo == True:
            if self.y_solto >= 300:
                self.comida_no_chao = True
                self.caindo = False
            else:
                self.rect.y += 5

                if self.y_solto >= 200 and self.y_solto < 300:
                    self.y_chao = 380
                    if self.rect.y >= self.y_chao:
                        self.comida_no_chao = True
                        # pygame.time.set_timer(self.sumir, 5000)
                        self.caindo = False

                if self.y_solto >= 100 and self.y_solto < 200:
                    self.y_chao = 330
                    if self.rect.y >= self.y_chao:
                        self.comida_no_chao = True
                        # pygame.time.set_timer(self.sumir, 5000)
                        self.caindo = False
                if self.y_solto >= 0 and self.y_solto < 100:
                    self.y_chao = 290
                    if self.rect.y >= self.y_chao:
                        self.comida_no_chao = True
                        # pygame.time.set_timer(self.sumir, 5000)
                        self.caindo = False

        if self.solto == False:
            if pygame.mouse.get_pressed()[0] == True:
                self.rect.x, self.rect.y = pygame.mouse.get_pos()

            else:
                self.y_solto = self.rect.y
                self.cair()
                self.solto = True

        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
