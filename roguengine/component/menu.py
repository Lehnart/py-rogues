from typing import List, Optional

import pygame


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
