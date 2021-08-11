import datetime

import pygame

from roguengine.rogue_esper import Processor
from roguengine.systems.render.events import DrawStringEvent
from roguengine.util.font import Font


class TimeProcessor(Processor):

    def __init__(self, px: int, py: int, font: Font):
        super().__init__()
        self._font = font
        self._px = px
        self._py = py

    def process(self):
        now = datetime.datetime.now()
        string = "{:02d}:{:02d}".format(
            now.hour,
            now.minute
        )
        x = self._px
        y = self._py
        self.world.publish(DrawStringEvent(string, x, y, pygame.Color(0, 0, 0), pygame.Color(128, 128, 128), self._font))
