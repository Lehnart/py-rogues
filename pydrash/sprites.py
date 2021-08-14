import pygame

pygame.init()

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 16
SPRITE_SHEET: pygame.Surface = pygame.image.load("res/sprites.png")
UI_FRAME_SPRITE: pygame.Surface = pygame.image.load("res/ui.png")

TILE_MAP_SPRITE = pygame.image.load("res/map_tiles.png")
RESIDENT_MAP_SPRITE = pygame.image.load("res/map_residents.png")


def get_sprite(px: int, py: int) -> pygame.Surface:
    sprite = SPRITE_SHEET.subsurface(pygame.Rect(px, py, SPRITE_WIDTH, SPRITE_HEIGHT))
    return sprite


SPRITE_DICT = {
    "player": get_sprite(0, 80),
    "wall": get_sprite(0, 16),
    "ground": get_sprite(16, 16),
    "corridor": get_sprite(32, 0),
    "void": get_sprite(0, 0),
    "forest": get_sprite(48, 0),
    "grass": get_sprite(64, 0),
    "water": get_sprite(96, 0)
}
