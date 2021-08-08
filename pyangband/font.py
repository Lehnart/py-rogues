import pygame

from roguengine.util.font import Font

CHAR_SPRITE_WIDTH = 16
CHAR_SPRITE_HEIGHT = 16
CHAR_SPRITE_SHEET: pygame.Surface = pygame.image.load("res/font_16x16.bmp")

CHAR_POSITIONS = {
    " ": (0, 32),
    '!': (16, 32),
    '\"': (32, 32),
    '#': (48, 32),
    '$': (64, 32),
    '%': (80, 32),
    '&': (96, 32),
    '\'': (112, 32),
    '(': (128, 32),
    ')': (144, 32),
    '*': (160, 32),
    '+': (176, 32),
    ',': (192, 32),
    '-': (208, 32),
    '.': (224, 32),
    '/': (240, 32),
    'a': (16, 96),
    'b': (32, 96),
    'c': (48, 96),
    'd': (64, 96),
    'e': (80, 96),
    'f': (96, 96),
    'g': (112, 96),
    'h': (128, 96),
    'i': (144, 96),
    'j': (160, 96),
    'k': (176, 96),
    'l': (192, 96),
    'm': (208, 96),
    'n': (224, 96),
    'o': (240, 96),
    'p': (0, 112),
    'q': (16, 112),
    'r': (32, 112),
    's': (48, 112),
    't': (64, 112),
    'u': (80, 112),
    'v': (96, 112),
    'w': (112, 112),
    'x': (128, 112),
    'y': (144, 112),
    'z': (160, 112),
    'A': (16, 64),
    'B': (32, 64),
    'C': (48, 64),
    'D': (64, 64),
    'E': (80, 64),
    'F': (96, 64),
    'G': (112, 64),
    'H': (128, 64),
    'I': (144, 64),
    'J': (160, 64),
    'K': (176, 64),
    'L': (192, 64),
    'M': (208, 64),
    'N': (224, 64),
    'O': (240, 64),
    'P': (0, 80),
    'Q': (16, 80),
    'R': (32, 80),
    'S': (48, 80),
    'T': (64, 80),
    'U': (80, 80),
    'V': (96, 80),
    'W': (112, 80),
    'X': (128, 80),
    'Y': (144, 80),
    'Z': (160, 80),
    '[': (244, 80),
    '\\': (192, 80),
    ']': (228, 80),
    '0': (0, 48),
    '1': (16, 48),
    '2': (32, 48),
    '3': (48, 48),
    '4': (64, 48),
    '5': (80, 48),
    '6': (96, 48),
    '7': (112, 48),
    '8': (128, 48),
    '9': (144, 48),
    ':': (160, 48),
    '=': (208, 48),
    '?': (240, 48),
}

FONT = Font(CHAR_SPRITE_SHEET, CHAR_SPRITE_WIDTH, CHAR_SPRITE_HEIGHT, CHAR_POSITIONS, pygame.Color(254, 254, 254), pygame.Color(255, 0, 255))
