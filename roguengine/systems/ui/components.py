import time
from typing import Callable
from typing import List, Optional
from typing import Tuple

import pygame

from roguengine import rogue_esper


class UISpriteComponent:

    def __init__(self, sprite: pygame.Surface):
        self.sprite = sprite


class BlinkingComponent:

    def __init__(self, period: float):
        self._blinking_period = period
        self._last_blinking_time = time.time()
        self._blinking_count = 0

    def get_period(self) -> float:
        return self._blinking_period

    def get_last_blinking_time(self) -> float:
        return self._last_blinking_time

    def get_blinking_count(self) -> int:
        return self._blinking_count

    def blink(self):
        self._last_blinking_time = time.time()
        self._blinking_count += 1


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


class LabelComponent:

    def __init__(
            self,
            px: int,
            py: int,
            label: str,
            font_color: pygame.Color,
            bkgd_color: pygame.Color
    ):
        self._px = px
        self._py = py
        self._label = label
        self._font_color = font_color
        self._bkgd_color = bkgd_color

    def get_position(self) -> Tuple[int, int]:
        return self._px, self._py

    def get_label(self) -> str:
        return self._label

    def get_font_color(self) -> pygame.Color:
        return self._font_color

    def get_bkgd_color(self) -> pygame.Color:
        return self._bkgd_color


class Label:

    def __init__(self, px, py, label: str, font_color: pygame.Color, bkgd_color: pygame.Color):
        self.px = px
        self.py = py
        self.s = label
        self.font_color = font_color
        self.bkgd_color = bkgd_color


class MenuComponent:

    def __init__(
            self,
            px: int,
            py: int,
            y_shift: int,
            labels: List[str],
            font_colors: List[pygame.Color],
            bkgd_colors: List[pygame.Color],
            selected_color: pygame.Color,
            selected_index: Optional[int] = None
    ):
        self._labels = []
        self._selected_color = selected_color
        self._selected_index = selected_index

        x, y = px, py
        for i, label in enumerate(labels):
            self._labels.append(Label(x, y, label, font_colors[i], bkgd_colors[i]))
            y += y_shift

    def get_labels(self) -> List[Label]:
        return self._labels

    def get_selected(self) -> Optional[int]:
        return self._selected_index

    def get_selected_color(self) -> pygame.Color:
        return self._selected_color

    def move_selection(self, dy: int):
        if self._selected_index is None:
            self._selected_index = 0
            return

        self._selected_index += dy
        if self._selected_index >= len(self._labels):
            self._selected_index = 0
            return

        if self._selected_index < 0:
            self._selected_index = len(self._labels) - 1
            return
