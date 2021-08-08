from roguengine.callable.components import CallableComponent, KeyCallableComponent
from roguengine.callable.events import KeyPressedEvent
from roguengine.rogue_esper import Processor


class CallableProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for _, call_comp in self.world.get_component(CallableComponent):
            event_type = call_comp.event_type
            for event in self.world.receive(event_type):
                call_comp.call(event, self.world)


class KeyCallableProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for _, call_comp in self.world.get_component(KeyCallableComponent):
            key_pressed_event = call_comp.key_pressed_event
            for key_event in self.world.receive(KeyPressedEvent):
                if key_event.code != key_pressed_event.code:
                    continue
                call_comp.call()
