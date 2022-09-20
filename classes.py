from pickletools import pyfloat
import pygame
from pygame.locals import *
import os
# from random import randint


pygame.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'sprites')
diretorio_sons = os.path.join(diretorio_principal, 'trilha sonora')
sprite_sheet = pygame.image.load(
    os.path.join(diretorio_imagens, 'link_sprites.png'))
sprite_comida = pygame.image.load(os.path.join(diretorio_imagens, 'apple.png'))
sprite_but_comida = pygame.image.load(
    os.path.join(diretorio_imagens, 'apple_button.png'))
sprite_but_sabao = pygame.image.load(
    os.path.join(diretorio_imagens, 'botao_sabao.png'))
sprite_sabao = pygame.image.load(os.path.join(
    diretorio_imagens, 'sabao_sprites.png'))
sprite_mouse = pygame.image.load(os.path.join(
    diretorio_imagens, 'mouse_sprites.png'))
sprite_afagado = pygame.image.load(os.path.join(
    diretorio_imagens, 'link_sprites_afago.png'))

# criando a classe do bichinho virtual


class Poupy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # setando os sprites de cada direção
        self.img_stoped = []
        for i in range(3):
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
        for m in range(33, 43):
            img = sprite_sheet.subsurface((m * 120, 0), (120, 130))
            self.img_right.append(img)

        self.img_afago = []
        for n in range(3):
            img = sprite_afagado.subsurface((n * 120, 0), (120, 130))
            self.img_afago.append(img)

        self.action = 0  # 0: stoped 1:down 2:left 3:up 4:right 5:afago
        self.index_frame = 0
        self.image = self.img_stoped[self.index_frame]
        self.image = pygame.transform.scale(self.image, (120, 130))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.timer_andar = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_andar, 5000)
        self.newx = 300
        self.newy = 300
        self.x = 300
        self.y = 300
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.afagado = False

    def update(self):

        if self.newx != self.rect.x:
            if self.newx > self.rect.x:
                self.update_action(4)
                if (self.rect.x + 2) > self.newx:
                    self.newx = self.rect.x
                if self.newx == self.rect.x and self.newy != self.rect.y:
                    if self.newy > self.rect.y:
                        self.update_action(1)
                    elif self.newy < self.rect.y:
                        self.update_action(3)

            if self.newx < self.rect.x:
                self.update_action(2)
                if (self.rect.x - 2) < self.newx:
                    self.newx = self.rect.x
                if self.newx == self.rect.x and self.newy != self.rect.y:
                    if self.newy > self.rect.y:
                        self.update_action(1)
                    elif self.newy < self.rect.y:
                        self.update_action(3)

            if self.newy < self.rect.y and self.newx < self.rect.x + 240 and self.newx > self.rect.x - 120:
                self.update_action(3)
                if (self.rect.y - 2) < self.newy:
                    self.newy = self.rect.y
                if self.newy == self.rect.y and self.newx != self.rect.x:
                    if self.newx > self.rect.x:
                        self.update_action(4)
                    elif self.newx < self.rect.x:
                        self.update_action(2)

            if self.newy > self.rect.y and self.newx < self.rect.x + 240 and self.newx > self.rect.x - 120:
                self.update_action(1)
                if (self.rect.y + 2) < self.newy:
                    self.newy = self.rect.y
                if self.newy == self.rect.y and self.newx != self.rect.x:
                    if self.newx > self.rect.x:
                        self.update_action(4)
                    elif self.newx < self.rect.x:
                        self.update_action(2)

        if self.newx == self.rect.x and self.newy == self.rect.y:
            self.update_action(0)

 # ERRO AQUI

        if self.action == 0:
            self.image = self.img_stoped[int(self.index_frame)]
            self.index_frame += 0.05
            if self.index_frame >= len(self.img_stoped):
                self.index_frame = 0

        elif self.action == 1:
            self.image = self.img_down[int(self.index_frame)]
            self.index_frame += 0.2
            self.rect.y += 2
            if self.index_frame >= len(self.img_down):
                self.index_frame = 0
                self.update_action(0)

        elif self.action == 2:
            self.image = self.img_left[int(self.index_frame)]
            self.index_frame += 0.2
            self.rect.x -= 2
            if self.newy < self.rect.y:
                self.rect.y -= 2
            if self.newy > self.rect.y:
                self.rect.y += 2
            if self.index_frame >= len(self.img_left):
                self.index_frame = 0
                self.update_action(0)

        elif self.action == 3:
            self.image = self.img_up[int(self.index_frame)]
            self.index_frame += 0.5
            self.rect.y -= 2
            if self.index_frame >= len(self.img_up):
                self.index_frame = 0
                self.update_action(0)

        elif self.action == 4:
            self.image = self.img_right[int(self.index_frame)]
            self.index_frame += 0.2
            self.rect.x += 2
            if self.newy < self.rect.y:
                self.rect.y -= 2
            if self.newy > self.rect.y:
                self.rect.y += 2
            if self.index_frame >= len(self.img_right):
                self.index_frame = 0
                self.update_action(0)


# ERRO AQUI

        elif self.action == 5:
            pygame.time.set_timer(self.timer_andar, 0)
            print("entrou 22")
            self.image = self.img_afago[int(self.index_frame)]
            self.index_frame += 0.05
            if self.index_frame >= len(self.img_afago):
                self.index_frame = 0
                self.update_action(0)

        self.image = pygame.transform.scale(self.image, (120, 130))

    def update_action(self, new_action):
        print(new_action, self.action)
        if new_action != self.action:
            self.action = new_action
            self.index_frame = 0


class Alimento(pygame.sprite.Sprite):

    def __init__(self, mouse_pos):
        pygame.sprite.Sprite.__init__(self)
        self.comida_parada = sprite_comida.subsurface((0, 0), (32, 32))
        self.sendo_comida = []
        for i in range(0, 5):
            img = sprite_comida.subsurface((i * 32, 0), (32, 32))
            self.sendo_comida.append(img)
        self.index_frame_maca = 0
        self.image = self.comida_parada
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.start_comer = False
        self.caindo = False
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
        if self.start_comer == True:
            self.image = self.sendo_comida[int(self.index_frame_maca)]
            self.index_frame_maca += 0.05
            if self.index_frame_maca >= len(self.sendo_comida):
                self.index_frame_maca = 5

        if self.caindo == True:
            if self.y_solto >= 300:
                self.caindo = False
            else:
                self.rect.y += 5

                if self.y_solto >= 200 and self.y_solto < 300:
                    self.y_chao = 380
                    if self.rect.y >= self.y_chao:
                        pygame.time.set_timer(self.sumir, 5000)
                        self.caindo = False

                if self.y_solto >= 100 and self.y_solto < 200:
                    self.y_chao = 330
                    if self.rect.y >= self.y_chao:
                        pygame.time.set_timer(self.sumir, 5000)
                        self.caindo = False
                if self.y_solto >= 0 and self.y_solto < 100:
                    self.y_chao = 290
                    if self.rect.y >= self.y_chao:
                        pygame.time.set_timer(self.sumir, 5000)
                        self.caindo = False

        if self.solto == False:
            if pygame.mouse.get_pressed()[0] == True:
                self.rect.x, self.rect.y = pygame.mouse.get_pos()

            else:
                self.y_solto = self.rect.y
                self.cair()
                self.solto = True

        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))


class Alimento_Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_button = sprite_but_comida.subsurface((0, 0), (64, 64))
        self.botao_clicado = False
        self.image = self.img_button
        self.image = pygame.transform.scale(self.image, (64 + 32, 64 + 32))
        self.x = 112
        self.y = 374
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def update(self):

        self.image = pygame.transform.scale(self.image, (64 + 32, 64 + 32))


class Soap_Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_button = sprite_but_sabao.subsurface((0, 0), (64, 64))
        self.botao_clicado = False
        self.botao_clicado = False
        self.image = self.img_button
        self.image = pygame.transform.scale(self.image, (64 + 32, 64 + 32))
        self.x = 432
        self.y = 374
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def update(self):

        self.image = pygame.transform.scale(self.image, (64 + 32, 64 + 32))


class Soap(pygame.sprite.Sprite):
    def __init__(self, mouse_pos):
        pygame.sprite.Sprite.__init__(self)
        self.sabao_usado = []
        for i in range(0, 5):
            img = sprite_sabao.subsurface((i * 64, 0), (64, 64))
            self.sabao_usado.append(img)
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


class Hand(pygame.sprite.Sprite):
    def __init__(self, mouse_pos):
        pygame.sprite.Sprite.__init__(self)
        self.clicar = False
        self.x, self.y = mouse_pos
        self.x -= 32
        self.normal = sprite_mouse.subsurface((128, 0), (64, 80))
        self.clicado = sprite_mouse.subsurface((64, 0), (64, 80))
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
