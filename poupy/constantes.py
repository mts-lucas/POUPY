import json
import os
from pathlib import Path
from typing import Any, Optional

import pygame
from pygame.locals import *

pygame.init()


def salvar_progresso(nome: str, fome: float, limpeza: float) -> None:
    """Grava nome, fome e limpeza do bixinho no arquivo de save."""
    bixinho = {"nome": nome, "fome": fome, "limpeza": limpeza}
    with open(ARQUIVO_SAVE, "w", encoding="utf-8") as arquivo:
        json.dump(bixinho, arquivo)


def recuperar_progresso() -> Optional[dict[str, Any]]:
    """Lê o save; devolve None se não existir ou se estiver inválido."""
    try:
        with open(ARQUIVO_SAVE, "r", encoding="utf-8") as arquivo:
            bixinho = json.load(arquivo)
        return {
            "nome": str(bixinho["nome"]),
            "fome": float(bixinho["fome"]),
            "limpeza": float(bixinho["limpeza"]),
        }
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        return None


def existe_save() -> bool:
    """True se há um save válido para continuar."""
    return recuperar_progresso() is not None


def ler_imagens(
    primeiro_numero: int,
    segundo_numero: int,
    sprite: pygame.Surface,
    xsprite: int,
    ysprite: int,
    linha: int = 0,
) -> list[pygame.Surface]:
    """Recorta os quadros [primeiro, segundo) de uma linha da folha de sprites."""
    lista_imagens = []
    for i in range(primeiro_numero, segundo_numero):
        img = sprite.subsurface((i * xsprite, linha * ysprite), (xsprite, ysprite))
        lista_imagens.append(img)

    return lista_imagens


DIRETORIO_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_PRINCIPAL, 'assets', 'sprites')
DIRETORIO_SONS = os.path.join(DIRETORIO_PRINCIPAL, 'assets', 'musica')
DIRETORIO_FONTES = os.path.join(DIRETORIO_PRINCIPAL, 'assets', 'fontes')
ARQUIVO_SAVE = Path(DIRETORIO_PRINCIPAL) / 'save_bixinho.json'
LADO_SPRITE_COBRA = 32
ESCALA_SPRITE_COBRA = 4
SPRITE_COBRA_IDLE = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_idle_32x32.png'))
SPRITE_COBRA_WALK = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_walk_32x32.png'))
SPRITE_COBRA_EAT = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_eat_32x32.png'))
SPRITE_COBRA_PET = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_pet_32x32.png'))
SPRITE_COBRA_SCRUB = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_scrub_32x32.png'))
SPRITE_COBRA_HUNGRY = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_hungry_32x32.png'))
SPRITE_COBRA_DIRTY = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_dirty_32x32.png'))
SPRITE_COBRA_SAD = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'cobrinha_sad_32x32.png'))
SPRITE_COMIDA = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'carne_mastigada_24x24.png'))
SPRITE_CARNE_PUFT = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'carne_puft_168x24.png'))
SPRITE_OSSO_PUFT = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'osso_puft_168x24.png'))
SPRITE_BUT_COMIDA = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'botao_carne_32x32.png'))
SPRITE_BUT_SABAO = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'botao_sabao_32x32.png'))
SPRITE_SABAO = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'espuma_sabao_24x24.png'))
LADO_SPRITE_CURSOR = 24
ESCALA_SPRITE_CURSOR = 2
FRAME_CURSOR_NORMAL = 0
FRAME_CURSOR_CLICADO = 4
SPRITE_MOUSE = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'luva_cursor_120x24.png'))
SPRITE_BARRA_FOME = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'barra_fome_504x12.png'))
SPRITE_BARRA_LIMPEZA = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'barra_limpeza_504x12.png'))
SPRITE_BARRA_FELICIDADE = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'barra_felicidade_504x12.png'))
TELA_FUNDO = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'fundo_jardim_1920x1080.png'))
SPRITE_TITULO = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'titulo_poupy_200x43.png'))
SPRITE_PAINEL_NOME = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'painel_nome_200x97.png'))
SPRITE_BOTAO_JOGAR = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'botao_jogar_400x20.png'))
SPRITE_BOTAO_CONTINUAR = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'botao_continuar_400x20.png'))
SPRITE_BOTAO_CONFIRMAR = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'botao_confirmar_384x20.png'))
SPRITE_BOTAO_VOLTAR = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'botao_voltar_288x20.png'))

# fonte pixel art (Press Start 2P) para o nome do bixinho
ARQUIVO_FONTE = os.path.join(DIRETORIO_FONTES, 'PressStart2P-Regular.ttf')
TAMANHO_FONTE_HUD = 16
TAMANHO_FONTE_ENTRADA = 24
FONTE_NOME_HUD = pygame.font.Font(ARQUIVO_FONTE, TAMANHO_FONTE_HUD)
FONTE_NOME_ENTRADA = pygame.font.Font(ARQUIVO_FONTE, TAMANHO_FONTE_ENTRADA)

LARGURA_JANELA = 640
ALTURA_JANELA = 480
RELOGIO_JOGO = pygame.time.Clock()

# cores
PRETO = (0, 0, 0)
COR_TEXTO_HUD = (255, 244, 214)
COR_SOMBRA_HUD = (59, 36, 18)
COR_TEXTO_ENTRADA = (59, 36, 18)
