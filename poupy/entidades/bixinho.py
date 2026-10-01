from dataclasses import dataclass
from enum import IntEnum

import pygame

from poupy.constantes import ler_imagens, SPRITE_SHEET, SPRITE_AFAGADO, SPRITE_COMENDO

LARGURA_SPRITE = 120
ALTURA_SPRITE = 130
PASSO_PIXELS = 2
POSICAO_INICIAL = (300, 300)

# faixa de x (relativa ao bixinho) em que ele já pode andar na vertical
MARGEM_ESQUERDA = 120
MARGEM_DIREITA = 240

STATUS_INICIAL = 150.00
INTERVALO_TIMER_MS = 5000


class Acao(IntEnum):
    PARADO = 0
    BAIXO = 1
    ESQUERDA = 2
    CIMA = 3
    DIREITA = 4
    AFAGO = 5
    COMER = 6


@dataclass(frozen=True)
class Animacao:
    """Quadros de uma ação e como ela anda e termina."""
    frames: list[pygame.Surface]
    passo_frame: float
    dx: int = 0
    dy: int = 0
    segue_y: bool = False  # corrige o y rumo ao destino enquanto anda em x
    volta_ao_parado: bool = False  # ao fim do ciclo, volta para PARADO


class Poupy(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.animacoes = self._criar_animacoes()
        self.action = Acao.PARADO
        self.index_frame = 0
        self.image = self.animacoes[Acao.PARADO].frames[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=POSICAO_INICIAL)

        # destino do passeio e variáveis de controle
        self.newx, self.newy = POSICAO_INICIAL
        self.comendo = False

        # parâmetros de vida
        self.fome = STATUS_INICIAL
        self.limpo = STATUS_INICIAL
        self.feliz = (self.fome + self.limpo) // 2

        # eventos de timer tratados em Jogo
        self.timer_andar = pygame.USEREVENT + 1
        self.descer_fome = pygame.USEREVENT + 4
        self.descer_limpeza = pygame.USEREVENT + 5
        for evento in (self.timer_andar, self.descer_fome, self.descer_limpeza):
            pygame.time.set_timer(evento, INTERVALO_TIMER_MS)

    @staticmethod
    def _criar_animacoes() -> dict[Acao, Animacao]:
        def frames(inicio: int, fim: int, folha: pygame.Surface) -> list[pygame.Surface]:
            return ler_imagens(inicio, fim, folha, LARGURA_SPRITE, ALTURA_SPRITE)

        return {
            Acao.PARADO: Animacao(frames(0, 3, SPRITE_SHEET), 0.05),
            Acao.BAIXO: Animacao(
                frames(3, 13, SPRITE_SHEET), 0.2, dy=PASSO_PIXELS, volta_ao_parado=True
            ),
            Acao.ESQUERDA: Animacao(
                frames(13, 23, SPRITE_SHEET), 0.2,
                dx=-PASSO_PIXELS, segue_y=True, volta_ao_parado=True,
            ),
            Acao.CIMA: Animacao(
                frames(23, 33, SPRITE_SHEET), 0.5, dy=-PASSO_PIXELS, volta_ao_parado=True
            ),
            Acao.DIREITA: Animacao(
                frames(33, 43, SPRITE_SHEET), 0.2, dx=PASSO_PIXELS, segue_y=True
            ),
            Acao.AFAGO: Animacao(frames(0, 3, SPRITE_AFAGADO), 0.05, volta_ao_parado=True),
            Acao.COMER: Animacao(frames(0, 3, SPRITE_COMENDO), 0.05),
        }

    def update(self) -> None:
        self._escolher_acao()
        self._animar()
        self.feliz = (self.fome + self.limpo) // 2

    def update_action(self, new_action: Acao) -> None:
        """Troca a ação e reinicia a animação, se for diferente da atual."""
        if new_action != self.action:
            self.action = new_action
            self.index_frame = 0

    def mouse_colidindo(self) -> bool:
        """True se o botão esquerdo está pressionado sobre o bixinho."""
        return (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and pygame.mouse.get_pressed()[0]
        )

    # ------------------------------------------------------------- movimento

    def _escolher_acao(self) -> None:
        """Decide a ação a partir da posição atual e do destino."""
        if self.newx != self.rect.x:
            self._andar_em_x()
            self._andar_em_y()

        chegou = self.newx == self.rect.x and self.newy == self.rect.y
        if chegou and not self.mouse_colidindo():
            self.update_action(Acao.COMER if self.comendo else Acao.PARADO)

    def _andar_em_x(self) -> None:
        """Anda na horizontal; ao alinhar o x, segue na vertical."""
        if self.newx > self.rect.x:
            self.update_action(Acao.DIREITA)
        elif self.newx < self.rect.x:
            self.update_action(Acao.ESQUERDA)
        else:
            return

        if abs(self.newx - self.rect.x) < PASSO_PIXELS:
            self.newx = self.rect.x
        if self.newx == self.rect.x:
            self._virar_para_y()

    def _andar_em_y(self) -> None:
        """Anda na vertical se o destino estiver na faixa de x do bixinho."""
        na_faixa = self.rect.x - MARGEM_ESQUERDA < self.newx < self.rect.x + MARGEM_DIREITA
        if not na_faixa:
            return

        if self.newy < self.rect.y:
            self.update_action(Acao.CIMA)
            perto = abs(self.newy - self.rect.y) < PASSO_PIXELS
        elif self.newy > self.rect.y:
            self.update_action(Acao.BAIXO)
            # mantém o comportamento original: aqui o critério é invertido
            perto = self.newy - self.rect.y > PASSO_PIXELS
        else:
            return

        if perto:
            self.newy = self.rect.y
        if self.newy == self.rect.y:
            self._virar_para_x()

    def _virar_para_y(self) -> None:
        if self.newy > self.rect.y:
            self.update_action(Acao.BAIXO)
        elif self.newy < self.rect.y:
            self.update_action(Acao.CIMA)

    def _virar_para_x(self) -> None:
        if self.newx > self.rect.x:
            self.update_action(Acao.DIREITA)
        elif self.newx < self.rect.x:
            self.update_action(Acao.ESQUERDA)

    # ------------------------------------------------------------- animação

    def _animar(self) -> None:
        """Mostra o quadro atual, anda e avança a animação da ação."""
        animacao = self.animacoes[self.action]
        self.image = animacao.frames[int(self.index_frame)]
        self.index_frame += animacao.passo_frame

        self.rect.x += animacao.dx
        self.rect.y += animacao.dy
        if animacao.segue_y:
            if self.newy < self.rect.y:
                self.rect.y -= PASSO_PIXELS
            if self.newy > self.rect.y:
                self.rect.y += PASSO_PIXELS

        if self.index_frame >= len(animacao.frames):
            self.index_frame = 0
            if animacao.volta_ao_parado:
                self.update_action(Acao.PARADO)
