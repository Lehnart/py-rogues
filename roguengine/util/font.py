from typing import Dict, Tuple

import pygame


class Font:

    def __init__(
            self,
            char_sprite_sheet: pygame.Surface,
            char_width: int,
            char_height: int,
            map_char_to_xy: Dict[str, Tuple[int, int]],
            font_oc: pygame.Color,
            bkgd_oc: pygame.Color,
            scale: float = 1.
    ):
        self._sheet = char_sprite_sheet
        self._char_width = char_width
        self._char_height = char_height
        self._map_char_to_xy = map_char_to_xy
        self._scale = scale
        self._font_oc = font_oc
        self._bkgd_oc = bkgd_oc

    def get_char_width(self) -> int:
        return int(self._char_width * self._scale)

    def get_char_height(self):
        return int(self._char_height * self._scale)

    def _get_colored_char_sprite(self, char_sprite: pygame.Surface, bkgd_color: pygame.Color, font_color: pygame.Color) -> pygame.Surface:
        bkgd_oc = char_sprite.map_rgb(self._bkgd_oc)
        bkgd_c = char_sprite.map_rgb(bkgd_color)

        font_oc = char_sprite.map_rgb(self._font_oc)
        font_c = char_sprite.map_rgb(font_color)

        pixel_array = pygame.PixelArray(char_sprite)
        pixel_array.replace(bkgd_oc, bkgd_c)
        pixel_array.replace(font_oc, font_c)

        sprite = pixel_array.surface
        return sprite

    def _get_char_sprite(self, px: int, py: int) -> pygame.Surface:
        sprite = self._sheet.subsurface(pygame.Rect(px, py, self._char_width, self._char_height))
        sprite: pygame.Surface = sprite.convert()
        return sprite

    def get_char(self, character: str, font_color: pygame.Color, bkgd_color: pygame.Color) -> pygame.Surface:
        x, y = self._map_char_to_xy[character]
        char_sprite = self._get_char_sprite(x, y)
        scale_dim = (int(char_sprite.get_width() * self._scale), int(char_sprite.get_height() * self._scale))
        char_sprite = pygame.transform.scale(char_sprite, scale_dim)
        return self._get_colored_char_sprite(char_sprite, bkgd_color, font_color)

    def draw_string(self, s: str, x: int, y: int, window_surface: pygame.Surface, font_color: pygame.Color, bkgd_color: pygame.Color):
        for c in s:
            sprite = self.get_char(c, font_color, bkgd_color)
            window_surface.blit(sprite, (x, y))
            x += sprite.get_width()
