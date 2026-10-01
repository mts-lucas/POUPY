from enum import IntEnum

import pygame

from poupy.constantes import (
    SPRITE_CARNE_PUFT,
    SPRITE_COMIDA,
    SPRITE_OSSO_PUFT,
    ler_imagens,
)

LADO_QUADRO = 24
ESCALA = 3
LADO_FINAL = LADO_QUADRO * ESCALA
QUADROS_COMIDA = 6
QUADROS_PUFT = 7

VELOCIDADE_QUEDA = 5
DURACAO_COMER_MS = 4000
DURACAO_PUFT_MS = 500
TEMPO_CARNE_SUMIR_MS = 10000
TEMPO_OSSO_SUMIR_MS = 5000


class EstadoComida(IntEnum):
    """Fases da vida de uma carne, da queda até sumir."""

    CAINDO = 0
    NO_CHAO = 1
    SENDO_COMIDA = 2
    OSSO = 3
    PUFT = 4


def _carregar_quadros(folha: pygame.Surface, quantidade: int) -> list[pygame.Surface]:
    """Recorta os quadros da folha e já os escala para o tamanho de jogo."""
    quadros = ler_imagens(0, quantidade, folha, LADO_QUADRO, LADO_QUADRO)
    return [pygame.transform.scale(q, (LADO_FINAL, LADO_FINAL)) for q in quadros]


class Alimento(pygame.sprite.Sprite):
    """Carne que cai do alto, é comida, vira osso e some com um puft."""

    def __init__(self, x: int, y_chao: int) -> None:
        super().__init__()
        self.quadros_comida = _carregar_quadros(SPRITE_COMIDA, QUADROS_COMIDA)
        self.quadros_puft_carne = _carregar_quadros(SPRITE_CARNE_PUFT, QUADROS_PUFT)
        self.quadros_puft_osso = _carregar_quadros(SPRITE_OSSO_PUFT, QUADROS_PUFT)
        self.quadros_puft = self.quadros_puft_carne

        self.estado = EstadoComida.CAINDO
        self.y_chao = y_chao
        self.inicio_estado = pygame.time.get_ticks()
        self.foi_comida = False

        self._definir_imagem(self.quadros_comida[0])
        self.rect = self.image.get_rect(midtop=(x, -LADO_FINAL))

    @property
    def comida_no_chao(self) -> bool:
        """True quando a carne já pousou e ainda pode ser comida."""
        return self.estado in (EstadoComida.NO_CHAO, EstadoComida.SENDO_COMIDA)

    def sendo_comido(self) -> None:
        """Inicia a mastigação, se a carne estiver parada no chão."""
        if self.estado == EstadoComida.NO_CHAO:
            self._mudar_estado(EstadoComida.SENDO_COMIDA)

    def update(self) -> None:
        """Avança o estado atual da carne conforme o tempo decorrido."""
        agora = pygame.time.get_ticks()
        decorrido = agora - self.inicio_estado

        if self.estado == EstadoComida.CAINDO:
            self._cair()
        elif self.estado == EstadoComida.NO_CHAO:
            if decorrido >= TEMPO_CARNE_SUMIR_MS:
                self._iniciar_puft(self.quadros_puft_carne)
        elif self.estado == EstadoComida.SENDO_COMIDA:
            self._mastigar(decorrido)
        elif self.estado == EstadoComida.OSSO:
            if decorrido >= TEMPO_OSSO_SUMIR_MS:
                self._iniciar_puft(self.quadros_puft_osso)
        elif self.estado == EstadoComida.PUFT:
            self._animar_puft(decorrido)

    def _cair(self) -> None:
        """Desce até o chão e então fica disponível para ser comida."""
        self.rect.y += VELOCIDADE_QUEDA
        if self.rect.y >= self.y_chao:
            self.rect.y = self.y_chao
            self._mudar_estado(EstadoComida.NO_CHAO)

    def _mastigar(self, decorrido: int) -> None:
        """Mostra a carne sendo mordida; ao fim vira osso e conta como comida."""
        progresso = min(decorrido / DURACAO_COMER_MS, 1)
        indice = min(int(progresso * QUADROS_COMIDA), QUADROS_COMIDA - 1)
        self._definir_imagem(self.quadros_comida[indice])
        if progresso >= 1:
            self.foi_comida = True
            self._mudar_estado(EstadoComida.OSSO)

    def _iniciar_puft(self, quadros: list[pygame.Surface]) -> None:
        """Começa a animação de sumir usando os quadros dados."""
        self.quadros_puft = quadros
        self._mudar_estado(EstadoComida.PUFT)

    def _animar_puft(self, decorrido: int) -> None:
        """Toca o puft e remove a sprite quando ele termina."""
        if decorrido >= DURACAO_PUFT_MS:
            self.kill()
            return
        indice = decorrido * len(self.quadros_puft) // DURACAO_PUFT_MS
        self._definir_imagem(self.quadros_puft[indice])

    def _mudar_estado(self, estado: EstadoComida) -> None:
        """Troca o estado e reinicia a contagem de tempo."""
        self.estado = estado
        self.inicio_estado = pygame.time.get_ticks()

    def _definir_imagem(self, imagem: pygame.Surface) -> None:
        """Usa a imagem e atualiza a máscara de colisão."""
        self.image = imagem
        self.mask = pygame.mask.from_surface(imagem)
