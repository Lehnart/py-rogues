import pygame

from roguengine.rogue_esper import Event


class SetSpriteEvent(Event):

    def __init__(self, ent: int, sprite: pygame.Surface, is_invisible: bool = False):
        super().__init__()
        self.ent = ent
        self.sprite = sprite
        self.is_invisible = is_invisible


class CreateSpriteEvent(Event):

    def __init__(self, ent: int, px: int, py: int, sprite: pygame.Surface, layer : int = 0, is_invisible: bool = False):
        super().__init__()
        self.ent = ent
        self.sprite = sprite
        self.px = px
        self.py = py
        self.layer = layer
        self.is_invisible = is_invisible
