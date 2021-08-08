from typing import List

from roguengine.rogue_esper import Processor
from roguengine.systems.text_form.components import TextFormComponent
from roguengine.systems.text_form.events import KeyPressedEvent


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
