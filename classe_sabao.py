import pygame
from pygame.locals import *
from constantes import ler_imagens, SPRITE_SABAO


pygame.init()


class Soap(pygame.sprite.Sprite):
    def __init__(self, mouse_pos):
        pygame.sprite.Sprite.__init__(self)
        self.sabao_usado = ler_imagens(0, 5, SPRITE_SABAO, 64, 64)
        self.index_frame_sabao = 0
        self.image = self.sabao_usado[self.index_frame_sabao]
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.solto = False
        self.usando = False
        self.sumir = pygame.USEREVENT + 3
        pygame.time.set_timer(self.sumir, 0)

        self.x, self.y = mouse_pos
        self.x -= 32
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def update(self):

        if self.solto == False:
            if pygame.mouse.get_pressed()[0] == True:
                self.rect.x, self.rect.y = pygame.mouse.get_pos()
                self.rect.x -= 32
                if self.usando == True:
                    self.image = self.sabao_usado[int(self.index_frame_sabao)]
                    self.index_frame_sabao += 0.1
                    if self.index_frame_sabao >= len(self.sabao_usado):
                        self.index_frame_sabao = 0

                else:
                    self.index_frame_sabao = 0

            else:
                pygame.time.set_timer(self.sumir, 100)
                self.solto = True

        self.image = pygame.transform.scale(self.image, (64 + 32, 64 + 32))
