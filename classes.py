import pygame
from pygame.locals import *
import os



pygame.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'sprites')
diretorio_sons = os.path.join(diretorio_principal, 'trilha sonora')
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'link_sprites.png'))

#criando a classe do bichinho virtual

class Poupy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagem_poupy = []
        for i in range(43):
            img = sprite_sheet.subsurface((i * 120, 0), (120, 130))
            self.imagem_poupy.append(img)

        self.index_lista = 0
        self.image = self.imagem_poupy[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (300, 300)
        self.andar_d = False
        self.andar_a = False
        self.andar_w = False
        self.andar_s = False

    def update(self):
        if self.andar_d == True:
            if self.index_lista >= 42:
                self.index_lista = 33
                self.andar_d = False

            self.index_lista += 0.1
        
        else:
            if self.index_lista > 2:
                self.index_lista = 0

            self.index_lista += 0.025
        self.image = self.imagem_poupy[int(self.index_lista)]

    def andar_direita(self):
        self.andar_d = True
        self.index_lista = 33

    def andar_esquerda(self):
        pass

    def andar_cima(self):
        pass

    def andar_baixo(self):
        pass

