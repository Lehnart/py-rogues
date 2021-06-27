from typing import List

from roguengine.component.text_form import TextFormComponent
from roguengine.esper import Processor
from roguengine.event.key_pressed import KeyPressedEvent


class TextFormProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for _, c in self.world.get_component(TextFormComponent):
            messages: List[KeyPressedEvent] = self.world.receive(KeyPressedEvent)
            for msg in messages:
                s = msg.code
                if s == '\r':
                    continue
                if s == '\b':
                    c.del_char()
                else:
                    c.add_char(s)
