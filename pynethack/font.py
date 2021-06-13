import pygame

from roguengine.processor.ui import Font

CHAR_SPRITE_WIDTH = 8
CHAR_SPRITE_HEIGHT = 12
CHAR_SPRITE_SHEET: pygame.Surface = pygame.image.load("res/font_8x12.bmp")

CHAR_POSITIONS = {
    " ": (0, 0),
    '!': (8, 0),
    '\"': (16, 0),
    '#': (24, 0),
    '$': (32, 0),
    '%': (40, 0),
    '&': (48, 0),
    '\'': (56, 0),
    '(': (64, 0),
    ')': (72, 0),
    '*': (80, 0),
    '+': (88, 0),
    ',': (96, 0),
    '-': (104, 0),
    '.': (112, 0),
    '/': (120, 0),
    'a': (8, 48),
    'b': (16, 48),
    'c': (24, 48),
    'd': (32, 48),
    'e': (40, 48),
    'f': (48, 48),
    'g': (56, 48),
    'h': (64, 48),
    'i': (72, 48),
    'j': (80, 48),
    'k': (88, 48),
    'l': (96, 48),
    'm': (104, 48),
    'n': (112, 48),
    'o': (120, 48),
    'p': (0, 60),
    'q': (8, 60),
    'r': (16, 60),
    's': (24, 60),
    't': (32, 60),
    'u': (40, 60),
    'v': (48, 60),
    'w': (56, 60),
    'x': (64, 60),
    'y': (72, 60),
    'z': (80, 60),
    'A': (8, 24),
    'B': (16, 24),
    'C': (24, 24),
    'D': (32, 24),
    'E': (40, 24),
    'F': (48, 24),
    'G': (56, 24),
    'H': (64, 24),
    'I': (72, 24),
    'J': (80, 24),
    'K': (88, 24),
    'L': (96, 24),
    'M': (104, 24),
    'N': (112, 24),
    'O': (120, 24),
    'P': (0, 36),
    'Q': (8, 36),
    'R': (16, 36),
    'S': (24, 36),
    'T': (32, 36),
    'U': (40, 36),
    'V': (48, 36),
    'W': (56, 36),
    'X': (64, 36),
    'Y': (72, 36),
    'Z': (80, 36),
    '0': (0, 12),
    '1': (8, 12),
    '2': (16, 12),
    '3': (24, 12),
    '4': (32, 12),
    '5': (40, 12),
    '6': (48, 12),
    '7': (56, 12),
    '8': (64, 12),
    '9': (72, 12),
    ':': (80, 12),

}

FONT = Font(CHAR_SPRITE_SHEET, CHAR_SPRITE_WIDTH, CHAR_SPRITE_HEIGHT, CHAR_POSITIONS)
