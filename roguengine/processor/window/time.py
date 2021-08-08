import datetime

import pygame

from roguengine.component.window.window import WindowComponent
from roguengine.rogue_esper import Processor
from roguengine.util.font import Font


class TimeProcessor(Processor):

    def __init__(self, px: int, py: int, font: Font):
        super().__init__()
        self._font = font
        self._px = px
        self._py = py

    def process(self):
        for window_entity, [window_component] in self.world.get_components(WindowComponent):
            window_surface = window_component.surface()
            now = datetime.datetime.now()
            string = "{:02d}:{:02d}".format(
                now.hour,
                now.minute
            )
            x = self._px
            y = self._py
            self._font.draw_string(string, x, y, window_surface, pygame.Color(0, 0, 0), pygame.Color(128, 128, 128))
