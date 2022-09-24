import pygame
from pygame.locals import *
from constantes import SPRITE_MOUSE


pygame.init()

class Hand(pygame.sprite.Sprite):
    def __init__(self, mouse_pos):
        pygame.sprite.Sprite.__init__(self)
        self.clicar = False
        self.x, self.y = mouse_pos
        self.x -= 32
        self.normal = SPRITE_MOUSE.subsurface((128, 0), (64, 80))
        self.clicado = SPRITE_MOUSE.subsurface((64, 0), (64, 80))
        self.image = self.normal
        self.image = pygame.transform.scale(self.image, (32, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def update(self):
        if self.clicar == False:
            if pygame.mouse.get_pressed()[0] == True:
                self.image = self.clicado
                self.rect.x, self.rect.y = pygame.mouse.get_pos()
                self.rect.x -= 32
            else:
                self.image = self.normal
                self.rect.x, self.rect.y = pygame.mouse.get_pos()
                self.rect.x -= 32

        self.image = pygame.transform.scale(self.image, (33 * 2, 40 * 2))
