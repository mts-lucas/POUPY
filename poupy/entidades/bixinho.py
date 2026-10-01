from dataclasses import dataclass
from enum import IntEnum
from random import choice

import pygame

from poupy.constantes import (
    ESCALA_SPRITE_COBRA,
    LADO_SPRITE_COBRA,
    SPRITE_COBRA_DIRTY,
    SPRITE_COBRA_EAT,
    SPRITE_COBRA_HUNGRY,
    SPRITE_COBRA_IDLE,
    SPRITE_COBRA_PET,
    SPRITE_COBRA_SAD,
    SPRITE_COBRA_SCRUB,
    SPRITE_COBRA_WALK,
    ler_imagens,
)

LADO_SPRITE = LADO_SPRITE_COBRA * ESCALA_SPRITE_COBRA
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
    LIMPAR = 7
    FOME = 8
    SUJO = 9
    TRISTE = 10


# ações que substituem o idle quando o bixinho tem alguma carência
ACOES_CARENCIA = (Acao.FOME, Acao.SUJO, Acao.TRISTE)


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
        self.limpando = False
        self.carencias: list[Acao] = []  # preenchida por Jogo a cada frame

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
        def frames(
            inicio: int, fim: int, folha: pygame.Surface, linha: int = 0
        ) -> list[pygame.Surface]:
            quadros = ler_imagens(
                inicio, fim, folha, LADO_SPRITE_COBRA, LADO_SPRITE_COBRA, linha
            )
            return [
                pygame.transform.scale(quadro, (LADO_SPRITE, LADO_SPRITE))
                for quadro in quadros
            ]

        return {
            Acao.PARADO: Animacao(frames(0, 6, SPRITE_COBRA_IDLE), 0.1),
            Acao.BAIXO: Animacao(
                frames(0, 4, SPRITE_COBRA_WALK, 0), 0.1, dy=PASSO_PIXELS, volta_ao_parado=True
            ),
            Acao.ESQUERDA: Animacao(
                frames(0, 4, SPRITE_COBRA_WALK, 1), 0.1,
                dx=-PASSO_PIXELS, segue_y=True, volta_ao_parado=True,
            ),
            Acao.CIMA: Animacao(
                frames(0, 4, SPRITE_COBRA_WALK, 3), 0.2, dy=-PASSO_PIXELS, volta_ao_parado=True
            ),
            Acao.DIREITA: Animacao(
                frames(0, 4, SPRITE_COBRA_WALK, 2), 0.1, dx=PASSO_PIXELS, segue_y=True
            ),
            Acao.AFAGO: Animacao(frames(0, 8, SPRITE_COBRA_PET), 0.1, volta_ao_parado=True),
            Acao.COMER: Animacao(frames(0, 8, SPRITE_COBRA_EAT), 0.1),
            Acao.LIMPAR: Animacao(frames(0, 8, SPRITE_COBRA_SCRUB), 0.15),
            Acao.FOME: Animacao(
                frames(0, 8, SPRITE_COBRA_HUNGRY), 0.1, volta_ao_parado=True
            ),
            Acao.SUJO: Animacao(
                frames(0, 8, SPRITE_COBRA_DIRTY), 0.1, volta_ao_parado=True
            ),
            Acao.TRISTE: Animacao(
                frames(0, 8, SPRITE_COBRA_SAD), 0.1, volta_ao_parado=True
            ),
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
        if self.action in ACOES_CARENCIA and not (self.comendo or self.limpando):
            return  # deixa a animação de carência terminar

        if self.newx != self.rect.x:
            self._andar_em_x()
            self._andar_em_y()

        chegou = self.newx == self.rect.x and self.newy == self.rect.y
        if chegou and not self.mouse_colidindo():
            self.update_action(self._acao_no_destino())

    def _acao_no_destino(self) -> Acao:
        """Ação de quem já chegou ao destino: comer, tomar banho, mostrar uma carência ou ficar parado."""
        if self.comendo:
            return Acao.COMER
        if self.limpando:
            return Acao.LIMPAR
        if self.carencias:
            return choice(self.carencias)
        return Acao.PARADO

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
