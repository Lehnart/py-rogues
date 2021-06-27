from typing import Tuple, Callable

import pygame

from roguengine import rogue_esper


class DynamicLabelComponent:

    def __init__(self, px: int, py: int, acallable: Callable[[rogue_esper.RogueWorld], str], font_color: pygame.Color, bkgd_color: pygame.Color):
        self._px = px
        self._py = py
        self._font_color = font_color
        self._bkgd_color = bkgd_color
        self._callable = acallable

    def get_position(self) -> Tuple[int, int]:
        return self._px, self._py

    def get_callable(self) -> Callable[[rogue_esper.RogueWorld], str]:
        return self._callable

    def get_font_color(self) -> pygame.Color:
        return self._font_color

    def get_bkgd_color(self) -> pygame.Color:
        return self._bkgd_color
