import pygame

from roguengine.rogue_esper import Processor
from roguengine.systems.log.events import LogEvent
from roguengine.systems.render.events import DrawStringEvent
from roguengine.util.font import Font


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
        self._msgs = [""] * message_count
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
            if msg_index == self._message_count - 1:
                self.world.publish(DrawStringEvent(msg, x, y, self._new_color, pygame.Color(0, 0, 0), self._font))
            else:
                self.world.publish(DrawStringEvent(msg, x, y, self._old_color, pygame.Color(0, 0, 0), self._font))
