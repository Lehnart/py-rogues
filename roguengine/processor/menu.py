from roguengine.component.input.input_listener import InputListenerComponent
from roguengine.component.ui.menu import MenuComponent
from roguengine.event.menu_select import MenuSelectEvent
from roguengine.event.move import MoveEvent
from roguengine.rogue_esper import Processor


class MenuProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        messages = self.world.receive(MoveEvent)
        for msg in messages:
            _, dy = msg.movement.dx_dy()
            if dy == 0:
                continue

            for menu_entity, [menu, _] in self.world.get_components(MenuComponent, InputListenerComponent):
                menu.move_selection(dy)
                self.world.publish(MenuSelectEvent(menu_entity))
