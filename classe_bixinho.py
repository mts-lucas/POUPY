import pygame
from pygame.locals import *
from constantes import ler_imagens, SPRITE_SHEET, SPRITE_AFAGADO, SPRITE_COMENDO


pygame.init()


class Poupy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # setando os sprites de cada direção
        self.img_stoped = ler_imagens(0, 3, SPRITE_SHEET, 120, 130)
        self.img_down = ler_imagens(3, 13, SPRITE_SHEET, 120, 130)
        self.img_left = ler_imagens(13, 23, SPRITE_SHEET, 120, 130)
        self.img_up = ler_imagens(23, 33, SPRITE_SHEET, 120, 130)
        self.img_right = ler_imagens(33, 43, SPRITE_SHEET, 120, 130)
        self.img_afago = ler_imagens(0, 3, SPRITE_AFAGADO, 120, 130)
        self.img_comer = ler_imagens(0, 3, SPRITE_COMENDO, 120, 130)
        self.action = 0  # 0: stoped 1:down 2:left 3:up 4:right 5:afago, 6:comer
        self.index_frame = 0
        self.image = self.img_stoped[self.index_frame]
        self.image = pygame.transform.scale(self.image, (120, 130))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        
        #setando a variave de controle do movimento
        self.timer_andar = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_andar, 5000)
        #setando o rect da sprite e gerando a posição inicial
        self.newx = 300
        self.newy = 300
        self.x = 300
        self.y = 300
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        #variaveis de controle
        self.afagado = False
        self.comendo = False

        #parametros de vida
        self.fome = 100
        self.limpo = 100
        self.feliz = (self.fome + self.limpo)/2

        self.descer_fome = pygame.USEREVENT + 4
        pygame.time.set_timer(self.descer_fome, 25000)

        self.descer_limpeza = pygame.USEREVENT + 5
        pygame.time.set_timer(self.descer_limpeza, 25000)

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


        if self.newx == self.rect.x and self.newy == self.rect.y and self.mouse_colidindo() == False:
            if self.comendo == True:
                self.update_action(6)

            else:
                self.update_action(0)

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

        elif self.action == 5:
            # pygame.time.set_timer(self.timer_andar, 0)
            self.image = self.img_afago[int(self.index_frame)]
            self.index_frame += 0.05
            if self.index_frame >= len(self.img_afago):
                self.index_frame = 0
                self.update_action(0)

        elif self.action == 6:
            print("entrou 22")
            # pygame.time.set_timer(self.timer_andar, 0)
            self.image = self.img_comer[int(self.index_frame)]
            self.index_frame += 0.05
            if self.index_frame >= len(self.img_comer):
                self.index_frame = 0

        self.image = pygame.transform.scale(self.image, (120, 130))

    def update_action(self, new_action):
        print(new_action, self.action)
        if new_action != self.action:
            self.action = new_action
            self.index_frame = 0

    def mouse_colidindo(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) == True and pygame.mouse.get_pressed()[0] == True:
            return True
        else:
            return False
