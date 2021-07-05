from roguengine.component.callable import CallableComponent
from roguengine.rogue_esper import Processor


class CallableProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for _, call_comp in self.world.get_component(CallableComponent):
            event_type = call_comp.event_type
            if any(self.world.receive(event_type)):
                call_comp.call()
