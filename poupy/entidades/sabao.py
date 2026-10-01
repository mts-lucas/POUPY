import math

import pygame

from poupy.constantes import SPRITE_SABAO, ler_imagens

LADO_QUADRO = 24
ESCALA = 3
LADO_FINAL = LADO_QUADRO * ESCALA
QUADROS_SABAO = 6
PRIMEIRO_QUADRO_ESPUMA = 2

# duração fixa do banho (será trocada por outra condição)
DURACAO_BANHO_MS = 4000
DURACAO_QUADRO_MS = 150

# elipse percorrida em volta do centro do bixinho
RAIO_X = 40
RAIO_Y = 25
VOLTAS_POR_SEGUNDO = 0.5


def _carregar_quadros() -> list[pygame.Surface]:
    """Recorta os quadros da folha e já os escala para o tamanho de jogo."""
    quadros = ler_imagens(0, QUADROS_SABAO, SPRITE_SABAO, LADO_QUADRO, LADO_QUADRO)
    return [pygame.transform.scale(q, (LADO_FINAL, LADO_FINAL)) for q in quadros]


class Soap(pygame.sprite.Sprite):
    """Sabão/espuma que surge sozinho e gira em volta do alvo até o banho acabar."""

    def __init__(self, alvo: pygame.sprite.Sprite, fase: float = 0.0) -> None:
        super().__init__()
        self.alvo = alvo
        self.fase = fase
        self.quadros = _carregar_quadros()
        self.inicio = pygame.time.get_ticks()
        self.image = self.quadros[0]
        self.rect = self.image.get_rect(center=alvo.rect.center)
        self._orbitar(0)

    def update(self) -> None:
        decorrido = pygame.time.get_ticks() - self.inicio
        if decorrido >= DURACAO_BANHO_MS:
            self.kill()
            return
        self._animar(decorrido)
        self._orbitar(decorrido)

    def _animar(self, decorrido: int) -> None:
        """Mostra a barra e a espuma crescendo; depois alterna os quadros de espuma."""
        indice = decorrido // DURACAO_QUADRO_MS
        if indice >= QUADROS_SABAO:
            espumas = QUADROS_SABAO - PRIMEIRO_QUADRO_ESPUMA
            indice = PRIMEIRO_QUADRO_ESPUMA + (indice - QUADROS_SABAO) % espumas
        self.image = self.quadros[indice]

    def _orbitar(self, decorrido: int) -> None:
        angulo = self.fase + 2 * math.pi * VOLTAS_POR_SEGUNDO * decorrido / 1000
        centro_x, centro_y = self.alvo.rect.center
        self.rect.center = (
            centro_x + round(math.cos(angulo) * RAIO_X),
            centro_y + round(math.sin(angulo) * RAIO_Y),
        )
