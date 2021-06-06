from typing import Tuple, List

import pygame


class GaugeComponent:

    def __init__(
            self, px: int, py: int, width: int, height: int,
            font_color: pygame.Color,
            bkgd_color_thresholds: List[Tuple[float, pygame.Color]],
            label: str = None
    ):
        self._px = px
        self._py = py
        self._width = width
        self._height = height
        self._label = label
        self._value = 1.
        self._font_color = font_color
        self._color_threshold = bkgd_color_thresholds
