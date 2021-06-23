import pygame

pygame.init()

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 16
SPRITE_SHEET: pygame.Surface = pygame.image.load("res/tileset.bmp")


def get_sprite(px: int, py: int) -> pygame.Surface:
    sprite = SPRITE_SHEET.subsurface(pygame.Rect(px, py, SPRITE_WIDTH, SPRITE_HEIGHT))
    return sprite


SPRITE_DICT = {
    "player": get_sprite(576, 128),
    "spider": get_sprite(0, 0),
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
    "void": pygame.Surface((16, 16))
}
