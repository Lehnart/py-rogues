import datetime
from typing import Dict

import pygame

from roguengine.component.window import WindowComponent
from roguengine.esper import Processor


class TimeProcessor(Processor):

    def __init__(self, px: int, py: int, char_sprite_dict: Dict[str, pygame.Surface]):
        super().__init__()
        self._char_sprite_dict = char_sprite_dict
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
            for c in string:
                if c not in self._char_sprite_dict:
                    continue
                sprite = self._char_sprite_dict[c]
                window_surface.blit(sprite, (x, y))
                x += sprite.get_width()
