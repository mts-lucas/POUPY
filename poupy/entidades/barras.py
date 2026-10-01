import math

import pygame

from poupy.constantes import ler_imagens

LADO_QUADRO_X = 56
LADO_QUADRO_Y = 12
ESCALA = 3
LARGURA_FINAL = LADO_QUADRO_X * ESCALA
ALTURA_FINAL = LADO_QUADRO_Y * ESCALA
QUADROS_BARRA = 9
MARCAS_BARRA = QUADROS_BARRA - 1  # o último quadro é a barra vazia
QUADRO_ALERTA = 5  # a partir do 6º quadro (3 marquinhas) o bixinho reclama


class Barras(pygame.sprite.Sprite):
    """Barra de status: o quadro mostrado depende do valor atual."""

    def __init__(
        self, folha: pygame.Surface, valor: float, maximo: float, posx: int, posy: int
    ) -> None:
        super().__init__()
        quadros = ler_imagens(0, QUADROS_BARRA, folha, LADO_QUADRO_X, LADO_QUADRO_Y)
        self.quadros = [
            pygame.transform.scale(q, (LARGURA_FINAL, ALTURA_FINAL)) for q in quadros
        ]
        self.maximo = maximo
        self.index_frame = 0
        self.image = self.quadros[self.index_frame]
        self.rect = self.image.get_rect(topleft=(posx, posy))
        self.atualizar(valor)

    @property
    def cheia(self) -> bool:
        """True quando a barra mostra todas as marquinhas."""
        return self.index_frame == 0

    @property
    def precisa_atencao(self) -> bool:
        """True quando restam poucas marquinhas."""
        return self.index_frame >= QUADRO_ALERTA

    def atualizar(self, valor: float) -> None:
        """Escolhe o quadro pelo número de marquinhas que o valor ainda preenche."""
        marcas = math.ceil(valor / self.maximo * MARCAS_BARRA)
        marcas = max(0, min(MARCAS_BARRA, marcas))
        self.index_frame = MARCAS_BARRA - marcas
        self.image = self.quadros[self.index_frame]
