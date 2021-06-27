from typing import List, Type, Callable, Dict

from roguengine.esper import Processor, Event


class CallableProcessor(Processor):

    def __init__(self, event_dict: Dict[Type[Event], Callable]):
        super().__init__()
        self.event_classes = event_dict

    def process(self):
        for event_key in self.event_classes:
            messages = self.world.receive(event_key)
            for _ in messages:
                self.event_classes[event_key]()
