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
        #setando os sprites de cada direção
        self.img_stoped = []
        for i in range(43):
            img = sprite_sheet.subsurface((i * 120, 0), (120, 130))
            self.img_stoped.append(img)

        self.img_down = []
        for j in range(3, 13):
            img = sprite_sheet.subsurface((j * 120, 0), (120, 130))
            self.img_down.append(img)
        
        self.img_left = []
        for k in range(13, 23):
            img = sprite_sheet.subsurface((k * 120, 0), (120, 130))
            self.img_left.append(img)
        
        self.img_up = []
        for l in range(23, 33):
            img = sprite_sheet.subsurface((l * 120, 0), (120, 130))
            self.img_up.append(img)
        
        self.img_right = []
        for m in range(33, 44):
            img = sprite_sheet.subsurface((m * 120, 0), (120, 130))
            self.img_right.append(img)

        self.action = 0 # 0: stoped 1:down 2:left 3:up 4:right
        self.index_frame = 0
        self.image = self.img_stoped[self.index_frame]
        self.image = pygame.transform.scale(self.image, (120, 130))
        self.rect = self.image.get_rect()

        self.x = 300
        self.y = 300
        self.rect.center = (self.x, self.y)
        self.andar_d = False
        self.andar_a = False
        self.andar_w = False
        self.andar_s = False

        self.update_time = pygame.time.get_ticks()


    def update(self):
        pass

    def andar_direita(self):
        pass

    def andar_esquerda(self):
        pass

    def andar_cima(self):
        pass

    def andar_baixo(self):
        pass

