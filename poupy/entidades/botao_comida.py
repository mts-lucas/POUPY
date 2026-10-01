import pygame

from poupy.constantes import SPRITE_BUT_COMIDA, ler_imagens

LADO_QUADRO = 32
ESCALA = 3
LADO_FINAL = LADO_QUADRO * ESCALA
QUADROS_BOTAO = 4
QUADRO_NORMAL = 0
QUADRO_PRESSIONADO = 3
POSICAO_BOTAO = (112, 374)


class Alimento_Button(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        quadros = ler_imagens(0, QUADROS_BOTAO, SPRITE_BUT_COMIDA, LADO_QUADRO, LADO_QUADRO)
        self.quadros = [
            pygame.transform.scale(q, (LADO_FINAL, LADO_FINAL)) for q in quadros
        ]
        self.image = self.quadros[QUADRO_NORMAL]
        self.rect = self.image.get_rect(topleft=POSICAO_BOTAO)

    def update(self) -> None:
        """Mostra o quadro pressionado enquanto o mouse segura o botão."""
        pressionado = (
            pygame.mouse.get_pressed()[0]
            and self.rect.collidepoint(pygame.mouse.get_pos())
        )
        self.image = self.quadros[QUADRO_PRESSIONADO if pressionado else QUADRO_NORMAL]
