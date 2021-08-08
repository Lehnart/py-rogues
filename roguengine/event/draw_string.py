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
