import pygame
from poupy.constantes import (
    ESCALA_SPRITE_CURSOR,
    FRAME_CURSOR_CLICADO,
    FRAME_CURSOR_NORMAL,
    LADO_SPRITE_CURSOR,
    SPRITE_MOUSE,
)


pygame.init()

LADO_CURSOR_ESCALADO = LADO_SPRITE_CURSOR * ESCALA_SPRITE_CURSOR
DESLOCAMENTO_X_CURSOR = LADO_CURSOR_ESCALADO // 2


def _carregar_frame(indice: int) -> pygame.Surface:
    """Recorta um frame da luva e o escala uma única vez."""
    frame = SPRITE_MOUSE.subsurface(
        (indice * LADO_SPRITE_CURSOR, 0), (LADO_SPRITE_CURSOR, LADO_SPRITE_CURSOR)
    )
    return pygame.transform.scale(frame, (LADO_CURSOR_ESCALADO, LADO_CURSOR_ESCALADO))


class Hand(pygame.sprite.Sprite):
    """Cursor em forma de luva que segue o mouse e fecha ao clicar."""

    def __init__(self, mouse_pos: tuple[int, int]) -> None:
        super().__init__()
        self.normal = _carregar_frame(FRAME_CURSOR_NORMAL)
        self.clicado = _carregar_frame(FRAME_CURSOR_CLICADO)
        self.image = self.normal
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self._seguir_mouse(mouse_pos)

    def _seguir_mouse(self, mouse_pos: tuple[int, int]) -> None:
        self.rect.x = mouse_pos[0] - DESLOCAMENTO_X_CURSOR
        self.rect.y = mouse_pos[1]

    def update(self) -> None:
        pressionado = pygame.mouse.get_pressed()[0]
        self.image = self.clicado if pressionado else self.normal
        self._seguir_mouse(pygame.mouse.get_pos())
