from typing import Dict

import pygame

from roguengine.component.window import WindowComponent
from roguengine.esper import Processor
from roguengine.event.log import LogEvent


class LoggerProcessor(Processor):

    def __init__(self, px: int, py: int, char_sprite_dict: Dict[str, pygame.Surface], message_count: int):
        super().__init__()
        self._px = px
        self._py = py
        self._char_sprite_dict = char_sprite_dict
        self._message_count = message_count
        self._msgs = []

    def put(self, msg: str):
        self._msgs.append(msg)
        while len(self._msgs) > self._message_count:
            self._msgs.pop(0)

    def process(self):

        for msg in self.world.receive(LogEvent):
            self._msgs.append(msg.msg)
            while len(self._msgs) > self._message_count:
                self._msgs.pop(0)

        for msg_index, msg in enumerate(self._msgs[::-1]):
            x = self._px
            y = self._py + (msg_index * self._char_sprite_dict["0"].get_height())
            for window_entity, [window_component] in self.world.get_components(WindowComponent):
                window_surface = window_component.surface()
                for c in msg:
                    if c not in self._char_sprite_dict:
                        continue
                    sprite = self._char_sprite_dict[c]
                    window_surface.blit(sprite, (x, y))
                    x += sprite.get_width()
