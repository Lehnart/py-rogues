import pygame

from roguengine.processor.ui import Font

CHAR_SPRITE_WIDTH = 8
CHAR_SPRITE_HEIGHT = 8
CHAR_SPRITE_SHEET: pygame.Surface = pygame.image.load("res/sprites.bmp")

CHAR_POSITIONS = {
    'a': (27 * 8, 7),
    'b': (28 * 8, 7),
    'c': (29 * 8, 7),
    'd': (30 * 8, 7),
    'e': (31 * 8, 7),
    'f': (32 * 8, 7),
    'g': (33 * 8, 7),
    'h': (34 * 8, 7),
    'i': (35 * 8, 7),
    'j': (36 * 8, 7),
    'k': (37 * 8, 7),
    'l': (38 * 8, 7),
    'm': (39 * 8, 7),
    'n': (40 * 8, 7),
    'o': (41 * 8, 7),
    'p': (42 * 8, 7),
    'q': (43 * 8, 7),
    'r': (44 * 8, 7),
    's': (45 * 8, 7),
    't': (46 * 8, 7),
    'u': (47 * 8, 7),
    'v': (48 * 8, 7),
    'w': (49 * 8, 7),
    'x': (50 * 8, 7),
    'y': (51 * 8, 7),
    'z': (52 * 8, 7),
    'A': (1 * 8, 7),
    'B': (2 * 8, 7),
    'C': (3 * 8, 7),
    'D': (4 * 8, 7),
    'E': (5 * 8, 7),
    'F': (6 * 8, 7),
    'G': (7 * 8, 7),
    'H': (8 * 8, 7),
    'I': (9 * 8, 7),
    'J': (10 * 8, 7),
    'K': (11 * 8, 7),
    'L': (12 * 8, 7),
    'M': (13 * 8, 7),
    'N': (14 * 8, 7),
    'O': (15 * 8, 7),
    'P': (16 * 8, 7),
    'Q': (17 * 8, 7),
    'R': (18 * 8, 7),
    'S': (19 * 8, 7),
    'T': (20 * 8, 7),
    'U': (21 * 8, 7),
    'V': (22 * 8, 7),
    'W': (23 * 8, 7),
    'X': (24 * 8, 7),
    'Y': (25 * 8, 7),
    'Z': (26 * 8, 7),
    '0': (1 * 8, 15),
    '1': (2 * 8, 15),
    '2': (3 * 8, 15),
    '3': (4 * 8, 15),
    '4': (5 * 8, 15),
    '5': (6 * 8, 15),
    '6': (7 * 8, 15),
    '7': (8 * 8, 15),
    '8': (9 * 8, 15),
    '9': (10 * 8, 15),
    '.': (11 * 8, 15),
    ',': (12 * 8, 15),
    ';': (13 * 8, 15),
    ':': (14 * 8, 15),
    '-': (15 * 8, 15),
    '+': (16 * 8, 15),
    '*': (17 * 8, 15),
    '/': (18 * 8, 15),
    '%': (19 * 8, 15),
    '<': (20 * 8, 15),
    '>': (21 * 8, 15),
    '!': (22 * 8, 15),
    '?': (23 * 8, 15),
    '^': (25 * 8, 15),
    '[': (26 * 8, 15),
    ']': (27 * 8, 15),
    '(': (28 * 8, 15),
    ')': (29 * 8, 15),
    '{': (30 * 8, 15),
    '#': (32 * 8, 15),
    '&': (33 * 8, 15),
    '=': (34 * 8, 15),
    '\"': (35 * 8, 15),
    '\'': (36 * 8, 15),
    '@': (37 * 8, 15),
    '|': (38 * 8, 15),
    '\\': (39 * 8, 15),
    '_': (42 * 8, 15),
    '~': (43 * 8, 15),
    '$': (44 * 8, 15),
    ' ': (0, 0)
}

FONT = Font(CHAR_SPRITE_SHEET, CHAR_SPRITE_WIDTH, CHAR_SPRITE_HEIGHT, CHAR_POSITIONS, pygame.Color(239, 239, 239), pygame.Color(0, 0, 0), 2.)