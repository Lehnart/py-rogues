from typing import Tuple

import pygame


class SpriteComponent:

    def __init__(self, px: int, py: int, sprite: pygame.Surface, layer: int = 0):
        self._px = px
        self._py = py
        self._sprite = sprite
        self._layer = layer
        self._is_visible = True

    def move(self, dx: int, dy: int):
        self._px += dx * self._sprite.get_width()
        self._py += dy * self._sprite.get_height()

    def set_position(self, x: int, y: int):
        self._px = x * self._sprite.get_width()
        self._py = y * self._sprite.get_height()

    def sprite(self) -> pygame.Surface:
        return self._sprite

    def top_left_pixel_position(self) -> Tuple[int, int]:
        return self._px, self._py

    def layer(self) -> int:
        return self._layer

    def set_layer(self, layer: int):
        self._layer = layer

    def is_visible(self) -> bool:
        return self._is_visible

    def flip(self):
        self._is_visible = not self._is_visible
