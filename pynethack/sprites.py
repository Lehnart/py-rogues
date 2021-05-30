import pygame

pygame.init()

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 16
SPRITE_SHEET: pygame.Surface = pygame.image.load("res/tileset.bmp")


def get_sprite(px: int, py: int) -> pygame.Surface:
    sprite = SPRITE_SHEET.subsurface(pygame.Rect(px, py, SPRITE_WIDTH, SPRITE_HEIGHT))
    return sprite


SPRITE_DICT = {
    "player": get_sprite(0, 0),
    "wall": get_sprite(192,336),
    "ground": get_sprite(464,336),
    "corridor": get_sprite(496, 336),
    "door": get_sprite(400, 336),
}
