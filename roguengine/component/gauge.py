from typing import Tuple, List, Callable

import pygame

from roguengine import rogue_esper


class GaugeComponent:

    def __init__(
            self,
            px: int,
            py: int,
            width: int,
            height: int,
            font_color: pygame.Color,
            bkgd_color_thresholds: List[Tuple[float, pygame.Color]],
            value_function: Callable[[rogue_esper.RogueWorld], float],
            value_max_function: Callable[[rogue_esper.RogueWorld], float],
            label: str
    ):
        self.px = px
        self.py = py
        self.width = width
        self.height = height
        self.label = label
        self.value_function = value_function
        self.value_max_function = value_max_function
        self.font_color = font_color
        self.color_threshold = bkgd_color_thresholds
