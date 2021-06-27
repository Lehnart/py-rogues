import time

from roguengine.component.blinking import BlinkingComponent
from roguengine.esper import Processor


class BlinkProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):

        for ent, comp in self.world.get_component(BlinkingComponent):

            last_time = comp.get_last_blinking_time()
            now = time.time()
            if now > last_time + comp.get_period():
                comp.blink()
