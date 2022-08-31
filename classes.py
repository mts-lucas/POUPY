import pygame
from pygame.locals import *
import os



pygame.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'sprites')
diretorio_sons = os.path.join(diretorio_principal, 'trilha sonora')
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'link_sprites.png')).convert_alpha()

#criando a classe do bichinho virtual

class Poupy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite(self)
        self.imagem_poupy = []
        for i in range():
            img = 
        self.img = sprite_sheet.subsurface((0,0), (120, 130))

    
    def andar(self):
        pass
