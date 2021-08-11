import pygame

from roguengine.rogue_esper import Event
from roguengine.util.font import Font


class DrawStringEvent(Event):

    def __init__(self, s: str, x: int, y: int, font_color: pygame.Color, bkgd_color: pygame.Color, font: Font):
        super().__init__()
        self.s = s
        self.x = x
        self.y = y
        self.font = font
        self.font_color = font_color
        self.bkgd_color = bkgd_color


class SetSpriteEvent(Event):

    def __init__(self, ent: int, sprite: pygame.Surface, is_invisible: bool = False):
        super().__init__()
        self.ent = ent
        self.sprite = sprite
        self.is_invisible = is_invisible


class MoveSpriteEvent(Event):

    def __init__(self, ent: int, dx: int, dy: int):
        super().__init__()
        self.ent = ent
        self.dx = dx
        self.dy = dy


class UpdateSpritePositionEvent(Event):

    def __init__(self, ent: int, x: int, y: int):
        super().__init__()
        self.ent = ent
        self.x = x
        self.y = y


class FlipEvent(Event):

    def __init__(self, ent: int):
        super().__init__()
        self.ent = ent


class CreateSpriteEvent(Event):

    def __init__(self, ent: int, px: int, py: int, sprite: pygame.Surface, layer: int = 0, is_invisible: bool = False):
        super().__init__()
        self.ent = ent
        self.sprite = sprite
        self.px = px
        self.py = py
        self.layer = layer
        self.is_invisible = is_invisible
