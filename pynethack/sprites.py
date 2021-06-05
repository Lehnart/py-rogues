from typing import Dict

import pygame

pygame.init()

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 16
SPRITE_SHEET: pygame.Surface = pygame.image.load("res/tileset.bmp")


def get_sprite(px: int, py: int) -> pygame.Surface:
    sprite = SPRITE_SHEET.subsurface(pygame.Rect(px, py, SPRITE_WIDTH, SPRITE_HEIGHT))
    return sprite


CHAR_SPRITE_WIDTH = 4
CHAR_SPRITE_HEIGHT = 8
CHAR_SPRITE_SHEET: pygame.Surface = pygame.image.load("res/font.bmp")

SPRITE_DICT = {
    "player": get_sprite(576, 128),
    "vwall": get_sprite(176, 336),
    "hwall": get_sprite(192, 336),
    "twall": get_sprite(208, 336),
    "bwall": get_sprite(240, 336),
    "ground": get_sprite(464, 336),
    "invisible_ground": get_sprite(480, 336),
    "corridor": get_sprite(496, 336),
    "door": get_sprite(400, 336),
    "vdoor_open": get_sprite(384, 336),
    "hdoor_open": get_sprite(368, 336),
}


def get_char_sprite(px: int, py: int, bkgd_color: pygame.Color, font_color: pygame.Color) -> pygame.Surface:
    sprite = CHAR_SPRITE_SHEET.subsurface(pygame.Rect(px, py, CHAR_SPRITE_WIDTH, CHAR_SPRITE_HEIGHT))
    sprite: pygame.Surface = sprite.convert()

    bkgd_oc = sprite.map_rgb(pygame.Color(255, 255, 255))
    bkgd_c = sprite.map_rgb(bkgd_color)

    font_oc = sprite.map_rgb(pygame.Color(0, 0, 0))
    font_c = sprite.map_rgb(font_color)

    pixel_array = pygame.PixelArray(sprite)
    pixel_array.replace(bkgd_oc, bkgd_c)
    pixel_array.replace(font_oc, font_c)

    sprite = pixel_array.surface
    return sprite


def get_char_sprite_dict(font_color : pygame.Color, bkgd_color: pygame.Color) -> Dict[str, pygame.Surface]:
    return {
        'a': get_char_sprite(4, 16, font_color, bkgd_color),
        'b': get_char_sprite(8, 16, font_color, bkgd_color),
        'c': get_char_sprite(12, 16, font_color, bkgd_color),
        'd': get_char_sprite(16, 16, font_color, bkgd_color),
        'e': get_char_sprite(20, 16, font_color, bkgd_color),
        'f': get_char_sprite(24, 16, font_color, bkgd_color),
        'g': get_char_sprite(28, 16, font_color, bkgd_color),
        'h': get_char_sprite(32, 16, font_color, bkgd_color),
        'i': get_char_sprite(36, 16, font_color, bkgd_color),
        'j': get_char_sprite(40, 16, font_color, bkgd_color),
        'k': get_char_sprite(44, 16, font_color, bkgd_color),
        'l': get_char_sprite(48, 16, font_color, bkgd_color),
        'm': get_char_sprite(52, 16, font_color, bkgd_color),
        'n': get_char_sprite(56, 16, font_color, bkgd_color),
        'o': get_char_sprite(60, 16, font_color, bkgd_color),
        'p': get_char_sprite(64, 16, font_color, bkgd_color),
        'q': get_char_sprite(68, 16, font_color, bkgd_color),
        'r': get_char_sprite(72, 16, font_color, bkgd_color),
        's': get_char_sprite(76, 16, font_color, bkgd_color),
        't': get_char_sprite(80, 16, font_color, bkgd_color),
        'u': get_char_sprite(84, 16, font_color, bkgd_color),
        'v': get_char_sprite(88, 16, font_color, bkgd_color),
        'w': get_char_sprite(92, 16, font_color, bkgd_color),
        'x': get_char_sprite(96, 16, font_color, bkgd_color),
        'y': get_char_sprite(100, 16, font_color, bkgd_color),
        'z': get_char_sprite(104, 16, font_color, bkgd_color),
        'A': get_char_sprite(4, 8, font_color, bkgd_color),
        'B': get_char_sprite(8, 8, font_color, bkgd_color),
        'C': get_char_sprite(12, 8, font_color, bkgd_color),
        'D': get_char_sprite(16, 8, font_color, bkgd_color),
        'E': get_char_sprite(20, 8, font_color, bkgd_color),
        'F': get_char_sprite(24, 8, font_color, bkgd_color),
        'G': get_char_sprite(28, 8, font_color, bkgd_color),
        'H': get_char_sprite(32, 8, font_color, bkgd_color),
        'I': get_char_sprite(36, 8, font_color, bkgd_color),
        'J': get_char_sprite(40, 8, font_color, bkgd_color),
        'K': get_char_sprite(44, 8, font_color, bkgd_color),
        'L': get_char_sprite(48, 8, font_color, bkgd_color),
        'M': get_char_sprite(52, 8, font_color, bkgd_color),
        'N': get_char_sprite(56, 8, font_color, bkgd_color),
        'O': get_char_sprite(60, 8, font_color, bkgd_color),
        'P': get_char_sprite(64, 8, font_color, bkgd_color),
        'Q': get_char_sprite(68, 8, font_color, bkgd_color),
        'R': get_char_sprite(72, 8, font_color, bkgd_color),
        'S': get_char_sprite(76, 8, font_color, bkgd_color),
        'T': get_char_sprite(80, 8, font_color, bkgd_color),
        'U': get_char_sprite(84, 8, font_color, bkgd_color),
        'V': get_char_sprite(88, 8, font_color, bkgd_color),
        'W': get_char_sprite(92, 8, font_color, bkgd_color),
        'X': get_char_sprite(96, 8, font_color, bkgd_color),
        'Y': get_char_sprite(100, 8, font_color, bkgd_color),
        'Z': get_char_sprite(104, 8, font_color, bkgd_color),
        # '0': get_sprite(1 * 8, 15, 8, 8, color),
        # '1': get_sprite(2 * 8, 15, 8, 8, color),
        # '2': get_sprite(3 * 8, 15, 8, 8, color),
        # '3': get_sprite(4 * 8, 15, 8, 8, color),
        # '4': get_sprite(5 * 8, 15, 8, 8, color),
        # '5': get_sprite(6 * 8, 15, 8, 8, color),
        # '6': get_sprite(7 * 8, 15, 8, 8, color),
        # '7': get_sprite(8 * 8, 15, 8, 8, color),
        # '8': get_sprite(9 * 8, 15, 8, 8, color),
        # '9': get_sprite(10 * 8, 15, 8, 8, color),
        # '.': get_sprite(11 * 8, 15, 8, 8, color),
        # ',': get_sprite(12 * 8, 15, 8, 8, color),
        # ';': get_sprite(13 * 8, 15, 8, 8, color),
        # ':': get_sprite(14 * 8, 15, 8, 8, color),
        # '-': get_sprite(15 * 8, 15, 8, 8, color),
        # '+': get_sprite(16 * 8, 15, 8, 8, color),
        # '*': get_sprite(17 * 8, 15, 8, 8, color),
        # '/': get_sprite(18 * 8, 15, 8, 8, color),
        # '%': get_sprite(19 * 8, 15, 8, 8, color),
        # '<': get_sprite(20 * 8, 15, 8, 8, color),
        # '>': get_sprite(21 * 8, 15, 8, 8, color),
        # '!': get_sprite(22 * 8, 15, 8, 8, color),
        # '?': get_sprite(23 * 8, 15, 8, 8, color),
        # '^': get_sprite(25 * 8, 15, 8, 8, color),
        # '[': get_sprite(26 * 8, 15, 8, 8, color),
        # ']': get_sprite(27 * 8, 15, 8, 8, color),
        # '(': get_sprite(28 * 8, 15, 8, 8, color),
        # ')': get_sprite(29 * 8, 15, 8, 8, color),
        # '{': get_sprite(30 * 8, 15, 8, 8, color),
        # '#': get_sprite(32 * 8, 15, 8, 8, color),
        # '&': get_sprite(33 * 8, 15, 8, 8, color),
        # '=': get_sprite(34 * 8, 15, 8, 8, color),
        # '\"': get_sprite(35 * 8, 15, 8, 8, color),
        # '\'': get_sprite(36 * 8, 15, 8, 8, color),
        # '@': get_sprite(37 * 8, 15, 8, 8, color),
        # '|': get_sprite(38 * 8, 15, 8, 8, color),
        # '\\': get_sprite(39 * 8, 15, 8, 8, color),
        # '_': get_sprite(42 * 8, 15, 8, 8, color),
        # '~': get_sprite(43 * 8, 15, 8, 8, color),
        # '$': get_sprite(44 * 8, 15, 8, 8, color),
        # ' ': get_sprite(0, 0, 8, 8, color),
    }
