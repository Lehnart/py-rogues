from typing import Tuple

import pygame


class LabelComponent:

    def __init__(self, px: int, py: int, label: str, font_color : pygame.Color, bkgd_color : pygame.Color):
        self._px = px
        self._py = py
        self._label = label
        self._font_color = font_color
        self._bkgd_color = bkgd_color

    def get_position(self) -> Tuple[int,int]:
        return self._px, self._py

    def get_label(self) -> str:
        return self._label

    def get_font_color(self) -> pygame.Color:
        return self._font_color

    def get_bkgd_color(self) -> pygame.Color:
        return self._bkgd_color