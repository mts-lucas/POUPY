from enum import Enum, auto
from typing import Optional

import pygame

from poupy.constantes import (
    COR_TEXTO_ENTRADA,
    FONTE_NOME_ENTRADA,
    LARGURA_JANELA,
    SPRITE_BOTAO_CONFIRMAR,
    SPRITE_BOTAO_CONTINUAR,
    SPRITE_BOTAO_JOGAR,
    SPRITE_BOTAO_VOLTAR,
    SPRITE_PAINEL_NOME,
    SPRITE_TITULO,
    ler_imagens,
)

ESCALA = 3
QUADROS_BOTAO = 4
QUADRO_NORMAL = 0
QUADRO_HOVER = 1
QUADRO_PRESSIONADO = 2
QUADRO_DESABILITADO = 3

# menu inicial
TITULO_Y = 40
BOTAO_MENU_CENTRO_Y = 320

# tela do nome
PAINEL_Y = 40
BOTOES_NOME_CENTRO_Y = 380
ESPACO_ENTRE_BOTOES = 24

# caixa branca do painel (x, y, largura, altura) no sprite original
CAIXA_TEXTO = (22, 42, 152, 12)
MARGEM_TEXTO = 6
NOME_MAX = 12
INTERVALO_CURSOR_MS = 500


class Resultado(Enum):
    """O que uma tela pede ao Jogo quando o jogador escolhe uma opção."""

    JOGAR = auto()
    CONTINUAR = auto()
    CONFIRMAR = auto()
    VOLTAR = auto()


def _escalar(imagem: pygame.Surface) -> pygame.Surface:
    """Amplia a imagem pela escala do menu."""
    largura, altura = imagem.get_size()
    return pygame.transform.scale(imagem, (largura * ESCALA, altura * ESCALA))


class Botao(pygame.sprite.Sprite):
    """Botão de 4 quadros: normal, hover, pressionado e desabilitado."""

    def __init__(self, folha: pygame.Surface, centro: tuple[int, int]) -> None:
        super().__init__()
        largura_quadro = folha.get_width() // QUADROS_BOTAO
        quadros = ler_imagens(0, QUADROS_BOTAO, folha, largura_quadro, folha.get_height())
        self.quadros = [_escalar(q) for q in quadros]
        self.habilitado = True
        self.image = self.quadros[QUADRO_NORMAL]
        self.rect = self.image.get_rect(center=centro)

    def clicado(self, pos: tuple[int, int]) -> bool:
        """True se o clique foi sobre o botão e ele está habilitado."""
        return self.habilitado and self.rect.collidepoint(pos)

    def update(self) -> None:
        """Escolhe o quadro conforme o botão esteja desabilitado, sob o mouse ou pressionado."""
        if not self.habilitado:
            quadro = QUADRO_DESABILITADO
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            pressionado = pygame.mouse.get_pressed()[0]
            quadro = QUADRO_PRESSIONADO if pressionado else QUADRO_HOVER
        else:
            quadro = QUADRO_NORMAL
        self.image = self.quadros[quadro]


def _soltou_sobre(evento: pygame.event.Event, botao: Botao) -> bool:
    """True se o botão esquerdo foi solto sobre o botão (habilitado)."""
    return (
        evento.type == pygame.MOUSEBUTTONUP
        and evento.button == 1
        and botao.clicado(evento.pos)
    )


class TelaMenu:
    """Menu inicial: título e um botão (Continuar se há save, senão Jogar)."""

    def __init__(self, tem_save: bool) -> None:
        self.titulo = _escalar(SPRITE_TITULO)
        self.titulo_rect = self.titulo.get_rect(midtop=(LARGURA_JANELA // 2, TITULO_Y))
        self.tem_save = tem_save
        folha = SPRITE_BOTAO_CONTINUAR if tem_save else SPRITE_BOTAO_JOGAR
        self.botao = Botao(folha, (LARGURA_JANELA // 2, BOTAO_MENU_CENTRO_Y))
        self.botoes = pygame.sprite.Group(self.botao)

    def tratar_evento(self, evento: pygame.event.Event) -> Optional[Resultado]:
        """Devolve JOGAR ou CONTINUAR ao clicar no botão ou apertar Enter."""
        if _soltou_sobre(evento, self.botao):
            return Resultado.CONTINUAR if self.tem_save else Resultado.JOGAR
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return Resultado.CONTINUAR if self.tem_save else Resultado.JOGAR
        return None

    def atualizar(self) -> None:
        """Atualiza o quadro do botão."""
        self.botoes.update()

    def desenhar(self, tela: pygame.Surface) -> None:
        """Desenha o título e o botão."""
        tela.blit(self.titulo, self.titulo_rect)
        self.botoes.draw(tela)


class TelaNome:
    """Tela para digitar o nome da criatura."""

    def __init__(self) -> None:
        self.nome = ""
        self.texto = FONTE_NOME_ENTRADA.render("", False, COR_TEXTO_ENTRADA)
        self.cursor = FONTE_NOME_ENTRADA.render("_", False, COR_TEXTO_ENTRADA)
        self.painel = _escalar(SPRITE_PAINEL_NOME)
        self.painel_rect = self.painel.get_rect(midtop=(LARGURA_JANELA // 2, PAINEL_Y))
        x, y, largura, altura = CAIXA_TEXTO
        self.caixa = pygame.Rect(
            self.painel_rect.x + x * ESCALA,
            self.painel_rect.y + y * ESCALA,
            largura * ESCALA,
            altura * ESCALA,
        )

        self.botao_confirmar = Botao(SPRITE_BOTAO_CONFIRMAR, (0, BOTOES_NOME_CENTRO_Y))
        self.botao_voltar = Botao(SPRITE_BOTAO_VOLTAR, (0, BOTOES_NOME_CENTRO_Y))
        total = self.botao_confirmar.rect.width + ESPACO_ENTRE_BOTOES + self.botao_voltar.rect.width
        esquerda = (LARGURA_JANELA - total) // 2
        self.botao_voltar.rect.x = esquerda
        self.botao_confirmar.rect.x = esquerda + self.botao_voltar.rect.width + ESPACO_ENTRE_BOTOES
        self.botoes = pygame.sprite.Group(self.botao_voltar, self.botao_confirmar)
        self._atualizar_nome()

    @property
    def valido(self) -> bool:
        """O nome precisa ter ao menos uma letra além de espaços."""
        return bool(self.nome.strip())

    def _atualizar_nome(self) -> None:
        """Renderiza o texto só quando o nome muda e atualiza o botão Confirmar."""
        self.texto = FONTE_NOME_ENTRADA.render(self.nome, False, COR_TEXTO_ENTRADA)
        self.botao_confirmar.habilitado = self.valido

    def tratar_evento(self, evento: pygame.event.Event) -> Optional[Resultado]:
        """Recebe texto, teclas e cliques; devolve CONFIRMAR ou VOLTAR quando couber."""
        if evento.type == pygame.TEXTINPUT:
            self._digitar(evento.text)
        elif evento.type == pygame.KEYDOWN:
            return self._tratar_tecla(evento.key)
        elif _soltou_sobre(evento, self.botao_confirmar):
            return Resultado.CONFIRMAR
        elif _soltou_sobre(evento, self.botao_voltar):
            return Resultado.VOLTAR
        return None

    def _tratar_tecla(self, tecla: int) -> Optional[Resultado]:
        """Backspace apaga, Enter confirma (se válido) e Esc volta."""
        if tecla == pygame.K_BACKSPACE:
            self.nome = self.nome[:-1]
            self._atualizar_nome()
        elif tecla in (pygame.K_RETURN, pygame.K_KP_ENTER) and self.valido:
            return Resultado.CONFIRMAR
        elif tecla == pygame.K_ESCAPE:
            return Resultado.VOLTAR
        return None

    def _digitar(self, texto: str) -> None:
        """Acrescenta os caracteres imprimíveis, respeitando o limite do nome."""
        for caractere in texto:
            if caractere.isprintable() and len(self.nome) < NOME_MAX:
                self.nome += caractere
        self._atualizar_nome()

    def atualizar(self) -> None:
        """Atualiza o quadro dos botões."""
        self.botoes.update()

    def desenhar(self, tela: pygame.Surface) -> None:
        """Desenha o painel, o nome digitado e os botões."""
        tela.blit(self.painel, self.painel_rect)
        self._desenhar_texto(tela)
        self.botoes.draw(tela)

    def _desenhar_texto(self, tela: pygame.Surface) -> None:
        """Escreve o nome dentro da caixa, com cursor piscante ao final."""
        destino = self.texto.get_rect(midleft=(self.caixa.x + MARGEM_TEXTO, self.caixa.centery))
        tela.blit(self.texto, destino)
        if (pygame.time.get_ticks() // INTERVALO_CURSOR_MS) % 2 == 0:
            tela.blit(self.cursor, self.cursor.get_rect(midleft=(destino.right, self.caixa.centery)))
