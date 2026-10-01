import math
import os
import sys
from enum import Enum, auto
from random import randint
from typing import Any, Optional

import pygame

from poupy.constantes import (ALTURA_JANELA, COR_SOMBRA_HUD, COR_TEXTO_HUD,
                              DIRETORIO_SONS, FONTE_NOME_HUD, LARGURA_JANELA,
                              PRETO, RELOGIO_JOGO, SPRITE_BARRA_FELICIDADE,
                              SPRITE_BARRA_FOME, SPRITE_BARRA_LIMPEZA,
                              TELA_FUNDO, existe_save, recuperar_progresso,
                              salvar_progresso)
from poupy.entidades.barras import MARCAS_BARRA, Barras
from poupy.entidades.bixinho import Acao, Poupy
from poupy.entidades.botao_comida import AlimentoButton
from poupy.entidades.botao_sabao import SoapButton
from poupy.entidades.comida import LADO_FINAL as LADO_COMIDA
from poupy.entidades.comida import Alimento, EstadoComida
from poupy.entidades.mouse import Hand
from poupy.entidades.sabao import Soap
from poupy.menu import Resultado, TelaMenu, TelaNome

FPS = 60
VOLUME_MUSICA = 0.50
NOME_MUSICA = "BoxCat Games - Young Love.mp3"

# limites e passos dos atributos do bixinho
STATUS_MAXIMO = 150
PASSO_DECAIMENTO = 5
GANHO_COMIDA = 10
GANHO_BANHO = STATUS_MAXIMO / MARCAS_BARRA  # um banho sobe uma marquinha
QTD_ESPUMAS = 1
MAX_CARNES = 3

# camadas de desenho (maior fica na frente)
CAMADA_MUNDO = 0
CAMADA_INTERFACE = 1

# nome do bixinho, acima das barras de status
POSICAO_NOME = (30, 12)
DESLOCAMENTO_SOMBRA_NOME = 2

# posição das barras de status
POSICAO_BARRA_FOME = (30, 44)
POSICAO_BARRA_LIMPEZA = (30, 84)
POSICAO_BARRA_FELICIDADE = (30, 124)

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


class Estado(Enum):
    """Em qual tela o jogo está."""

    MENU = auto()
    NOME = auto()
    JOGANDO = auto()


class Jogo:
    """Controla a janela, os objetos e o game loop do Poupy."""

    def __init__(self) -> None:
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
        pygame.display.set_caption("Poupy")
        pygame.mouse.set_visible(False)
        self.fundo = self._preparar_fundo()
        self.relogio = RELOGIO_JOGO
        self.rodando = True
        self.continua_andando = True
        self.estado = Estado.MENU
        self.bixinho: Optional[Poupy] = None
        self.nome_bixinho = ""

        self._iniciar_musica()
        self.mouse = Hand(pygame.mouse.get_pos())
        self.grupo_cursor = pygame.sprite.Group(self.mouse)
        self.tela_menu = TelaMenu(existe_save())
        self.tela_nome = TelaNome()

    def _preparar_fundo(self) -> pygame.Surface:
        """Escala o fundo até a altura da janela e recorta o centro, sem distorcer."""
        largura, altura = TELA_FUNDO.get_size()
        largura_escalada = largura * ALTURA_JANELA // altura
        escalado = pygame.transform.smoothscale(TELA_FUNDO, (largura_escalada, ALTURA_JANELA))
        recorte = pygame.Rect(0, 0, LARGURA_JANELA, ALTURA_JANELA)
        recorte.centerx = largura_escalada // 2
        return escalado.subsurface(recorte).copy()

    def _iniciar_musica(self) -> None:
        """Carrega e toca a música de fundo em loop."""
        pygame.mixer.music.set_volume(VOLUME_MUSICA)
        pygame.mixer.music.load(os.path.join(DIRETORIO_SONS, NOME_MUSICA))
        pygame.mixer.music.play(-1)

    def _iniciar_partida(self, nome: str, progresso: Optional[dict[str, Any]]) -> None:
        """Cria o bixinho, botões, barras e grupos de sprites e começa a jogar."""
        self.nome_bixinho = nome
        self.nome_hud = self._renderizar_nome(nome)
        self.bixinho = Poupy()
        if progresso is not None:
            self.bixinho.fome = progresso["fome"]
            self.bixinho.limpo = progresso["limpeza"]
        self.botao_comida = AlimentoButton()
        self.botao_sabao = SoapButton()
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

        self.todas_as_sprites = pygame.sprite.LayeredUpdates()
        self.todas_as_sprites.add(self.bixinho, layer=CAMADA_MUNDO)
        self.todas_as_sprites.add(
            self.botao_sabao,
            self.botao_comida,
            self.barra_fome,
            self.barra_felicidade,
            self.barra_limpo,
            layer=CAMADA_INTERFACE,
        )
        self.grupo_sabao = pygame.sprite.Group()

        # carnes ainda não comidas (o osso que sobra não conta)
        self.carnes: list[Alimento] = []

        self.estado = Estado.JOGANDO
        salvar_progresso(nome, self.bixinho.fome, self.bixinho.limpo)

    @staticmethod
    def _renderizar_nome(nome: str) -> pygame.Surface:
        """Renderiza o nome uma única vez, com sombra para ler sobre o fundo."""
        texto = FONTE_NOME_HUD.render(nome, False, COR_TEXTO_HUD)
        sombra = FONTE_NOME_HUD.render(nome, False, COR_SOMBRA_HUD)
        largura, altura = texto.get_size()
        recuo = DESLOCAMENTO_SOMBRA_NOME
        superficie = pygame.Surface((largura + recuo, altura + recuo), pygame.SRCALPHA)
        superficie.blit(sombra, (recuo, recuo))
        superficie.blit(texto, (0, 0))
        return superficie

    # ---------------------------------------------------------------- eventos

    def tratar_eventos(self) -> None:
        """Consome a fila de eventos do pygame e repassa à tela atual."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.sair()
            elif self.estado == Estado.MENU:
                self._tratar_resultado(self.tela_menu.tratar_evento(evento))
            elif self.estado == Estado.NOME:
                self._tratar_resultado(self.tela_nome.tratar_evento(evento))
            else:
                self._tratar_evento_partida(evento)

    def _tratar_resultado(self, resultado: Optional[Resultado]) -> None:
        """Troca de tela conforme a opção escolhida no menu ou na tela do nome."""
        if resultado == Resultado.JOGAR:
            self.estado = Estado.NOME
            pygame.key.start_text_input()
        elif resultado == Resultado.CONTINUAR:
            progresso = recuperar_progresso()
            if progresso is not None:
                self._iniciar_partida(progresso["nome"], progresso)
        elif resultado == Resultado.VOLTAR:
            self.estado = Estado.MENU
            pygame.key.stop_text_input()
        elif resultado == Resultado.CONFIRMAR:
            pygame.key.stop_text_input()
            self._iniciar_partida(self.tela_nome.nome.strip(), None)

    def _tratar_evento_partida(self, evento: pygame.event.Event) -> None:
        """Trata timers do bixinho (andar, fome, limpeza) e cliques do mouse."""
        if evento.type == self.bixinho.timer_andar:
            self._sortear_destino()
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            self._tratar_clique(pygame.mouse.get_pos())
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
        if self.botao_comida.rect.collidepoint(mouse_pos) and len(self.carnes) < MAX_CARNES:
            carne = Alimento(
                randint(CARNE_X_MIN, CARNE_X_MAX), randint(CARNE_Y_MIN, CARNE_Y_MAX)
            )
            self.carnes.append(carne)
            self.todas_as_sprites.add(carne, layer=CAMADA_MUNDO)

        if self.botao_sabao.rect.collidepoint(mouse_pos) and not self.grupo_sabao:
            self._iniciar_banho()

    def _iniciar_banho(self) -> None:
        """Para o bixinho e faz as espumas surgirem girando em volta dele."""
        for i in range(QTD_ESPUMAS):
            espuma = Soap(self.bixinho, 2 * math.pi * i / QTD_ESPUMAS)
            self.todas_as_sprites.add(espuma, layer=CAMADA_MUNDO)
            self.grupo_sabao.add(espuma)
        self.continua_andando = False
        self.bixinho.newx = self.bixinho.rect.x
        self.bixinho.newy = self.bixinho.rect.y

    # ----------------------------------------------------------------- update

    def atualizar(self) -> None:
        """Aplica as regras do jogo e atualiza as sprites da tela atual."""
        self.grupo_cursor.update()
        if self.estado == Estado.MENU:
            self.tela_menu.atualizar()
            return
        if self.estado == Estado.NOME:
            self.tela_nome.atualizar()
            return

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
        """Mantém o bixinho parado durante o banho e premia a limpeza ao fim."""
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
        """Encerra refeições, descarta carnes sumidas e leva o bixinho à carne escolhida."""
        for carne in [c for c in self.carnes if c.foi_comida]:
            self._terminar_refeicao(carne)

        sumiram = [c for c in self.carnes if not c.alive()]
        if sumiram:
            # a carne sumiu (puft) antes de ser comida
            self.carnes = [c for c in self.carnes if c.alive()]
            if not any(c.estado == EstadoComida.SENDO_COMIDA for c in self.carnes):
                self.bixinho.comendo = False
                self.continua_andando = True

        alvo = self._escolher_carne()
        if alvo is None or not self._tem_fome():
            # sem carne à vista ou sem fome, o bixinho não tem interesse
            return

        self.continua_andando = False
        self.bixinho.newx = alvo.rect.x - OFFSET_COMIDA_X
        self.bixinho.newy = alvo.rect.y - OFFSET_COMIDA_Y

        if pygame.sprite.collide_mask(self.bixinho, alvo):
            self.bixinho.newx = self.bixinho.rect.x
            self.bixinho.newy = self.bixinho.rect.y
            self.bixinho.comendo = True
            alvo.sendo_comido()

    def _escolher_carne(self) -> Optional[Alimento]:
        """A carne que está sendo comida ou, senão, a mais próxima do bixinho."""
        no_chao = [c for c in self.carnes if c.comida_no_chao]
        for carne in no_chao:
            if carne.estado == EstadoComida.SENDO_COMIDA:
                return carne
        centro = self.bixinho.rect.center
        return min(
            no_chao,
            key=lambda c: math.dist(centro, c.rect.center),
            default=None,
        )

    def _tem_fome(self) -> bool:
        """O bixinho só se interessa pela carne se a barra de fome não estiver cheia."""
        return not self.barra_fome.cheia

    def _terminar_refeicao(self, carne: Alimento) -> None:
        """Alimenta o bixinho uma única vez quando a carne vira osso."""
        self.bixinho.comendo = False
        self.continua_andando = True
        self.bixinho.fome = min(STATUS_MAXIMO, self.bixinho.fome + GANHO_COMIDA)
        # o osso fica na tela até sumir sozinho, mas já libera espaço para outra carne
        self.carnes.remove(carne)

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
        """Desenha fundo, a tela atual e o cursor por cima de tudo."""
        self.tela.fill(PRETO)
        self.tela.blit(self.fundo, (0, 0))
        if self.estado == Estado.MENU:
            self.tela_menu.desenhar(self.tela)
        elif self.estado == Estado.NOME:
            self.tela_nome.desenhar(self.tela)
        else:
            self.todas_as_sprites.draw(self.tela)
            self.tela.blit(self.nome_hud, POSICAO_NOME)
        self.grupo_cursor.draw(self.tela)
        pygame.display.flip()

    # ------------------------------------------------------------------- loop

    def executar(self) -> None:
        """Roda o game loop: eventos → update → draw → tick."""
        while self.rodando:
            self.tratar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(FPS)

    def sair(self) -> None:
        """Salva o progresso (se a partida começou) e encerra o jogo."""
        if self.bixinho is not None:
            salvar_progresso(self.nome_bixinho, self.bixinho.fome, self.bixinho.limpo)
        pygame.quit()
        sys.exit()
