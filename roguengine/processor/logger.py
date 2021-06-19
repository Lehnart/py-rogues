import pygame

from roguengine.component.window import WindowComponent
from roguengine.esper import Processor
from roguengine.event.log import LogEvent
from roguengine.processor.ui import Font


class LoggerProcessor(Processor):

    def __init__(
            self,
            px: int,
            py: int,
            font: Font,
            message_count: int,
            new_log_color: pygame.Color,
            old_log_color: pygame.Color
    ):
        super().__init__()
        self._px = px
        self._py = py
        self._font = font
        self._message_count = message_count
        self._msgs = [""]*message_count
        self._new_color = new_log_color
        self._old_color = old_log_color

    def put(self, msg: str):
        self._msgs.append(msg)
        while len(self._msgs) > self._message_count:
            self._msgs.pop(0)

    def process(self):

        for msg in self.world.receive(LogEvent):
            self._msgs.append(msg.msg)
            while len(self._msgs) > self._message_count:
                self._msgs.pop(0)

        for msg_index, msg in enumerate(self._msgs):
            x = self._px
            y = self._py + (msg_index * self._font.get_char_height())
            for window_entity, [window_component] in self.world.get_components(WindowComponent):
                window_surface = window_component.surface()
                if msg_index == self._message_count-1 :
                    self._font.draw_string(msg, x, y, window_surface,self._new_color, pygame.Color(0, 0, 0))
                else :
                    self._font.draw_string(msg, x, y, window_surface, self._old_color, pygame.Color(0, 0, 0))
