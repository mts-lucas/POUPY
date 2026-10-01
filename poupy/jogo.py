import math
import os
import sys
from datetime import datetime
from random import randint
from typing import Optional

import pygame

from poupy.constantes import (
    ALTURA_JANELA,
    DIRETORIO_SONS,
    FONTE_CS,
    LARGURA_JANELA,
    POSICAO_RELOGIO,
    PRETO,
    RELOGIO_JOGO,
    SPRITE_BARRA_FELICIDADE,
    SPRITE_BARRA_FOME,
    SPRITE_BARRA_LIMPEZA,
    TELA_FUNDO,
    add_sprites_grupo,
    recuperar_progresso,
    salvar_progresso,
)
from poupy.entidades.barras import MARCAS_BARRA, Barras
from poupy.entidades.bixinho import Acao, Poupy
from poupy.entidades.botao_comida import Alimento_Button
from poupy.entidades.botao_sabao import Soap_Button
from poupy.entidades.comida import LADO_FINAL as LADO_COMIDA, Alimento
from poupy.entidades.mouse import Hand
from poupy.entidades.sabao import Soap

FPS = 60
VOLUME_MUSICA = 0.50
BRANCO = (255, 255, 255)
NOME_MUSICA = "BoxCat Games - Young Love.mp3"

# limites e passos dos atributos do bixinho
STATUS_MAXIMO = 150
PASSO_DECAIMENTO = 5
GANHO_COMIDA = 10
GANHO_BANHO = STATUS_MAXIMO / MARCAS_BARRA  # um banho sobe uma marquinha
QTD_ESPUMAS = 1

# posição das barras de status
POSICAO_BARRA_FOME = (30, 20)
POSICAO_BARRA_LIMPEZA = (30, 60)
POSICAO_BARRA_FELICIDADE = (30, 100)

# area onde o bixinho caminha
ANDAR_X_MAX = 520
ANDAR_Y_MIN = 200
ANDAR_Y_MAX = 350

# deslocamento para o bixinho parar ao lado da comida
OFFSET_COMIDA_X = 64
OFFSET_COMIDA_Y = 66

# onde a carne pode pousar (centro em x, topo em y), alcançável pelo bixinho
CARNE_X_MIN = OFFSET_COMIDA_X + LADO_COMIDA // 2
CARNE_X_MAX = ANDAR_X_MAX + OFFSET_COMIDA_X + LADO_COMIDA // 2
CARNE_Y_MIN = ANDAR_Y_MIN + OFFSET_COMIDA_Y
CARNE_Y_MAX = ANDAR_Y_MAX + OFFSET_COMIDA_Y


class Jogo:
    """Controla a janela, os objetos e o game loop do Poupy."""

    def __init__(self) -> None:
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
        pygame.display.set_caption("Poupy")
        pygame.mouse.set_visible(False)
        self.fundo = pygame.transform.scale(TELA_FUNDO, (LARGURA_JANELA, ALTURA_JANELA))
        self.relogio = RELOGIO_JOGO
        self.rodando = True
        self.continua_andando = True

        self._iniciar_musica()
        self._criar_objetos()

    def _iniciar_musica(self) -> None:
        """Carrega e toca a música de fundo em loop."""
        pygame.mixer.music.set_volume(VOLUME_MUSICA)
        pygame.mixer.music.load(os.path.join(DIRETORIO_SONS, NOME_MUSICA))
        pygame.mixer.music.play(-1)

    def _criar_objetos(self) -> None:
        """Cria o bixinho, botões, barras, mouse e grupos de sprites."""
        self.bixinho = Poupy()
        self.bixinho.fome, self.bixinho.limpo = recuperar_progresso(
            self.bixinho.fome, self.bixinho.limpo
        )
        self.botao_comida = Alimento_Button()
        self.botao_sabao = Soap_Button()
        self.barra_fome = Barras(
            SPRITE_BARRA_FOME, self.bixinho.fome, STATUS_MAXIMO, *POSICAO_BARRA_FOME
        )
        self.barra_limpo = Barras(
            SPRITE_BARRA_LIMPEZA, self.bixinho.limpo, STATUS_MAXIMO, *POSICAO_BARRA_LIMPEZA
        )
        self.barra_felicidade = Barras(
            SPRITE_BARRA_FELICIDADE,
            self.bixinho.feliz,
            STATUS_MAXIMO,
            *POSICAO_BARRA_FELICIDADE,
        )
        self.mouse = Hand(pygame.mouse.get_pos())

        self.todas_as_sprites = add_sprites_grupo(
            self.botao_sabao,
            self.bixinho,
            self.botao_comida,
            self.barra_fome,
            self.barra_felicidade,
            self.barra_limpo,
            self.mouse,
        )
        self.grupo_sabao = pygame.sprite.Group()
        self.grupo_comida = pygame.sprite.Group()

        # itens que existem apenas enquanto estão em uso
        self.maca: Optional[Alimento] = None

    # ---------------------------------------------------------------- eventos

    def tratar_eventos(self) -> None:
        """Consome a fila de eventos do pygame."""
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.sair()
            elif evento.type == self.bixinho.timer_andar:
                self._sortear_destino()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                self._tratar_clique(mouse_pos)
            elif evento.type == self.bixinho.descer_fome:
                self.bixinho.fome = max(0, self.bixinho.fome - PASSO_DECAIMENTO)
            elif evento.type == self.bixinho.descer_limpeza:
                self.bixinho.limpo = max(0, self.bixinho.limpo - PASSO_DECAIMENTO)

    def _sortear_destino(self) -> None:
        """Sorteia um novo ponto para o bixinho andar."""
        if self.continua_andando:
            self.bixinho.newx = randint(0, ANDAR_X_MAX)
            self.bixinho.newy = randint(ANDAR_Y_MIN, ANDAR_Y_MAX)

    def _tratar_clique(self, mouse_pos: tuple[int, int]) -> None:
        """Faz cair uma carne ou inicia o banho quando o botão correspondente é clicado."""
        if self.botao_comida.rect.collidepoint(mouse_pos) and self.maca is None:
            self.maca = Alimento(
                randint(CARNE_X_MIN, CARNE_X_MAX), randint(CARNE_Y_MIN, CARNE_Y_MAX)
            )
            self.todas_as_sprites.add(self.maca)
            self.grupo_comida.add(self.maca)

        if self.botao_sabao.rect.collidepoint(mouse_pos) and not self.grupo_sabao:
            self._iniciar_banho()

    def _iniciar_banho(self) -> None:
        """Para o bixinho e faz as espumas surgirem girando em volta dele."""
        for i in range(QTD_ESPUMAS):
            espuma = Soap(self.bixinho, 2 * math.pi * i / QTD_ESPUMAS)
            self.todas_as_sprites.add(espuma)
            self.grupo_sabao.add(espuma)
        self.continua_andando = False
        self.bixinho.newx = self.bixinho.rect.x
        self.bixinho.newy = self.bixinho.rect.y

    # ----------------------------------------------------------------- update

    def atualizar(self) -> None:
        """Aplica as regras do jogo e atualiza as sprites."""
        self._atualizar_sabao()
        self._atualizar_comida()
        self._atualizar_carinho()
        self.todas_as_sprites.update()
        self._atualizar_barras()

    def _atualizar_barras(self) -> None:
        """Ajusta o quadro de cada barra ao valor atual do bixinho."""
        self.barra_fome.atualizar(self.bixinho.fome)
        self.barra_limpo.atualizar(self.bixinho.limpo)
        self.barra_felicidade.atualizar(self.bixinho.feliz)
        self.bixinho.carencias = [
            acao
            for barra, acao in (
                (self.barra_fome, Acao.FOME),
                (self.barra_limpo, Acao.SUJO),
                (self.barra_felicidade, Acao.TRISTE),
            )
            if barra.precisa_atencao
        ]

    def _atualizar_sabao(self) -> None:
        if not self.grupo_sabao:
            if self.bixinho.limpando:
                # banho acabou: sobe uma marquinha e libera o bixinho para passear
                self.bixinho.limpando = False
                self.continua_andando = True
                self.bixinho.limpo = min(STATUS_MAXIMO, self.bixinho.limpo + GANHO_BANHO)
            return

        self.continua_andando = False
        self.bixinho.limpando = True

    def _atualizar_comida(self) -> None:
        if self.maca is None:
            return

        if not self.maca.alive():
            # a carne/osso sumiu (puft): libera o bixinho para passear
            self.maca = None
            self.bixinho.comendo = False
            self.continua_andando = True
            return

        if self.maca.foi_comida:
            self._terminar_refeicao()
            return

        if not self.maca.comida_no_chao or not self._tem_fome():
            # sem fome, o bixinho não tem interesse na carne
            return

        self.continua_andando = False
        self.bixinho.newx = self.maca.rect.x - OFFSET_COMIDA_X
        self.bixinho.newy = self.maca.rect.y - OFFSET_COMIDA_Y

        colisoes = pygame.sprite.spritecollide(
            self.bixinho, self.grupo_comida, False, pygame.sprite.collide_mask
        )
        if colisoes:
            self.bixinho.newx = self.bixinho.rect.x
            self.bixinho.newy = self.bixinho.rect.y
            self.bixinho.comendo = True
            self.maca.sendo_comido()

    def _tem_fome(self) -> bool:
        """O bixinho só se interessa pela carne se a barra de fome não estiver cheia."""
        return not self.barra_fome.cheia

    def _terminar_refeicao(self) -> None:
        """Alimenta o bixinho uma única vez quando a carne vira osso."""
        self.bixinho.comendo = False
        self.continua_andando = True
        if self.maca in self.grupo_comida:
            self.bixinho.fome = min(STATUS_MAXIMO, self.bixinho.fome + GANHO_COMIDA)
            # o osso fica na tela mas não alimenta de novo
            self.grupo_comida.remove(self.maca)

    def _atualizar_carinho(self) -> None:
        """Para o bixinho e toca a animação de afago ao ser segurado."""
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.bixinho.rect.collidepoint(mouse_pos):
            self.continua_andando = False
            self.bixinho.update_action(Acao.AFAGO)
            self.bixinho.newx = self.bixinho.rect.x
            self.bixinho.newy = self.bixinho.rect.y

        if self.bixinho.action == Acao.PARADO:
            self.continua_andando = True

    # ------------------------------------------------------------------- draw

    def desenhar(self) -> None:
        """Desenha fundo, relógio e sprites na tela."""
        self.tela.fill(PRETO)
        self.tela.blit(self.fundo, (0, 0))
        self.tela.blit(self._renderizar_hora(), POSICAO_RELOGIO)
        self.todas_as_sprites.draw(self.tela)
        pygame.display.flip()

    def _renderizar_hora(self) -> pygame.Surface:
        hora_em_texto = datetime.now().strftime("%H:%M")
        return FONTE_CS.render(hora_em_texto, True, BRANCO)

    # ------------------------------------------------------------------- loop

    def executar(self) -> None:
        """Roda o game loop: eventos → update → draw → tick."""
        while self.rodando:
            self.tratar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(FPS)

    def sair(self) -> None:
        """Salva o progresso e encerra o jogo."""
        salvar_progresso(self.bixinho.fome, self.bixinho.limpo)
        pygame.quit()
        sys.exit()
